from counterfit_connection import CounterFitConnection
CounterFitConnection.init('127.0.0.1', 5000)

import time
import counterfit_shims_serial
import pynmea2
import json
import paho.mqtt.client as mqtt
from datetime import datetime

# Adafruit IO Configuration
ADAFRUIT_IO_USERNAME = "YOUR_IO_USERNAME"  # Replace with your username
ADAFRUIT_IO_KEY = "YOUR_ACTIVE_KEY"  # Replace with your key
FEED_NAME = "gps-data"
MQTT_BROKER = "io.adafruit.com"
MQTT_PORT = 1883  # Try 8883 if 1883 fails
MQTT_TOPIC = f"{ADAFRUIT_IO_USERNAME}/feeds/{FEED_NAME}"
MQTT_LOCATION_TOPIC = f"{ADAFRUIT_IO_USERNAME}/feeds/{FEED_NAME}.location"

# Initialize CounterFit serial
try:
    serial = counterfit_shims_serial.Serial('/dev/ttyAMA0')
    print("Serial initialized on COM1")
except Exception as e:
    print(f"Error initializing serial: {e}")
    serial = None

# Initialize MQTT client
def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to Adafruit IO MQTT broker")
    else:
        print(f"Failed to connect, return code {rc}")

client = mqtt.Client(client_id="gps-sensor-client", protocol=mqtt.MQTTv311)
client.username_pw_set(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
client.on_connect = on_connect
try:
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_start()
    print("Connected to Adafruit IO")
except Exception as e:
    print(f"Error connecting to MQTT: {e}")

def send_gps_data(line):
    try:
        msg = pynmea2.parse(line, check=False)
        if msg.sentence_type == 'GGA':
            lat = pynmea2.dm_to_sd(msg.lat)
            lon = pynmea2.dm_to_sd(msg.lon)

            if msg.lat_dir == 'S':
                lat = lat * -1
            if msg.lon_dir == 'W':
                lon = lon * -1

            alt = getattr(msg, 'altitude', 10)  # Default 10 if missing

            message_json = {
                "deviceId": "gps-sensor",
                "timestamp": datetime.utcnow().isoformat(),
                "gps": {"lat": lat, "lon": lon, "alt": alt}
            }

            payload = json.dumps(message_json)
            print("Sending telemetry", message_json)
            print("Raw payload:", payload)
            client.publish(MQTT_TOPIC, payload, qos=1)

            location_payload = f"{lat},{lon},{alt}"
            print("Location payload:", location_payload)
            client.publish(MQTT_LOCATION_TOPIC, location_payload, qos=1)


    except pynmea2.ParseError as e:
        print(f"Error: {e}")

if serial:
    while True:
        try:
            line = serial.readline().decode('utf-8')
            print(f"Read line: {line}")
            while len(line) > 0:
                send_gps_data(line)
                line = serial.readline().decode('utf-8')
            time.sleep(60)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(60)
else:
    print("Serial not initialized, exiting...")