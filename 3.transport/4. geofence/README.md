# IoT Geofence Notification Project

This project demonstrates a simple IoT geofencing system that sends email notifications when a virtual GPS device enters a predefined geographical area (geofence). It's designed to uses an MQTT broker for communication.

## Features

* **Virtual GPS Device:** Simulates GPS data transmission.
* **MQTT Communication:** Uses a local Mosquitto MQTT broker for message passing between the device and the monitor.
* **Geofence Logic:** Implements point-in-polygon checks using the `shapely` Python library.
* **Email Notifications:** Sends alerts via SendGrid when a device enters the geofence.
* **Codespaces Ready:** Designed to be easily set up and run in GitHub Codespaces.
* **Environment Variable Management:** Uses a `.env` file for secure handling of API keys and sensitive configuration.
## Prerequisites

* A [SendGrid](https://sendgrid.com) account:
    * Sign up for a free tier.
    * Create an API Key (save this securely).
    * Verify a Single Sender email address.


## Setup Instructions


### 1. Install Dependencies

```bash
sudo apt-get update && sudo apt-get install -y mosquitto mosquitto-clients
pip install paho-mqtt shapely sendgrid python-dotenv


3. Configure Environment Variables
This project uses a .env file to store sensitive information like your SendGrid API key and email addresses.



Add your credentials to .env:
Open the .env file and add your SendGrid details:

Code snippet

# .env
SENDGRID_API_KEY="YOUR_ACTUAL_SENDGRID_API_KEY"
SENDER_EMAIL="your_verified_sendgrid_sender_email@example.com"
RECEIVER_EMAIL="your_notification_receiver_email@example.com"
Replace "YOUR_ACTUAL_SENDGRID_API_KEY" with the API key you generated from SendGrid.
Replace "your_verified_sendgrid_sender_email@example.com" with the email address you verified as a sender in SendGrid.
Replace "your_notification_receiver_email@example.com" with the email address where you want to receive the geofence alerts.
Ensure .env is in .gitignore:
The .gitignore file should already include .env to prevent your secret credentials from being committed to version control. If not, add .env to your .gitignore file.

4. Define Your Geofence (Optional Modification)
The geofence is defined as a list of coordinates directly within the geofence_monitor.py script (variable GEOFENCE_POLYGON_COORDS). You can modify these coordinates to define a different area. The coordinates should be in (longitude, latitude) format.
Example default:

Python

# GEOFENCE_POLYGON_COORDS in geofence_monitor.py
[
    (-73.988429, 40.748817),
    (-73.981369, 40.748817),
    (-73.981369, 40.752817),
    (-73.988429, 40.752817),
    (-73.988429, 40.748817)
]
How to Run the Project
You will need three separate terminals in your GitHub Codespaces environment.

Terminal 1: Start the Mosquitto MQTT Broker
Bash

mosquitto -v
This will start the MQTT broker. Keep this terminal open and running. The -v flag provides verbose output.

Terminal 2: Run the Geofence Monitor Application
Bash

python geofence_monitor.py
This script will:

Connect to the MQTT broker.
Subscribe to the GPS data topic.
Listen for incoming GPS coordinates.
Check if coordinates are inside the defined geofence.
Send an email notification via SendGrid if a device enters the geofence (respecting a cooldown period).
Terminal 3: Run the Virtual GPS Device Simulator
Bash

python virtual_gps_device.py
This script will:

Connect to the MQTT broker.
Periodically publish sample GPS coordinates (some inside, some outside the geofence) to the MQTT topic.
Expected Outcome
The Virtual GPS Device terminal will show logs of data being sent.
The Mosquitto Broker terminal will show client connections and message traffic (if verbose).
The Geofence Monitor terminal will log:
Received GPS messages.
Whether each point is INSIDE or OUTSIDE the geofence.
Confirmation when an email notification is sent.
You should receive email notifications at your configured RECEIVER_EMAIL address when the simulated device's coordinates fall inside the geofence. (Check your spam/junk folder if emails don't appear in your inbox.)
Troubleshooting
No connection to MQTT Broker: Ensure mosquitto -v is running in a separate terminal and there are no errors. Check that MQTT_BROKER_HOST is localhost in both Python scripts.
Python script errors: Check the terminal output for any Python errors. Ensure all dependencies are installed correctly.
Environment variables not found: Double-check that your .env file is correctly named, in the root directory, and contains the correct variable names (SENDGRID_API_KEY, SENDER_EMAIL, RECEIVER_EMAIL). Ensure load_dotenv() is called in geofence_monitor.py.
Emails not sending:
Verify your SENDGRID_API_KEY is correct and has permissions to send emails.
Ensure your SENDER_EMAIL is verified in SendGrid.
Check the output of geofence_monitor.py for any errors from the SendGrid API.
Check your SendGrid dashboard for any API activity or errors.
Incorrect geofence behavior: Double-check the GEOFENCE_POLYGON_COORDS in geofence_monitor.py and the sample GPS coordinates in virtual_gps_device.py. Remember that shapely expects points as (longitude, latitude).



