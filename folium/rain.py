import folium
import random

# Initialize map centered around Côte d'Ivoire
map_ci = folium.Map(location=[7.54, -5.5471], zoom_start=7)

# Sample cities and their coordinates in Côte d'Ivoire

cities = {
    "Abidjan": [5.2858, -3.3036, 127.7], #    
    "Adiake": [5.3252, -4.0196, 189], # 
    "BONDOUKOU": [8.0479, -2.8079, 156.9], #    
    "BOUAKE": [7.6905, -5.0391, 124.9], #    
    "DALOA": [6.8774, -6.4502, 146.3], #    
    "DIMBOKRO": [6.6575, -4.7122, 333.3], #  
    "GAGNOA": [6.1514, -5.9515, 231.2], #      
    "KORHOGO": [9.4669, -5.6143, 90.7], #    
    "MAN": [7.4064, -7.5572, 159.7], #    
    "ODIENNE": [9.5189, -7.5572, 128.7], #    
    "SAN PEDRO": [4.7579, -6.6424, 126.6], #    
    "SASSANDRA": [4.9513, -6.0918, 184.7], #   
    "TABOU": [4.4279, -7.3571, 205.4], #   
    "YAMOUSSOUKRO": [6.82055,-5.276739, 164.6], #   
}

# Generate random rainfall data (in mm) for each city
for city, [lat, lon, rainfall]  in cities.items():
    folium.CircleMarker(
        location=[lat, lon],
        radius=15,  # Size of the marker
        popup=f"{city}: {rainfall:.1f} mm",  # Display city name and rainfall in popup
        color="blue",
        fill=True,
        fill_color="#61f9f6" if rainfall < 130 else "#6464fb",  # Color based on rainfall amount
        fill_opacity=0.6,
    ).add_to(map_ci)

# Display the map
map_ci.save("rainfall_map_cote_d_ivoire.html")
