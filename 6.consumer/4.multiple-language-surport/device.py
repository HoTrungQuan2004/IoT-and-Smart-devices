import requests
import time
import threading
import argparse
from googletrans import Translator

# The address of the central message hub
HUB_URL = "http://127.0.0.1:5000"

def poll_for_messages(device_id, my_lang):
    """
    Runs in a background thread to continuously check for new messages from the hub.
    """
    translator = Translator()
    while True:
        try:
            # Ask the hub for any messages waiting for me
            response = requests.get(f"{HUB_URL}/receive/{device_id}")
            if response.status_code == 200:
                messages = response.json()
                if messages:
                    for msg in messages:
                        source_lang = msg['source_lang']
                        original_text = msg['text']
                        
                        # Translate the received text to this device's language
                        translated = translator.translate(original_text, src=source_lang, dest=my_lang)
                        
                        print(f"\n\n--- Incoming Message ---")
                        print(f"From ({source_lang}): {original_text}")
                        print(f"Translated to ({my_lang}): {translated.text}")
                        print("------------------------")
                        print("Enter text to send: ", end="", flush=True)

        except requests.exceptions.ConnectionError:
            # Hub is not running, just wait and try again
            pass
        except Exception as e:
            print(f"\nAn error occurred: {e}")

        # Wait for 3 seconds before polling again
        time.sleep(3)

def run_device(device_id, my_lang, target_lang, target_device_id):
    """
    Main function to run the device client.
    """
    print("-------------------------------------------------")
    print(f"  Universal Translator Device: {device_id.upper()}")
    print(f"  My Language: {my_lang}")
    print(f"  Translating to: {target_lang} for {target_device_id.upper()}")
    print("-------------------------------------------------")
    print("Enter text to send (or 'quit' to exit):")

    # Start the background thread to listen for messages
    polling_thread = threading.Thread(target=poll_for_messages, args=(device_id, my_lang), daemon=True)
    polling_thread.start()

    # Loop to get user input and send it to the other device
    while True:
        text_to_send = input("Enter text to send: ")
        if text_to_send.lower() == 'quit':
            print(f"Shutting down {device_id}...")
            break
        
        if text_to_send:
            payload = {
                "source_device_id": device_id,
                "target_device_id": target_device_id,
                "text": text_to_send,
                "source_lang": my_lang
            }
            try:
                requests.post(f"{HUB_URL}/send", json=payload)
                print("...message sent!")
            except requests.exceptions.ConnectionError:
                print("...failed to send. Is the hub running?")
            except Exception as e:
                print(f"...failed to send. Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run a virtual translator device.")
    parser.add_argument("--id", required=True, help="The ID for this device (e.g., 'device1').")
    parser.add_argument("--lang", required=True, help="The language for this device (e.g., 'en').")
    parser.add_argument("--target-lang", required=True, help="The language to translate to (e.g., 'fr').")
    parser.add_argument("--target-id", required=True, help="The ID of the target device (e.g., 'device2').")

    args = parser.parse_args()

    run_device(args.id, args.lang, args.target_lang, args.target_id)