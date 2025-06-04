import picamera
import requests
import time
import json
import paho.mqtt.client as mqtt # For Adafruit IO connection
import os

# --- Adafruit IO Configuration ---
ADAFRUIT_IO_USERNAME = os.environ.get('ADAFRUIT_IO_USERNAME') # Get from environment variables
ADAFRUIT_IO_KEY = os.environ.get('ADAFRUIT_IO_KEY')         # Get from environment variables
ADAFRUIT_IO_FEED_STATUS = "fruit-status"
ADAFRUIT_IO_FEED_COMMAND = "actuator-command"
MQTT_BROKER = "io.adafruit.com"
MQTT_PORT = 1883

# --- Teachable Machine Configuration ---
# Replace with your Teachable Machine model's API URL
TEACHABLE_MACHINE_API_URL = "YOUR_TEACHABLE_MACHINE_MODEL_URL_HERE"

# --- Virtual Camera (CounterFit) Configuration ---
# Name of the image file to temporarily save
IMAGE_FILE = "fruit_image.jpg"
# Simulate a virtual LED (CounterFit Pin 13)
# Refer to CounterFit documentation for actuator simulation
LED_PIN = 13 # Example, you can configure an LED on CounterFit

# --- MQTT Callbacks ---
def on_connect(client, userdata, flags, rc):
    print("Connected to Adafruit IO with result code " + str(rc))
    # Subscribe to the command feed to receive commands from the Flask/FastAPI server
    client.subscribe(f"{ADAFRUIT_IO_USERNAME}/feeds/{ADAFRUIT_IO_FEED_COMMAND}")
    print(f"Subscribed to {ADAFRUIT_IO_USERNAME}/feeds/{ADAFRUIT_IO_FEED_COMMAND}")

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"Received message - Topic: {topic}, Payload: {payload}")

    if topic == f"{ADAFRUIT_IO_USERNAME}/feeds/{ADAFRUIT_IO_FEED_COMMAND}":
        handle_actuator_command(payload)

def handle_actuator_command(command):
    # This is where you would control the virtual actuator via CounterFit
    # CounterFit shims for actuators need to be installed and imported
    # Example with relay/GPIO shim (you might need to install 'counterfit-shims-gpio')
    # import counterfit_shims_gpio as GPIO
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(LED_PIN, GPIO.OUT)

    if command == "turn_on_led":
        print(f"[{time.time()}] Activating virtual LED (Pin {LED_PIN}) ON")
        # GPIO.output(LED_PIN, GPIO.HIGH) # Perform turning on virtual LED
        # For simplicity in a virtual environment, you can just print logs
    elif command == "turn_off_led":
        print(f"[{time.time()}] Activating virtual LED (Pin {LED_PIN}) OFF")
        # GPIO.output(LED_PIN, GPIO.LOW) # Perform turning off virtual LED
        # For simplicity in a virtual environment, you can just print logs
    else:
        print(f"Unknown command: {command}")

# --- Function to send image to Teachable Machine ---
def classify_image(image_path):
    with open(image_path, 'rb') as f:
        image_data = f.read()

    headers = {'Content-Type': 'application/octet-stream'}
    try:
        response = requests.post(TEACHABLE_MACHINE_API_URL, headers=headers, data=image_data)
        predictions = response.json().get('predictions', [])
        return predictions
    except requests.exceptions.RequestException as e:
        print(f"Error sending image to Teachable Machine: {e}")
        return None

# --- Main logic ---
if __name__ == "__main__":
    # Initialize MQTT client
    client = mqtt.Client()
    client.username_pw_set(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to Adafruit IO
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        client.loop_start() # Start a background thread to handle messages
    except Exception as e:
        print(f"Could not connect to Adafruit IO: {e}")
        exit()

    # Initialize Virtual Camera (CounterFit)
    # picamera will automatically use CounterFit shim if CounterFit server is running
    try:
        with picamera.PiCamera() as camera:
            camera.resolution = (640, 480) # Configure resolution
            camera.rotation = 0            # Configure image rotation
            time.sleep(2) # Allow camera to start up

            print("Virtual device ready. Starting image capture...")

            while True:
                print("Capturing fruit image...")
                camera.capture(IMAGE_FILE)
                print(f"Image captured: {IMAGE_FILE}")

                # Classify image
                predictions = classify_image(IMAGE_FILE)

                if predictions:
                    # Find the prediction with the highest confidence
                    best_prediction = max(predictions, key=lambda x: x['probability'])
                    label = best_prediction['className']
                    probability = best_prediction['probability'] * 100

                    print(f"Classification result: {label} (Confidence: {probability:.2f}%)")

                    # Send fruit status to Adafruit IO
                    try:
                        client.publish(f"{ADAFRUIT_IO_USERNAME}/feeds/{ADAFRUIT_IO_FEED_STATUS}", label)
                        print(f"Published '{label}' to Adafruit IO feed '{ADAFRUIT_IO_FEED_STATUS}'")
                    except Exception as e:
                        print(f"Error publishing to Adafruit IO: {e}")

                else:
                    print("Could not classify image.")

                time.sleep(5) # Wait 5 seconds before capturing the next image
    except Exception as e:
        print(f"Error initializing or using virtual camera: {e}")
        print("Ensure CounterFit server is running and you have installed counterfit-shims-picamera.")

    finally:
        client.loop_stop() # Stop MQTT background thread
        client.disconnect()
        print("Virtual device stopped.")