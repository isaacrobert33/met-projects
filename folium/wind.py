from math import cos, sin, radians
import folium
import random

def add_wind_marker(map_obj, lat, lon, speed, direction):
    # Calculate the end point of the arrow based on speed and direction
    direction_radians = radians(direction)
    end_lat = lat + (speed * 0.01 * cos(direction_radians))
    end_lon = lon + (speed * 0.01 * sin(direction_radians))
    
    folium.PolyLine(
        locations=[[lat, lon], [end_lat, end_lon]],
        color="blue",
        weight=3
    ).add_to(map_obj)

# Create a map
m = folium.Map(location=[6.8276, -5.2893], zoom_start=6)

# Example wind data (lat, lon, speed in m/s, direction in degrees)
winds = [
    [6.8276 + random.uniform(-1.5, 2.5), -5.2893 + random.uniform(-2.5, 2), random.uniform(7, 12), random.uniform(30, 90)]
    for i in range(120)
]

for wind in winds:
    add_wind_marker(m, wind[0], wind[1], wind[2], wind[3])

# Save the map
m.save("wind_map.html")
