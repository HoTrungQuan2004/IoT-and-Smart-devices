import paho.mqtt.client as mqtt
import json
import os
from shapely.geometry import Point, Polygon
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import time
from dotenv import load_dotenv # Import load_dotenv

# --- Configuration ---
load_dotenv() # Load variables from .env file at the start

# MQTT Broker Configuration
MQTT_BROKER_HOST = "localhost"
MQTT_BROKER_PORT = 1883
MQTT_TOPIC_GPS = "iot/gps_data"

# Geofence Polygon Coordinates (longitude, latitude)
# Example: A square around the Empire State Building area
GEOFENCE_POLYGON_COORDS = [
    (-73.988429, 40.748817),  # Bottom-left
    (-73.981369, 40.748817),  # Bottom-right
    (-73.981369, 40.752817),  # Top-right
    (-73.988429, 40.752817),  # Top-left
    (-73.988429, 40.748817)   # Closing point (same as first)
]
geofence_polygon = Polygon(GEOFENCE_POLYGON_COORDS)

# SendGrid Configuration (loaded from .env file)
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL") # Your verified SendGrid sender email
RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL") # Where to send notifications

# Notification state (to avoid spamming for the same device continuously inside)
# Stores device_id: last_notification_time
device_notification_state = {}
NOTIFICATION_COOLDOWN_SECONDS = 300 # 5 minutes

# --- Helper Functions ---
def is_inside_geofence(latitude, longitude):
    point = Point(longitude, latitude) # Create a Shapely Point
    return geofence_polygon.contains(point)

def send_email_notification(device_id, latitude, longitude):
    if not SENDGRID_API_KEY or not SENDER_EMAIL or not RECEIVER_EMAIL:
        print("Geofence Monitor: SendGrid API Key or emails not configured. Cannot send email.")
        print("Ensure SENDGRID_API_KEY, SENDER_EMAIL, and RECEIVER_EMAIL are set in your .env file.")
        return

    message_body = (
        f"Alert: Device '{device_id}' has entered the geofence.\n\n"
        f"Coordinates: Latitude={latitude}, Longitude={longitude}\n"
        f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    )
    message = Mail(
        from_email=SENDER_EMAIL,
        to_emails=RECEIVER_EMAIL,
        subject=f"[Geofence Alert] Device {device_id} Inside Geofence",
        html_content=f"<strong>Alert:</strong> Device <code>{device_id}</code> has entered the geofence.<br><br>"
                     f"<strong>Coordinates:</strong> Latitude={latitude}, Longitude={longitude}<br>"
                     f"<strong>Timestamp:</strong> {time.strftime('%Y-%m-%d %H:%M:%S %Z')}"
    )
    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)
        print(f"Geofence Monitor: Email sent! Status Code: {response.status_code} for device {device_id}")
    except Exception as e:
        print(f"Geofence Monitor: Error sending email for device {device_id}: {e}")

# --- MQTT Callbacks ---
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Geofence Monitor: Connected to MQTT Broker!")
        client.subscribe(MQTT_TOPIC_GPS)
        print(f"Geofence Monitor: Subscribed to topic: {MQTT_TOPIC_GPS}")
    else:
        print(f"Geofence Monitor: Failed to connect, return code {rc}")

def on_message(client, userdata, msg):
    print(f"Geofence Monitor: Received message on topic '{msg.topic}': {msg.payload.decode()}")
    try:
        data = json.loads(msg.payload.decode())
        latitude = data.get("latitude")
        longitude = data.get("longitude")
        device_id = data.get("deviceId", "UnknownDevice")

        if latitude is not None and longitude is not None:
            if is_inside_geofence(latitude, longitude):
                print(f"Geofence Monitor: Device {device_id} ({latitude}, {longitude}) is INSIDE the geofence.")

                current_time = time.time()
                last_notified_time = device_notification_state.get(device_id, 0)

                if current_time - last_notified_time > NOTIFICATION_COOLDOWN_SECONDS:
                    send_email_notification(device_id, latitude, longitude)
                    device_notification_state[device_id] = current_time
                else:
                    print(f"Geofence Monitor: Notification for {device_id} is on cooldown.")
            else:
                print(f"Geofence Monitor: Device {device_id} ({latitude}, {longitude}) is OUTSIDE the geofence.")
                if device_id in device_notification_state:
                    del device_notification_state[device_id]
        else:
            print("Geofence Monitor: Received message with missing lat/lon.")

    except json.JSONDecodeError:
        print("Geofence Monitor: Failed to decode JSON message.")
    except Exception as e:
        print(f"Geofence Monitor: Error processing message: {e}")

# --- Main Application ---
if __name__ == "__main__":
    if not all([SENDGRID_API_KEY, SENDER_EMAIL, RECEIVER_EMAIL]):
        print("CRITICAL: SendGrid API Key, Sender Email, or Receiver Email is not configured correctly or not found in .env file.")
        # exit(1) # Consider exiting if critical env vars are missing

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, client_id="geofence-monitor-app")
    client.on_connect = on_connect
    client.on_message = on_message

    try:
        client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
    except Exception as e:
        print(f"Geofence Monitor: Could not connect to MQTT Broker at {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT} - {e}")
        exit()

    print("Geofence Monitor: Starting MQTT loop (Ctrl+C to stop)...")
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        print("Geofence Monitor: Shutting down...")
    finally:
        client.disconnect()
        print("Geofence Monitor: Disconnected.")