import datetime
from shapely.geometry import shape, Point
import folium

# Step 3: Define the geofence
geofence_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {},
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [-122.42, 37.77],
                        [-122.41, 37.77],
                        [-122.41, 37.78],
                        [-122.42, 37.78],
                        [-122.42, 37.77]
                    ]
                ]
            }
        }
    ]
}
geofence = shape(geofence_geojson['features'][0]['geometry'])

# Step 4: Generate GPS data
start_time = datetime.datetime.now()
gps_data = [
    {"timestamp": start_time, "lat": 37.76, "lon": -122.43},
    {"timestamp": start_time + datetime.timedelta(minutes=1), "lat": 37.765, "lon": -122.425},
    {"timestamp": start_time + datetime.timedelta(minutes=2), "lat": 37.77, "lon": -122.42},
    {"timestamp": start_time + datetime.timedelta(minutes=3), "lat": 37.775, "lon": -122.415},
    {"timestamp": start_time + datetime.timedelta(minutes=4), "lat": 37.78, "lon": -122.41},
    {"timestamp": start_time + datetime.timedelta(minutes=5), "lat": 37.785, "lon": -122.405}
]

# Step 5: Geofencing logic
previous_state = 'outside'
for point in gps_data:
    gps_point = Point(point['lon'], point['lat'])
    if gps_point.within(geofence):
        current_state = 'inside'
    else:
        current_state = 'outside'
    if current_state != previous_state:
        if current_state == 'inside':
            print(f"Vehicle entered the geofence at {point['timestamp']}")
        else:
            print(f"Vehicle exited the geofence at {point['timestamp']}")
    previous_state = current_state

# Step 6: Visualization
map_center = [37.775, -122.415]
m = folium.Map(location=map_center, zoom_start=14)
folium.GeoJson(geofence_geojson, name="Geofence").add_to(m)
path = [(point['lat'], point['lon']) for point in gps_data]
folium.PolyLine(path, color='blue', weight=2.5, opacity=1).add_to(m)
for point in gps_data:
    loc = (point['lat'], point['lon'])
    gps_point = Point(point['lon'], point['lat'])
    color = 'green' if gps_point.within(geofence) else 'red'
    folium.Marker(
        location=loc,
        popup=f"Time: {point['timestamp']}\nState: {color}",
        icon=folium.Icon(color=color)
    ).add_to(m)
m.save('geofence_map.html')