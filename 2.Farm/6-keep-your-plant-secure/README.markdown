# 🌱 Secure IoT Plant Watering System: Assignment 10 - Keep Your Plant Secure

Welcome to the **Secure IoT Plant Watering System**! This solution brings your garden to life with a virtual soil moisture sensor and water pump, securely connected to Azure IoT Hub using X.509 certificates. An Azure Function acts as the brain, deciding when to water your plants based on soil moisture levels. Built in a GitHub Codespace with CounterFit for simulation. 🌼

## 🎯 Project Overview

Imagine a sunflower patch where the soil whispers its needs. Our IoT device, named `bloom-sensor-x509`, listens by simulating soil moisture and sends data to Azure IoT Hub. If the soil gets too dry (below 400), an Azure Function commands the virtual water pump to sprinkle life back into the earth. Security is paramount—X.509 certificates ensure our device communicates safely. The result? A thriving virtual garden, all managed from the cloud! 🌞

### Key Features

- **Virtual Sensors**: Uses CounterFit to simulate a soil moisture sensor and water pump relay.
- **Secure Connection**: Authenticates with Azure IoT Hub using X.509 certificates.
- **Smart Watering**: An Azure Function processes telemetry and controls the pump based on soil moisture.
- **Dynamic Simulation**: Soil moisture decreases over time, mimicking real-world drying.
- **Creative Touches**: Includes garden-themed metadata (e.g., "sunflower_patch") and playful logs like "Sprinkling life into the soil!"

## 🛠️ Project Structure

The project is organized for clarity:

```
secure-plant-watering/
├── device/
│   ├── main.py                     # Device code for telemetry and actuator control
│   ├── requirements.txt            # Python dependencies for device
│   └── certs/
│       ├── bloom-sensor-x509-cert.pem  # X.509 certificate (generated)
│       ├── bloom-sensor-x509-key.pem   # X.509 private key (generated)
├── function/
│   └── process_telemetry/
│       ├── __init__.py            # Azure Function to process telemetry
│       ├── function.json          # Function configuration
│   └── local.settings.json        # Local settings for function
└── README.md                      
```

1. **Log in to Azure**:

   - Run:

     ```bash
     az login
     ```

2. **Create Resource Group and IoT Hub**:

   - Set up the Azure environment:

     ```bash
     az group create --name evergreen-rg --location eastus
     az iot hub create --name flora-guard-hub-2025 --resource-group evergreen-rg --sku S1
     ```

3. **Register Device with X.509 Certificates**:

   - Generate certificates:

     ```bash
     mkdir -p device/certs
     az iot hub device-identity create --device-id bloom-sensor-x509 --am x509_thumbprint --output-dir device/certs --hub-name flora-guard-hub-2025
     ```
   - This creates `device/certs/bloom-sensor-x509-cert.pem` and `device/certs/bloom-sensor-x509-key.pem`.

4. **Get Connection Strings**:

   - IoT Hub service connection string:

     ```bash
     az iot hub show-connection-string --hub-name flora-guard-hub-2025 --policy-name service
     ```
     - Copy the output (e.g., `HostName=flora-guard-hub-2025.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=...`).
   - Event Hub connection string:
     - In Azure Portal, go to IoT Hub &gt; Built-in endpoints &gt; Event Hub compatible endpoint.
     - Copy the endpoint (e.g., `Endpoint=sb://ihsuprodxyz.servicebus.windows.net/...`).
     - Note the Event Hub name (e.g., `iothub-ehub-flora-gua-2025-xyz123`).

5. **Update Function Settings**:

   - Open `function/local.settings.json` and replace the placeholders:

     ```json
     {
       "IsEncrypted": false,
       "Values": {
         "AzureWebJobsStorage": "",
         "FUNCTIONS_WORKER_RUNTIME": "python",
         "IotHubConnectionString": "HostName=flora-guard-hub-2025.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=xyz123...",
         "EventHubConnectionString": "Endpoint=sb://ihsuprodxyz.servicebus.windows.net/;SharedAccessKeyName=iothubowner;SharedAccessKey=abc456...;EntityPath=iothub-ehub-flora-gua-2025-xyz123",
         "EventHubName": "iothub-ehub-flora-gua-2025-xyz123"
       }
     }
     ```

### Step 3: Run the Virtual Device with CounterFit

1. **Start CounterFit**:

   - In the terminal:

     ```bash
     counterfit
     ```
   - Open the CounterFit web app (click the forwarded port URL, e.g., `https://<codespace-name>-5000.github.dev`).

2. **Configure Virtual Sensors**:

   - In the CounterFit UI:
     - Add a **Grove Moisture Sensor** on analog pin 0.
     - Add a **Grove Relay** on digital pin 2.
   - Confirm settings (leave defaults for now; the code sets values dynamically).

3. **Run the Device Code**:

   - In a new terminal (Ctrl+Shift+\`):

     ```bash
     cd device
     python main.py
     ```
   - Watch the output:

     ```
     Connected to flora-guard-hub-2025 as bloom-sensor-x509
     Telemetry sent: Soil Moisture = 630, Status = healthy
     Telemetry sent: Soil Moisture = 615, Status = healthy
     ```

### Step 4: Test and Deploy the Azure Function

1. **Test Locally**:

   - Install Azure Functions Core Tools:

     ```bash
     npm install -g azure-functions-core-tools@4
     ```
   - Run the function:

     ```bash
     cd function
     func start
     ```
   - Send telemetry via the device code and check logs for actions like:

     ```
     Device: bloom-sensor-x509 | Moisture: 380 | Action: relay_on
     ```

2. **Deploy to Azure**:

   - In VS Code, right-click the `function` folder, select **Deploy to Function App**.
   - Create a new Function App (e.g., `flora-guard-function-2025`) in the `evergreen-rg` resource group.
   - After deployment, update the Function App settings in Azure Portal with `IotHubConnectionString`, `EventHubConnectionString`, and `EventHubName` from `local.settings.json`.

### Step 5: Watch Your Garden Thrive! 🌻

- The device simulates soil drying (moisture decreases by 5-20 every 5 seconds).
- When moisture drops below 400, the Azure Function triggers `relay_on`, and you’ll see:

  ```
  Water pump activated! Sprinkling life into the soil.
  ```
- Above 400, it triggers `relay_off`:

  ```
  Water pump stopped. Soil is resting.
  ```
- Check the CounterFit UI to see the relay state toggle and moisture values update.

## 

## 📚 Resources

- Microsoft IoT for Beginners
- CounterFit Documentation
- Azure IoT Hub Documentation
- Azure Functions Documentation

## 