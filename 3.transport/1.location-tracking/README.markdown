```markdown
# Vehicle Location Tracking with Counterfit


## Overview

The assignment simulates a GPS sensor on a virtual IoT device to track a moving vehicle's location, such as a delivery truck. The solution includes:
- A Python script (`decode.py`) to read and parse GPS data from a virtual UART GPS sensor in Counterfit.
- An optional script (`virtual-device-gps-sensor.py`) to automate location updates, simulating vehicle movement.
- Setup instructions for a Python virtual environment and Counterfit.

The project outputs latitude and longitude coordinates periodically, demonstrating how IoT devices can monitor vehicle locations for logistics.

## Setup Instructions


### Step 1: Set Up a Python Virtual Environment
1. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   ```
2. Activate it:
   - **Windows**:
     ```bash
     .venv\Scripts\activate.bat
     ```
   - **macOS/Linux**:
     ```bash
     source ./.venv/bin/activate
     ```
3. Verify activation (prompt should show `(.venv)`):
   ```bash
   python --version
   ```
   Expected output: `Python 3.9.1` (or similar).

### Step 2: Install Counterfit Packages
1. With the virtual environment activated, install the required pip packages:
   ```bash
   pip install CounterFit counterfit-connection counterfit-shims-grove counterfit-shims-serial
   ```
2. Verify installation:
   ```bash
   pip list
   ```
   Ensure `CounterFit`, `counterfit-connection`, `counterfit-shims-grove`, and `counterfit-shims-serial` are listed.

### Step 3: Launch Counterfit
1. In the terminal, run:
   ```bash
   CounterFit
   ```
2. Open a web browser and go to `http://localhost:5000`.
3. Verify the Counterfit interface loads, showing a "Disconnected" status.

### Step 4: Configure the Virtual GPS Sensor
1. In the Counterfit web app, go to the "Sensors" pane.
2. In "Create sensor":
   - Set "Sensor type" to "UART GPS".
   - Keep "Port" as `/dev/ttyAMA0`.
   - Click "Add".
3. Configure the sensor:
   - Set "Source" to "Lat/Lon".
   - Enter initial coordinates: Latitude `51.5074`, Longitude `-0.1278` (near London).
   - Set "Satellites" to `3`.
   - Check "Repeat" to send data every second.
   - Click "Set".

## Project Structure

- `decode.py`: Reads and parses GPS data from the virtual sensor, printing latitude and longitude.
- `virtual-device-gps-sensor.py` : Automates location updates to simulate vehicle movement.



## Overview

The assignment simulates a GPS sensor on a virtual IoT device to track a moving vehicle's location, such as a delivery truck. The solution includes:
- A Python script (`app.py`) to read and parse GPS data from a virtual UART GPS sensor in Counterfit.
- An optional script (`gps_simulator.py`) to automate location updates, simulating vehicle movement.
- Setup instructions for a Python virtual environment and Counterfit.

The project outputs latitude and longitude coordinates periodically, demonstrating how IoT devices can monitor vehicle locations for logistics.

## Prerequisites

- **Python 3.6 or higher**: Download from [python.org](https://www.python.org/downloads/).
- **Visual Studio Code (VS Code)**: Install from [code.visualstudio.com](https://code.visualstudio.com).
- **VS Code Pylance Extension**: Install via the VS Code Extensions marketplace.
- A terminal (Command Prompt on Windows, Terminal on macOS/Linux).
- Internet access for installing pip packages.

## Setup Instructions

Follow these steps to set up the project environment and Counterfit.

### Step 1: Install Python and VS Code
1. **Install Python**:
   - Download and install Python 3.6+ from [python.org](https://www.python.org/downloads/).
   - On Windows, check "Add Python to PATH" during installation.
   - Verify with:
     ```bash
     python3 --version
     ```
     Expected output: `Python 3.9.1` (or similar).
2. **Install VS Code**:
   - Download from [code.visualstudio.com](https://code.visualstudio.com).
   - On macOS, add VS Code to your PATH (see [VS Code documentation](https://code.visualstudio.com/docs/setup/mac#_launching-from-the-command-line)).
3. **Install Pylance**:
   - In VS Code, go to Extensions (Ctrl+Shift+X or Cmd+Shift+X), search for "Pylance," and install.

### Step 2: Create the Project Directory
1. Open a terminal.
2. Create and navigate to a project folder:
   ```bash
   mkdir location-tracking
   cd location-tracking
   ```

### Step 3: Set Up a Python Virtual Environment
1. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   ```
2. Activate it:
   - **Windows**:
     ```bash
     .venv\Scripts\activate.bat
     ```
   - **macOS/Linux**:
     ```bash
     source ./.venv/bin/activate
     ```
3. Verify activation (prompt should show `(.venv)`):
   ```bash
   python --version
   ```
   Expected output: `Python 3.9.1` (or similar).

### Step 4: Install Counterfit Packages
1. With the virtual environment activated, install the required pip packages:
   ```bash
   pip install CounterFit counterfit-connection counterfit-shims-grove counterfit-shims-serial
   ```
2. Verify installation:
   ```bash
   pip list
   ```
   Ensure `CounterFit`, `counterfit-connection`, `counterfit-shims-grove`, and `counterfit-shims-serial` are listed.

### Step 5: Launch Counterfit
1. In the terminal, run:
   ```bash
   CounterFit
   ```
2. Open a web browser and go to `http://localhost:5000`.
3. Verify the Counterfit interface loads, showing a "Disconnected" status.

### Step 6: Configure the Virtual GPS Sensor
1. In the Counterfit web app, go to the "Sensors" pane.
2. In "Create sensor":
   - Set "Sensor type" to "UART GPS".
   - Keep "Port" as `/dev/ttyAMA0`.
   - Click "Add".
3. Configure the sensor:
   - Set "Source" to "Lat/Lon".
   - Enter initial coordinates: Latitude `51.5074`, Longitude `-0.1278` (near London).
   - Set "Satellites" to `3`.
   - Check "Repeat" to send data every second.
   - Click "Set".

## Project Structure

- `app.py`: Reads and parses GPS data from the virtual sensor, printing latitude and longitude.
- `gps_simulator.py` (optional): Automates location updates to simulate vehicle movement.

```