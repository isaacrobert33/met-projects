import folium
import random

# Initialize map centered around Côte d'Ivoire
map_ci = folium.Map(location=[7.54, -5.5471], zoom_start=7)

# Sample cities and their coordinates in Côte d'Ivoire
cities = {
    "Abidjan": [5.359951, -4.008256],
    "Yamoussoukro": [6.827623, -5.289343],
    "Bouaké": [7.693850, -5.030311],
    "Korhogo": [9.458038, -5.629324],
    "Daloa": [6.877370, -6.451774],
    "San Pedro": [4.748510, -6.636020],
    "Man": [7.412513, -7.553832],
    "Odienné": [9.509167, -7.563543],
    "Bondoukou": [8.040936, -2.803568],
    "Gagnoa": [6.131933, -5.950666]
}

# Generate random humidity data (in %) for each city
for city, coords in cities.items():
    humidity = random.uniform(50, 100)  # Random humidity between 50% and 100%
    color = "green" if humidity < 70 else "orange" if humidity < 85 else "red"
    
    folium.CircleMarker(
        location=coords,
        radius=10,  # Size of the marker
        popup=f"{city}: {humidity:.1f}% humidity",  # Display city name and humidity in popup
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.6,
    ).add_to(map_ci)

# Save the map as an HTML file
map_ci.save("humidity_map_cote_d_ivoire.html")
