from flask import Flask, request, jsonify
import re

app = Flask(__name__)

def parse_duration(text):
    """
    Parses duration from text like "X minutes Y seconds".
    Returns total seconds and a descriptive string.
    """
    minutes = 0
    seconds = 0
    duration_text_parts = []

    minute_match = re.search(r'(\d+)\s*(minute|minutes|min)', text, re.IGNORECASE)
    if minute_match:
        minutes = int(minute_match.group(1))
        duration_text_parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")

    second_match = re.search(r'(\d+)\s*(second|seconds|sec)', text, re.IGNORECASE)
    if second_match:
        seconds = int(second_match.group(1))
        duration_text_parts.append(f"{seconds} second{'s' if seconds > 1 else ''}")
    
    if not duration_text_parts and re.search(r'\d+', text): # fallback for just numbers
        num_match = re.search(r'(\d+)', text)
        if num_match:
            # try to guess if it's seconds or minutes based on context (e.g. "timer for 5")
            # for simplicity, assume seconds if no unit, or if it's a small number
            # this part can be made more sophisticated
            val = int(num_match.group(1))
            if "minute" in text.lower() or (val <= 10 and not "second" in text.lower()): # guess minutes for small numbers if "minute" is nearby or no unit
                 minutes = val
                 duration_text_parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
            else: # default to seconds
                 seconds = val
                 duration_text_parts.append(f"{seconds} second{'s' if seconds > 1 else ''}")


    total_seconds = (minutes * 60) + seconds
    duration_text = " and ".join(duration_text_parts) if duration_text_parts else ""
    
    return total_seconds, duration_text

@app.route('/luis_parse', methods=['POST'])
def luis_parse():
    data = request.get_json()
    text = data.get('text', '').lower()

    print(f"LUIS Sim: Received text: '{text}'")

    if 'cancel' in text and 'timer' in text or 'stop' in text and 'timer' in text:
        print("LUIS Sim: Detected CancelTimer intent")
        return jsonify({'intent': 'CancelTimer', 'entities': {}})
    
    # More specific keywords for setting a timer
    set_timer_keywords = ['set timer', 'start timer', 'timer for', 'create timer']
    if any(keyword in text for keyword in set_timer_keywords):
        total_seconds, duration_text = parse_duration(text)
        if total_seconds > 0:
            print(f"LUIS Sim: Detected SetTimer intent. Duration: {total_seconds}s, Text: '{duration_text}'")
            # Matching the 'seconds' field from your example files
            return jsonify({
                'intent': 'SetTimer',
                'seconds': total_seconds, # For compatibility with get_timer_time
                'entities': {
                    'duration_seconds': total_seconds,
                    'duration_text': duration_text or f"{total_seconds} seconds"
                }
            })

    print("LUIS Sim: Detected None intent")
    return jsonify({'intent': 'None', 'entities': {}})

if __name__ == '__main__':
    # Makes it listen on all available network interfaces
    # and on port 5000 by default.
    app.run(host='0.0.0.0', port=5000, debug=True)