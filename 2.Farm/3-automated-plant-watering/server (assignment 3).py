import json
import time
import paho.mqtt.client as mqtt

id = 'Group2'

client_telemetry_topic = id + '/telemetry'
server_command_topic = id + '/commands'
client_name = id + 'soilmoisturesensor_server'

mqtt_client = mqtt.Client(client_name)
mqtt_client.connect('test.mosquitto.org')

mqtt_client.loop_start()

# Define constants
target_soil_moisture = 500
average_decrease_per_second = 21.67

def handle_telemetry(client, userdata, message):
    payload = json.loads(message.payload.decode())
    print("Message received:", payload)
    
    current_soil_moisture = payload['soil_moisture']
    
    if current_soil_moisture > target_soil_moisture:
        # Calculate how much to decrease the reading to reach the target
        required_decrease = current_soil_moisture - target_soil_moisture
        # Calculate pump runtime and round to the nearest second
        required_runtime = round(required_decrease / average_decrease_per_second)
        command = {'run_pump_for': required_runtime}
        print("Sending message:", command)
        client.publish(server_command_topic, json.dumps(command))
    else:
        print("Soil moisture is at or below target, no watering needed.")

mqtt_client.subscribe(client_telemetry_topic)
mqtt_client.on_message = handle_telemetry

while True:
    time.sleep(2)