import os
import json
import time
import random
from azure.iot.device import IoTHubDeviceClient, Message, MethodResponse, X509
from counterfit_shims_grove.grove_moisture import GroveMoisture
from counterfit_shims_grove.grove_relay import GroveRelay

# CounterFit configuration
os.environ['COUNTERFIT_HOST'] = 'localhost'
os.environ['COUNTERFIT_PORT'] = '5000'

# Virtual devices
soil_moisture_sensor = GroveMoisture(0)  # Analog pin 0
relay = GroveRelay(2)  # Digital pin 2

# X.509 certificate setup
x509 = X509(
    cert_file="device/certs/soil-moisture-sensor-x509-cert.pem",
    key_file="device/certs/soil-moisture-sensor-x509-key.pem",
    pass_phrase=None
)

# IoT Hub client
device_client = IoTHubDeviceClient.create_from_x509_certificate(
    hostname="plant-secure-hub-789.azure-devices.net",
    device_id="soil-moisture-sensor-x509",
    x509=x509
)

# Connect to IoT Hub
device_client.connect()
print("Connected to plant-secure-hub-789 as soil-moisture-sensor-x509")

# Direct method handler
def method_request_handler(method_request):
    if method_request.name == "relay_on":
        relay.on()
        print("Water pump activated! Sprinkling life into the soil.")
        response_status = 200
        response_payload = {"result": "Water pump turned ON", "timestamp": time.ctime()}
    elif method_request.name == "relay_off":
        relay.off()
        print("Water pump stopped. Soil is resting.")
        response_status = 200
        response_payload = {"result": "Water pump turned OFF", "timestamp": time.ctime()}
    else:
        response_status = 404
        response_payload = {"result": "Unknown command"}
    method_response = MethodResponse.create_from_method_request(method_request, response_status, response_payload)
    device_client.send_method_response(method_response)

# Simulate initial soil moisture
current_moisture = 650  # Starting value (0-1023 range, moderately moist)

# Main loop with dynamic simulation
while True:
    # Simulate soil drying out (decrease moisture randomly)
    current_moisture = max(0, current_moisture - random.randint(5, 20))
    soil_moisture_sensor.value = current_moisture  # Update CounterFit sensor
    moisture_reading = soil_moisture_sensor.value

    # Send telemetry with creative metadata
    message = Message(json.dumps({
        "soil_moisture": moisture_reading,
        "device": "soil-moisture-sensor-x509",
        "status": "healthy" if moisture_reading > 400 else "needs_water",
        "garden_zone": "sunflower_patch"
    }))
    device_client.send_message(message)
    print(f"Telemetry sent: Soil Moisture = {moisture_reading}, Status = {'healthy' if moisture_reading > 400 else 'needs water'}")

    # Check for direct method calls
    method_request = device_client.receive_method_request(timeout=1)
    if method_request:
        method_request_handler(method_request)

    time.sleep(5)