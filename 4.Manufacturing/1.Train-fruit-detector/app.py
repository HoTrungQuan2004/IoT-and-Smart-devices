import numpy as np
import tensorflow as tf
import requests
from PIL import Image
import io
import time

# Load TensorFlow Lite model
interpreter = tf.lite.Interpreter(model_path="/workspaces/IoT-and-Smart-devices/4.Manufacturing/1.Train-fruit-detector/model.tflite")  
interpreter.allocate_tensors()

# Get input and output tensor information
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Input image size (usually 224x224 from Teachable Machine)
IMG_WIDTH, IMG_HEIGHT = 224, 224

# Read labels from file labels.txt
with open("labels.txt", "r") as f:
    labels = [line.strip() for line in f.readlines()]  # Example: ["Ripe", "Unripe"]

# Function to get image from CounterFit
def get_image_from_counterfit(port="sensor_1"):
    # Gọi endpoint đúng của CounterFit
    url = f"http://localhost:5000/binary_sensor_data?port={port}"
    response = requests.get(url)

    # Kiểm tra phản hồi
    content_type = response.headers.get("Content-Type", "")
    print("Status:", response.status_code, "| Content-Type:", content_type)

    if response.status_code != 200:
        raise ValueError(f"Failed to fetch image, status code: {response.status_code}")
    if "image" not in content_type:
        print("Không nhận được ảnh, đây là dữ liệu trả về:")
        print(response.text[:200])  # In thử 200 ký tự đầu
        raise ValueError(f"Response is not an image. Check if CounterFit is running and port '{port}' is configured with a camera sensor.")

    # Nếu là ảnh thì tiếp tục xử lý
    img = Image.open(io.BytesIO(response.content))
    img = img.resize((IMG_WIDTH, IMG_HEIGHT))
    img_array = np.array(img, dtype=np.float32) / 255.0
    return img_array


# Function to run inference
def run_inference(image):
    interpreter.set_tensor(input_details[0]['index'], image)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return output_data

# Save results for reporting
results = []

# Test with multiple images
for i in range(10):  # Check 10 photos
    img_array = get_image_from_counterfit()
    img_array = np.expand_dims(img_array, axis=0)  # add batch dimension
    output = run_inference(img_array)
    
    predicted_class = np.argmax(output[0])
    predicted_label = labels[predicted_class]
    scores = {labels[j]: output[0][j] for j in range(len(labels))}
    
    print(f"Image {i+1}: Predicted: {predicted_label}, Scores: {scores}")
    results.append({"image": i+1, "predicted": predicted_label, "scores": scores})
    
    time.sleep(1)  # Wait before taking next photo