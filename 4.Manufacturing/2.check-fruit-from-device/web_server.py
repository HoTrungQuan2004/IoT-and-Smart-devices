from flask import Flask, jsonify
import paho.mqtt.client as mqtt
import os
import time

app = Flask(__name__)

# --- Adafruit IO Configuration ---
ADAFRUIT_IO_USERNAME = os.environ.get('ADAFRUIT_IO_USERNAME')
ADAFRUIT_IO_KEY = os.environ.get('ADAFRUIT_IO_KEY')
ADAFRUIT_IO_FEED_STATUS = "fruit-status" # Feed from device to server
ADAFRUIT_IO_FEED_COMMAND = "actuator-command" # Feed server sends commands to device
MQTT_BROKER = "io.adafruit.com"
MQTT_PORT = 1883

# --- MQTT Callbacks for Flask Server ---
def on_connect_server(client, userdata, flags, rc):
    print("Flask server connected to Adafruit IO with result code " + str(rc))
    client.subscribe(f"{ADAFRUIT_IO_USERNAME}/feeds/{ADAFRUIT_IO_FEED_STATUS}")
    print(f"Flask server listening to feed: {ADAFRUIT_IO_USERNAME}/feeds/{ADAFRUIT_IO_FEED_STATUS}")

def on_message_server(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"Flask server received message - Topic: {topic}, Payload: {payload}")

    if topic == f"{ADAFRUIT_IO_USERNAME}/feeds/{ADAFRUIT_IO_FEED_STATUS}":
        fruit_status = payload
        print(f"Flask server processing fruit status: {fruit_status}")

        command_to_device = ""
        # Logic for classification and commanding
        if fruit_status == "ripe":
            command_to_device = "turn_off_led"
            print("Flask server: Fruit is ripe, sending turn off command.")
        elif fruit_status == "unripe":
            command_to_device = "turn_on_led"
            print("Flask server: Fruit is unripe, sending turn on command.")
        elif fruit_status == "rotten":
            command_to_device = "turn_on_led"
            print("Flask server: Fruit is rotten, sending turn on command.")
        else:
            print(f"Flask server: Unknown status: {fruit_status}. No command sent.")

        # Send command down to the device via Adafruit IO
        try:
            if command_to_device:
                client.publish(f"{ADAFRUIT_IO_USERNAME}/feeds/{ADAFRUIT_IO_FEED_COMMAND}", command_to_device)
                print(f"Flask server: Command '{command_to_device}' sent to feed '{ADAFRUIT_IO_FEED_COMMAND}'")
        except Exception as e:
            print(f"Flask server: Error sending command via Adafruit IO: {e}")

# Initialize MQTT client for Flask server
server_mqtt_client = mqtt.Client()
server_mqtt_client.username_pw_set(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
server_mqtt_client.on_connect = on_connect_server
server_mqtt_client.on_message = on_message_server

# Simple endpoint to check if the server is running
@app.route('/')
def home():
    return "Flask/FastAPI server is running and listening to Adafruit IO."

if __name__ == '__main__':
    # Set environment variables for Adafruit IO Username and Key before running the server
    # export ADAFRUIT_IO_USERNAME="your_username"
    # export ADAFRUIT_IO_KEY="your_aio_key"

    try:
        server_mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
        server_mqtt_client.loop_start() # Start MQTT background thread
    except Exception as e:
        print(f"Could not connect MQTT for Flask server: {e}")
        exit()

    app.run(debug=True, port=5001, use_reloader=False) # use_reloader=False to avoid initializing MQTT client twice