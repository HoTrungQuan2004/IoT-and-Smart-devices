from counterfit_connection import CounterFitConnection
import time
import counterfit_shims_serial
import pynmea2 # Import the pynmea2 library

# Initialize connection to the CounterFit app
CounterFitConnection.init('127.0.0.1', 5000)

try:
    serial = counterfit_shims_serial.Serial('/dev/ttyAMA0')
    print("Successfully connected to virtual GPS sensor on /dev/ttyAMA0")
except Exception as e:
    print(f"Error connecting to virtual GPS sensor: {e}")
    print("Ensure CounterFit is running and the UART GPS sensor is created on /dev/ttyAMA0.")
    exit()

print("Reading and decoding data from virtual GPS sensor...")
try:
    while True:
        line_bytes = serial.readline()
        if line_bytes:
            try:
                line_str = line_bytes.decode('utf-8').strip()
                if line_str.startswith('$'): # Check if it looks like an NMEA sentence
                    try:
                        msg = pynmea2.parse(line_str)
                        # Now you can access specific data fields
                        if hasattr(msg, 'latitude') and hasattr(msg, 'longitude'):
                            print(f"Time: {getattr(msg, 'timestamp', 'N/A')}, Lat: {msg.latitude:.6f} {msg.lat_dir}, Lon: {msg.longitude:.6f} {msg.lon_dir}, Altitude: {getattr(msg, 'altitude', 'N/A')} {getattr(msg, 'altitude_units', '')}")
                        elif isinstance(msg, pynmea2.types.talker.RMC): # Example for RMC
                             print(f"RMC - Time: {msg.timestamp}, Status: {msg.status}, Lat: {msg.latitude:.6f} {msg.lat_dir}, Lon: {msg.longitude:.6f} {msg.lon_dir}, Speed: {msg.spd_over_grnd}, Date: {msg.datestamp}")
                        else:
                            print(f"Decoded NMEA: {msg}")
                    except pynmea2.ParseError as e:
                        print(f"Could not parse NMEA sentence: {line_str} - Error: {e}")
                    except Exception as e: # Catch other potential errors during processing
                        print(f"Error processing message {line_str}: {e}")
            except UnicodeDecodeError:
                print("Received non-UTF-8 data, skipping line.")
        time.sleep(0.1) # You might want a shorter sleep if NMEA sentences come quickly
except KeyboardInterrupt:
    print("\nStopping GPS data reading and decoding.")
finally:
    if 'serial' in locals() and serial.is_open:
        serial.close()
        print("Serial port closed.")
