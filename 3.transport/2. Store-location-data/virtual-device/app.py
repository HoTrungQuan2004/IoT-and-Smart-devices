import time
import json
from counterfit_connection import CounterFitConnection
from counterfit_shims_grove.grove_gps_sensor import GroveGPSSensor
from Adafruit_IO import Client, RequestError, Feed

# Khởi tạo kết nối với CounterFit
CounterFitConnection.init('127.0.0.1', 5000)

# Khởi tạo GPS sensor
gps = GroveGPSSensor(0)

# Cấu hình Adafruit IO
ADAFRUIT_IO_USERNAME = 'YOUR_ADAFRUIT_IO_USERNAME'  # Thay bằng username của bạn
ADAFRUIT_IO_KEY = 'YOUR_ADAFRUIT_IO_KEY'  # Thay bằng AIO Key của bạn
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

# Tạo hoặc lấy feed
try:
    latitude_feed = aio.feeds('latitude')
except RequestError:  # Nếu feed chưa tồn tại, tạo mới
    latitude_feed = Feed(name='latitude')
    latitude_feed = aio.create_feed(latitude_feed)

try:
    longitude_feed = aio.feeds('longitude')
except RequestError:
    longitude_feed = Feed(name='longitude')
    longitude_feed = aio.create_feed(longitude_feed)

print('Connected to Adafruit IO')

while True:
    # Lấy dữ liệu GPS từ sensor giả lập
    lat, long = gps.location
    
    # In dữ liệu để kiểm tra
    print(f'Latitude: {lat}, Longitude: {long}')
    
    # Gửi dữ liệu đến Adafruit IO
    try:
        aio.send_data(latitude_feed.key, lat)
        aio.send_data(longitude_feed.key, long)
        print('Data sent to Adafruit IO')
    except Exception as e:
        print(f'Error sending data: {e}')
    
    # Đợi 10 giây trước khi gửi dữ liệu tiếp theo
    time.sleep(10)
