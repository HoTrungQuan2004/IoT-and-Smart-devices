import time
import paho.mqtt.client as mqtt
import json
from datetime import datetime

# Cấu hình Adafruit IO
ADAFRUIT_IO_USERNAME = "your_username"  # Thay bằng username của bạn
ADAFRUIT_IO_KEY = "aio_XXXXXX1234567890"  # Thay bằng key của bạn
FEED_NAME = "gps-data"  # Tên feed trên Adafruit IO
MQTT_BROKER = "io.adafruit.com"
MQTT_PORT = 1883  # Hoặc 8883 nếu dùng SSL
MQTT_TOPIC = f"{ADAFRUIT_IO_USERNAME}/feeds/{FEED_NAME}"
MQTT_LOCATION_TOPIC = f"{ADAFRUIT_IO_USERNAME}/feeds/{FEED_NAME}.location"  # Topic cho location metadata

# Danh sách điểm GPS mẫu (giữ nguyên từ mã gốc)
GPS_POINTS = [
    {"lat": 47.645913, "lon": -122.132297, "alt": 10},
    {"lat": 47.645926, "lon": -122.132156, "alt": 10},
    {"lat": 47.645873, "lon": -122.131999, "alt": 10},
    {"lat": 47.645791, "lon": -122.131884, "alt": 10},
    {"lat": 47.645791, "lon": -122.131884, "alt": 10}
]

def on_connect(client, userdata, flags, rc, properties=None):
    if rc == 0:
        print("Connected to Adafruit IO MQTT broker")
    else:
        print(f"Failed to connect, return code {rc}")

def create_client():
    # Tạo MQTT client
    client = mqtt.Client(client_id="gps-sensor-client", protocol=mqtt.MQTTv311)
    client.username_pw_set(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)
    client.on_connect = on_connect
    client.connect(MQTT_BROKER, MQTT_PORT)
    client.loop_start()  # Bắt đầu vòng lặp xử lý mạng
    return client

def run_telemetry_sample(client):
    print("Sending periodic GPS messages to Adafruit IO")
    gps_index = 0
    while True:
        # Lấy điểm GPS hiện tại
        gps_point = GPS_POINTS[gps_index]
        gps_index = (gps_index + 1) % len(GPS_POINTS)
        
        # Tạo dữ liệu GPS
        msg_data = {
            "deviceId": "gps-sensor",
            "timestamp": datetime.utcnow().isoformat(),
            "lat": gps_point["lat"],
            "lon": gps_point["lon"],
            "alt": gps_point["alt"]
        }
        
        # Gửi dữ liệu JSON đến feed
        payload = json.dumps(msg_data)
        print(f"Sending message: {msg_data}")
        client.publish(MQTT_TOPIC, payload, qos=1)
        
        # Gửi location metadata (lat, lon, ele)
        location_payload = json.dumps({
            "lat": gps_point["lat"],
            "lon": gps_point["lon"],
            "ele": gps_point["alt"]
        })
        client.publish(MQTT_LOCATION_TOPIC, location_payload, qos=1)
        
        time.sleep(30)  # Gửi mỗi 30 giây

def main():
    print("Simulated GPS device sending to Adafruit IO")
    client = create_client()
    try:
        run_telemetry_sample(client)
    except KeyboardInterrupt:
        print("Stopping...")
        client.loop_stop()
        client.disconnect()

if __name__ == '__main__':
    main()