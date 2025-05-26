import paho.mqtt.client as mqtt
import time
import json
import random

# MQTT Broker Configuration
MQTT_BROKER_HOST = "localhost"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC_GPS = "iot/gps_data"

# Sample GPS coordinates (longitude, latitude)
# Some inside, some outside the example GEOFENCE_POLYGON_COORDS from Step 3
GPS_SAMPLES = [
    {"id": "device1", "name": "Point A (Inside)", "longitude": -73.985679, "latitude": 40.750000}, # Inside
    {"id": "device1", "name": "Point B (Outside)", "longitude": -74.000000, "latitude": 40.750000}, # Outside (West)
    {"id": "device1", "name": "Point C (Inside)", "longitude": -73.984000, "latitude": 40.751000}, # Inside
    {"id": "device1", "name": "Point D (Outside)", "longitude": -73.985679, "latitude": 40.760000}, # Outside (North)
]

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Virtual GPS Device: Connected to MQTT Broker!")
    else:
        print(f"Virtual GPS Device: Failed to connect, return code {rc}")

def on_publish(client, userdata, mid):
    print(f"Virtual GPS Device: Message {mid} published.")

client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id="virtual-gps-device")
client.on_connect = on_connect
client.on_publish = on_publish

try:
    client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
except Exception as e:
    print(f"Virtual GPS Device: Could not connect to MQTT Broker at {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT} - {e}")
    exit()

client.loop_start() # Start network loop in background to handle reconnections

try:
    while True:
        # Pick a random sample
        data_point = random.choice(GPS_SAMPLES)
        payload = json.dumps({
            "deviceId": data_point["id"],
            "latitude": data_point["latitude"],
            "longitude": data_point["longitude"],
            "description": data_point["name"], # For easier debugging
            "timestamp": time.time()
        })
        result = client.publish(MQTT_TOPIC_GPS, payload)
        result.wait_for_publish() # Wait for publish to complete
        print(f"Virtual GPS Device: Sent data: {payload}")
        time.sleep(10)  # Send data every 10 seconds
except KeyboardInterrupt:
    print("Virtual GPS Device: Shutting down...")
finally:
    client.loop_stop()
    client.disconnect()
    print("Virtual GPS Device: Disconnected.")