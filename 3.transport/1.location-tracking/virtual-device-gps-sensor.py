from counterfit_connection import CounterFitConnection
import time
import counterfit_shims_serial
import pynmea2 # Import the pynmea2 library

# Initialize connection to CounterFit
CounterFitConnection.init('127.0.0.1', 5000)

# Connect to the virtual serial port used by the CounterFit GPS
try:
    serial = counterfit_shims_serial.Serial('/dev/ttyAMA0')
except Exception as e:
    print(f"Error opening serial port: {e}")
    print("Make sure the GPS UART sensor is created in CounterFit on /dev/ttyAMA0.")
    exit()

def process_gps_data(line):
    """
    Parses an NMEA sentence and prints relevant GPS data if it's a GGA message.
    """
    try:
        # Parse the NMEA sentence
        msg = pynmea2.parse(line)

        # Check if the message is a GGA message
        if isinstance(msg, pynmea2.types.talker.GGA):
            # Extract latitude, longitude, and number of satellites
            # pynmea2.dm_to_sd converts from degrees, minutes to signed decimal degrees
            lat = msg.latitude
            lon = msg.longitude
            
            # Handle N/S and E/W indicators explicitly for clarity, though pynmea2 often provides signed values directly
            # For pynmea2, latitude is positive for North, negative for South.
            # Longitude is positive for East, negative for West.

            num_sats = msg.num_sats
            gps_qual = msg.gps_qual # GPS Quality indicator

            print(f"Raw GGA: {line.strip()}")
            print(f"Timestamp: {msg.timestamp}")
            print(f"Latitude: {lat:.6f} {msg.lat_dir}")
            print(f"Longitude: {lon:.6f} {msg.lon_dir}")
            print(f"Number of Satellites: {num_sats}")
            print(f"GPS Quality Indicator: {gps_qual}") # 0: Fix not available, 1: GPS SPS Mode, 2: Diff GPS, ...
            
            # Altitude can also be extracted
            if msg.altitude is not None:
                print(f"Altitude: {msg.altitude} {msg.altitude_units}")
            print("-" * 30)

    except pynmea2.ParseError as e:
        # This will catch lines that are not valid NMEA sentences or are corrupted
        # print(f"Could not parse NMEA sentence: {line.strip()} - Error: {e}")
        # It's common for GPS modules to output other sentence types or empty lines,
        # so you might want to silently ignore parse errors for non-GGA sentences.
        if line.startswith('$GNGGA') or line.startswith('$GPGGA'): # Only print error if it was likely a GGA sentence
             print(f"Could not parse GGA sentence: {line.strip()} - Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred while processing line: {line.strip()} - Error: {e}")

print("Starting GPS data reader...")
print("Ensure the CounterFit app is running and the UART GPS sensor is configured and sending data.")

try:
    while True:
        # Read a line from the serial port
        # The decode('utf-8', errors='ignore') will help prevent crashes on weird bytes
        line = serial.readline().decode('utf-8', errors='ignore')

        # If a line is received, process it
        if line and line.strip(): # Ensure line is not empty or just whitespace
            # The raw NMEA sentences usually start with '$'
            if line.startswith('$'):
                process_gps_data(line)
            else:
                # Sometimes other non-NMEA debug messages might appear
                print(f"Received non-NMEA data or empty line: {line.strip()}")
        
        # A small delay to prevent a tight loop if readline is non-blocking and returns empty quickly
        # However, serial.readline() is typically blocking, so this might not be strictly necessary
        # if the GPS sends data periodically (e.g., every second)..
        # If readline() is blocking, the loop will pause there until data arrives.
        # If it's non-blocking and data is sparse, this time.sleep might be too long.
        time.sleep(0.1) # Short sleep to yield control, adjust as needed

except KeyboardInterrupt:
    print("\nExiting GPS reader.")
except Exception as e:
    print(f"An error occurred in the main loop: {e}")
finally:
    if 'serial' in locals() and serial.is_open:
        serial.close()
        print("Serial port closed.")
