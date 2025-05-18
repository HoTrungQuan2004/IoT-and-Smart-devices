from counterfit_connection import CounterFitConnection
import time
import counterfit_shims_serial # For the virtual serial port

# Initialize connection to the CounterFit app
CounterFitConnection.init('127.0.0.1', 5000)

# Connect to the virtual serial port used by the CounterFit GPS sensor
# This matches the port you configured in the CounterFit UI
try:
    serial = counterfit_shims_serial.Serial('/dev/ttyAMA0')
    print("Successfully connected to virtual GPS sensor on /dev/ttyAMA0")
except Exception as e:
    print(f"Error connecting to virtual GPS sensor: {e}")
    print("Ensure CounterFit is running and the UART GPS sensor is created on /dev/ttyAMA0.")
    exit()

def print_gps_data(line):
    """
    Prints the GPS data line after stripping trailing whitespace.
    """
    print(line.rstrip())

print("Reading data from virtual GPS sensor...")
try:
    while True:
        # Read a line of data from the serial port
        # The virtual GPS sensor sends NMEA sentences which are strings
        line_bytes = serial.readline()
        if line_bytes:
            try:
                line_str = line_bytes.decode('utf-8')
                # Process lines as long as they are not empty
                while len(line_str) > 0:
                    print_gps_data(line_str)
                    line_bytes = serial.readline() # Read next line
                    if not line_bytes: # Break if no more bytes
                        line_str = ""
                        break
                    line_str = line_bytes.decode('utf-8')
            except UnicodeDecodeError:
                print("Received non-UTF-8 data, skipping line.")
        time.sleep(1) # Wait for 1 second before reading again
except KeyboardInterrupt:
    print("\nStopping GPS data reading.")
finally:
    if 'serial' in locals() and serial.is_open:
        serial.close()
        print("Serial port closed.")
