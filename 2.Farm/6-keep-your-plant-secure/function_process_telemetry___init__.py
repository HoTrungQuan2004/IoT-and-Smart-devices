import json
import os
import logging
from azure.iot.hub import IoTHubRegistryManager
from azure.iot.hub.models import CloudToDeviceMethod

def main(event):
    try:
        # Parse telemetry
        body = json.loads(event.get_body().decode('utf-8'))
        device_id = event.iothub_metadata['connection-device-id']
        soil_moisture = body['soil_moisture']
        
        # IoT Hub service client
        connection_string = os.environ['IotHubConnectionString']
        registry_manager = IoTHubRegistryManager(connection_string)
        
        # Decision logic with creative threshold
        threshold = 400
        method_name = 'relay_on' if soil_moisture < threshold else 'relay_off'
        direct_method = CloudToDeviceMethod(method_name=method_name, payload=json.dumps({"moisture": soil_moisture}))
        registry_manager.invoke_device_method(device_id, direct_method)
        logging.info(f"Device: {device_id} | Moisture: {soil_moisture} | Action: {method_name}")
    except Exception as e:
        logging.error(f"Error processing telemetry: {e}")