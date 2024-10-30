from folium.plugins import HeatMap
import folium
import random

# Generate some random data for the example (latitude, longitude, and intensity)
data = [[6.8276 + random.uniform(-0.5, 0.5), -5.2893 + random.uniform(-0.5, 0.5), random.uniform(20, 35)] for i in range(50)]

# Create a map
m = folium.Map(location=[6.8276, -5.2893], zoom_start=6)

# Add heat map
HeatMap(data).add_to(m)

# Save the map
m.save("temperature_heatmap.html")
