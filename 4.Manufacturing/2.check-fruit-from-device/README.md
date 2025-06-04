

---

## Setup and Installation

### 1. Train Your Teachable Machine Model

1. Go to [Teachable Machine](https://teachablemachine.withgoogle.com/).
2. Create a new **Image Project** → **Standard image model**.
3. Add classes for your fruit types (e.g., `ripe`, `unripe`, `rotten`).
4. Upload diverse images for each class.
5. Click **Train Model**.
6. Once trained, click **Export Model**.
7. Select the **TensorFlow.js** tab.
8. Choose **Upload my model to the cloud** and click **Upload my model**.
9. Copy the generated API URL (e.g., `https://teachablemachine.withgoogle.com/models/YOUR_MODEL_ID/`).  
   _You’ll need this URL for `virtual_device_app.py`._

---

### 2. Configure Adafruit IO

1. Go to [Adafruit IO](https://io.adafruit.com/) and create an account.
2. Click **AIO Key** (top right) to get your Username and Active Key.  
   _Keep these secure!_
3. Navigate to **Feeds** → **View All Feeds** → **New Feed**.
4. Create two feeds:
    - `fruit-status` (for classification results)
    - `actuator-command` (for actuator commands)
5. (Optional) Create a dashboard and add blocks to visualize your feeds.

---

### 3. Install CounterFit and Dependencies

**Prerequisites:**  
- Python 3.11 (recommended for compatibility)

**Install CounterFit and PiCamera shim:**
```bash
pip install counterfit
pip install counterfit-shims-picamera
```

**Install dependencies for the virtual device and web server:**
```bash

cd virtual-device
pip install -r requirements.txt  # (should include paho-mqtt, requests)





---

### 4. Set Environment Variables



```smd
set ADAFRUIT_IO_USERNAME=your_adafruit_io_username
set ADAFRUIT_IO_KEY=your_adafruit_io_active_key
```

---

## How to Run

You will need **three terminal windows** open:

### 1. Start CounterFit Server
```bash
counterfit
```
_This starts the virtual device server (usually at http://localhost:5000)._

### 2. Run Flask
```bash
cd web-server
python app.py
```
_This connects to Adafruit IO and processes fruit status updates._

### 3. Run Virtual Device

- Open `virtual-device/app.py` and replace `"YOUR_TEACHABLE_MACHINE_MODEL_URL_HERE"` with your actual API URL.
- Then run:
```bash
cd virtual-device
python app.py
```
_This simulates your IoT device, sending images for classification and publishing results._

---

## How It Works

1. **Image Capture:**  
   The virtual device "captures" an image (`fruit_image.jpg`).

2. **Image Classification:**  
   The image is sent to your Teachable Machine model for prediction.

3. **Status Publication:**  
   The device publishes the classification (e.g., `ripe`) to the `fruit-status` feed on Adafruit IO.

4. **Logic Processing:**  
   The server listens for updates and decides what command to send (e.g., turn on/off LED).

5. **Command Publication:**  
   The server publishes actuator commands to the `actuator-command` feed.

6. **Actuator Control:**  
   The virtual device receives commands and simulates actuator actions.

---

## Simulating Different Fruit States

- Prepare sample images (e.g., `ripe_sample.jpg`, `unripe_sample.jpg`, `rotten_sample.jpg`).
- To simulate a state, replace `fruit_image.jpg` in `virtual-device/` with your sample image before the next classification cycle.

---

## Notes

- Make sure you are using Python 3.11 for compatibility with CounterFit and Eventlet.
- If you encounter issues with dependencies, check your Python version and installed packages.
