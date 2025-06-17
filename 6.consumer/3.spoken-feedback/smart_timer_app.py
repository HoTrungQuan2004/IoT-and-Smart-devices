import requests
import threading
import time

# --- Virtual IoT Device Logic ---
active_timer_thread = None
timer_lock = threading.Lock() # To safely access active_timer_thread

def announce_timer_expired(duration_text):
    """Called when the timer finishes."""
    print(f"\n📢 Time's up on your {duration_text} timer!\n")

def start_timer_on_device(total_seconds, duration_text):
    """Starts a new timer on the 'device'."""
    global active_timer_thread
    with timer_lock:
        if active_timer_thread and active_timer_thread.is_alive():
            print("Virtual IoT Device: Cancelling existing timer before starting a new one.")
            active_timer_thread.cancel()
        
        print(f"Virtual IoT Device: Starting a new timer for {duration_text} ({total_seconds} seconds).")
        active_timer_thread = threading.Timer(total_seconds, announce_timer_expired, args=[duration_text])
        active_timer_thread.start()
        print(f"Timer for {duration_text} started.")

def cancel_timer_on_device():
    """Cancels the current active timer on the 'device'."""
    global active_timer_thread
    with timer_lock:
        if active_timer_thread and active_timer_thread.is_alive():
            active_timer_thread.cancel()
            active_timer_thread = None # Clear the reference
            print("Virtual IoT Device: Timer cancelled successfully.")
        else:
            print("Virtual IoT Device: No active timer to cancel.")
# --- End of Virtual IoT Device Logic ---


# --- Main Controller Logic ---
LUIS_SIMULATOR_URL = 'http://127.0.0.1:5000/luis_parse' # Ensure this matches your LUIS simulator address

def get_intent_from_luis(text):
    """Sends text to the LUIS simulator and gets the intent."""
    try:
        response = requests.post(LUIS_SIMULATOR_URL, json={'text': text})
        response.raise_for_status() # Raise an exception for bad status codes
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error connecting to LUIS Simulator: {e}")
        return {'intent': 'Error', 'entities': {}}

def main():
    print("Smart Timer App started. Type 'exit' to quit.")
    while True:
        try:
            user_input = input("Set Timmer: > ")
            if user_input.lower() == 'exit':
                print("Exiting Smart Timer App...")
                with timer_lock: # Ensure cleanup before exiting
                    if active_timer_thread and active_timer_thread.is_alive():
                        active_timer_thread.cancel()
                break

            if not user_input.strip():
                continue

            luis_response = get_intent_from_luis(user_input)
            intent = luis_response.get('intent')
            
            print(f"Controller: Received LUIS response: {luis_response}")


            if intent == 'SetTimer':
                # Use 'seconds' field for compatibility with your original snippets if available
                duration_seconds = luis_response.get('seconds') 
                if duration_seconds is None: # Fallback to entities
                    duration_seconds = luis_response.get('entities', {}).get('duration_seconds')

                duration_text = luis_response.get('entities', {}).get('duration_text')

                if duration_seconds and duration_seconds > 0:
                    effective_duration_text = duration_text or f"{duration_seconds} seconds"
                    start_timer_on_device(duration_seconds, effective_duration_text)
                else:
                    print("Controller: Could not determine timer duration from your command.")
            
            elif intent == 'CancelTimer':
                cancel_timer_on_device()
            
            elif intent == 'Error':
                print("Controller: Could not process command due to an error with LUIS service.")

            else: # None or other intents
                print("Controller: Sorry, I didn't understand that. Try 'set timer for 5 seconds' or 'cancel timer'.")
        
        except KeyboardInterrupt:
            print("\nExiting Smart Timer App due to KeyboardInterrupt...")
            with timer_lock:
                if active_timer_thread and active_timer_thread.is_alive():
                    active_timer_thread.cancel()
            break
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

if __name__ == '__main__':
    main()