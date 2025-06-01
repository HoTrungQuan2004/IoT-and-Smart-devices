import numpy as np
import tensorflow as tf
import requests
from PIL import Image
import io
import time
import base64
import json
import argparse

# Adafruit IO configuration
AIO_USERNAME = "YourAdafruitIOUsername"  # Replace with your actual Adafruit IO username
AIO_KEY = "YourAdafruitIOKey"  # Replace with your actual Adafruit IO key
FEED_NAME = "YourFeedName"  # Replace with your actual feed name

# ─────────────────────────────────────────────────────────────
# Argument parsing
parser = argparse.ArgumentParser(description="Run fruit detector continuously")
parser.add_argument('--sensor', type=str, default='sensor_1', help='Sensor name from CounterFit (default: sensor_1)')
args = parser.parse_args()
sensor_port = args.sensor

# ─────────────────────────────────────────────────────────────
# Load TensorFlow Lite model
model_path = "model.tflite"
interpreter = tf.lite.Interpreter(model_path=model_path)
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

IMG_WIDTH, IMG_HEIGHT = input_details[0]['shape'][2], input_details[0]['shape'][1]

# ─────────────────────────────────────────────────────────────
# Load labels
with open("labels.txt", "r") as f:
    labels = [line.strip() for line in f.readlines()]

# ─────────────────────────────────────────────────────────────
def get_image_from_counterfit(port="sensor_1"):
    url = f"http://localhost:5000/binary_sensor_data?port={port}"
    response = requests.get(url)
    content_type = response.headers.get("Content-Type", "")

    if response.status_code != 200:
        return None

    if "image" in content_type:
        img = Image.open(io.BytesIO(response.content))
    else:
        try:
            data = response.json()
            base64_str = data.get("value", "")
            if not base64_str:
                return None
            img_bytes = base64.b64decode(base64_str)
            img = Image.open(io.BytesIO(img_bytes))
        except Exception:
            return None

    img = img.resize((IMG_WIDTH, IMG_HEIGHT))

    if input_details[0]['dtype'] == np.uint8:
        img_array = np.array(img, dtype=np.uint8)
    else:
        img_array = np.array(img, dtype=np.float32) / 255.0

    return img_array
# ─────────────────────────────────────────────────────────────
def send_to_adafruit(label, scores):
    url = f"https://io.adafruit.com/api/v2/{AIO_USERNAME}/feeds/{FEED_NAME}/data"
    headers = {
        "X-AIO-Key": AIO_KEY,
        "Content-Type": "application/json"
    }
    payload = {
        "value": json.dumps({"label": label, "scores": scores})
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        if response.status_code == 200 or response.status_code == 201:
            print(f"     ☁️  Sent to Adafruit IO: {label}")
        else:
            print(f"     ⚠️  Failed to send to Adafruit: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"     ❌  Error sending to Adafruit: {e}")

# ─────────────────────────────────────────────────────────────
def run_inference(image):
    interpreter.set_tensor(input_details[0]['index'], image)
    interpreter.invoke()
    return interpreter.get_tensor(output_details[0]['index'])

# ─────────────────────────────────────────────────────────────
# Main loop: runs continuously
print("\n🚀 Running fruit detection model continuously...")
print("❗ Press Ctrl+C to stop.\n")

previous_image = None

try:
    while True:
        img_array = get_image_from_counterfit(sensor_port)

        if img_array is None:
            time.sleep(1)
            continue

        if previous_image is not None and np.array_equal(img_array, previous_image):
            time.sleep(1)
            continue  # skip identical images

        previous_image = img_array.copy()

        img_array = np.expand_dims(img_array, axis=0)
        output = run_inference(img_array)

        predicted_class = np.argmax(output[0])
        predicted_label = labels[predicted_class]
        scores = {labels[j]: round(float(output[0][j]), 4) for j in range(len(labels))}

        print("🖼️  New image received:")
        print(f"     ✅ Predicted: \033[1;32m{predicted_label}\033[0m")
        print(f"     📊 Scores: {json.dumps(scores)}")
        print("─────────────────────────────────────────────")
        send_to_adafruit(predicted_label, scores)

        time.sleep(1)

except KeyboardInterrupt:
    print("\n👋 Program stopped by user request.")
