from flask import Flask, request, jsonify

# Initialize the Flask application
app = Flask(__name__)

# In-memory storage for messages
# A real-world application would use a database or a message queue.
messages = {
    "device1": [],
    "device2": []
}

@app.route('/send', methods=['POST'])
def send_message():
    """
    Receives a message from a device and stores it for the target device.
    Expects JSON payload with:
    - text: The message content
    - source_lang: The language of the message
    - target_device_id: The ID of the recipient device ('device1' or 'device2')
    """
    data = request.get_json()
    if not all(k in data for k in ['text', 'source_lang', 'target_device_id']):
        return jsonify({"error": "Missing data"}), 400

    target_device = data['target_device_id']
    if target_device not in messages:
        return jsonify({"error": "Invalid target device ID"}), 400

    message = {
        "text": data['text'],
        "source_lang": data['source_lang']
    }
    
    messages[target_device].append(message)
    print(f"Message from {data.get('source_device_id', 'unknown')} for {target_device}: {data['text']}")
    
    return jsonify({"status": "message sent"}), 200

@app.route('/receive/<device_id>', methods=['GET'])
def receive_messages(device_id):
    """
    A device polls this endpoint to get its pending messages.
    """
    if device_id not in messages:
        return jsonify({"error": "Invalid device ID"}), 400

    # Get pending messages for the device and clear the queue
    pending_messages = messages[device_id]
    messages[device_id] = []
    
    return jsonify(pending_messages)

if __name__ == '__main__':
    # Run the hub on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)