import folium

# Create a map centered around a specific location (latitude, longitude)
m = folium.Map(location=[6.8276, -5.2893], zoom_start=6)

# Add markers for weather stations
stations = [
    {"name": "Station 1", "lat": 6.8276, "lon": -5.2893},
    {"name": "Station 2", "lat": 5.3483, "lon": -4.0244}
]

for station in stations:
    folium.Marker(
        location=[station['lat'], station['lon']],
        popup=station['name'],
        icon=folium.Icon(icon="cloud")
    ).add_to(m)

# Display the map
m.save("weather_stations_map.html")
