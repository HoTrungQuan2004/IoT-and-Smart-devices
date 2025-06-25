import time
import numpy as np
import tflite_runtime.interpreter as tflite
from counterfit_connection import CounterFitConnection
import requests
from PIL import Image
import io
import base64
import json

# Adafruit IO config
AIO_USERNAME = ""
AIO_KEY = ""
# change these feeds' name to match your Adafruit IO feeds
FEED_DISTANCE = "distance"
FEED_RESULT = "ripe-or-unripe-fruits"
FEED_LED = "led-control"

ADAFRUIT_IO_URL = "https://io.adafruit.com/api/v2"

# CounterFit setup
CounterFitConnection.init('localhost', 5000)
DISTANCE_SENSOR_INDEX = 0
CAMERA_PORT = "sensor_1"
LED_PIN = 22
DISTANCE_THRESHOLD = 200

# AI model
MODEL_PATH = "model.tflite"
interpreter = tflite.Interpreter(model_path=MODEL_PATH)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
IMG_WIDTH, IMG_HEIGHT = input_details[0]['shape'][2], input_details[0]['shape'][1]

def send_to_adafruit(feed, value):
    url = f"{ADAFRUIT_IO_URL}/{AIO_USERNAME}/feeds/{feed}/data"
    headers = {"X-AIO-Key": AIO_KEY, "Content-Type": "application/json"}
    payload = {"value": str(value)}
    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code in [200,201]:
            print(f"✅ Sent to Adafruit IO feed {feed}: {value}")
        else:
            print(f"⚠️ Failed to send to {feed}: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Error sending to Adafruit IO: {e}")

def get_latest_from_adafruit(feed):
    url = f"{ADAFRUIT_IO_URL}/{AIO_USERNAME}/feeds/{feed}/data/last"
    headers = {"X-AIO-Key": AIO_KEY}
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json().get("value", None)
        return None
    except Exception as e:
        print(f"❌ Error reading from Adafruit IO: {e}")
        return None

def control_led(status):
    CounterFitConnection.set_actuator_float_value(LED_PIN, float(status))

def read_proximity():
    return CounterFitConnection.get_sensor_int_value(DISTANCE_SENSOR_INDEX)

def get_image_from_counterfit(port="sensor_1"):
    url = f"http://localhost:5000/binary_sensor_data?port={port}"
    try:
        response = requests.get(url)
    except Exception as e:
        print(f"Error connecting to CounterFit camera API: {e}")
        return None
    content_type = response.headers.get("Content-Type", "")
    if response.status_code != 200:
        return None
    if "image" in content_type:
        img = Image.open(io.BytesIO(response.content))
    else:
        try:
            data = response.json()
            base64_str = data.get("value", "")
            if not base64_str:
                return None
            img_bytes = base64.b64decode(base64_str)
            img = Image.open(io.BytesIO(img_bytes))
        except Exception:
            return None
    img = img.resize((IMG_WIDTH, IMG_HEIGHT))
    img = img.convert("RGB")
    img_array = np.array(img, dtype=np.uint8)
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

def classify_image(img_array):
    interpreter.set_tensor(input_details[0]['index'], img_array)
    interpreter.invoke()
    output = interpreter.get_tensor(output_details[0]['index'])
    pred = np.argmax(output)
    return pred

print("\n🚦 Fruit detector started! Press Ctrl+C to stop.\n")

try:
    while True:
        distance = read_proximity()
        print(f"Distance: {distance} mm")
        send_to_adafruit(FEED_DISTANCE, distance)

        # Read LED control commands from Adafruit IO
        led_cmd = get_latest_from_adafruit(FEED_LED)
        if led_cmd is not None:
            control_led(led_cmd == "1")
            print(f"LED command from cloud: {'ON' if led_cmd=='1' else 'OFF'}")

        # If the object is nearby, take a picture, classify it, and send the result to the cloud
        if distance < DISTANCE_THRESHOLD:
            print("Object detected! Capturing image from camera sensor...")
            img_array = get_image_from_counterfit(CAMERA_PORT)
            if img_array is None:
                print("⚠️  No image received from camera sensor.")
                time.sleep(1)
                continue
            label = classify_image(img_array)
            print("AI prediction:", label)
            send_to_adafruit(FEED_RESULT, label)
            # Send LED on/off command to led_control feed (can be used for cloud-to-device testing)
            if label == 0:
                control_led(True)
                send_to_adafruit(FEED_LED, 1)
                print("Unripe fruit detected, LED ON")
            else:
                control_led(False)
                send_to_adafruit(FEED_LED, 0)
                print("Ripe fruit detected, LED OFF")
            time.sleep(5)
        time.sleep(0.5)
except KeyboardInterrupt:
    pass
finally:
    control_led(False)
    print("Program terminated.")
