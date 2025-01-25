from folium.plugins import HeatMap
import folium
import random

# Generate some random data for the example (latitude, longitude, and intensity)
# data = [[6.8276 + random.uniform(-0.5, 0.5), -5.2893 + random.uniform(-0.5, 0.5), random.uniform(20, 35)] for i in range(50)]

data = [
    [5.2858, -3.3036, 26.10], # Abidjan   
    [5.3252, -4.0196, 26.30], # Adiake
    [8.0479, -2.8079, 25.90], # BONDOUKOU   
    [7.6905, -5.0391, 24.80], # BOUAKE   
    [6.8774, -6.4502,26.30], # DALOA   
    [6.6575, -4.7122,27.00], # DIMBOKRO 
    [6.1514, -5.9515,26.00], # GAGNOA     
    [9.4669, -5.6143,25.90], # KORHOGO   
    [7.4064, -7.5572,25.40], # MAN   
    [9.5189, -7.5572,25.40], # ODIENNE   
    [4.7579, -6.6424,25.60], # SAN PEDRO   
    [4.9513, -6.0918,25.5], # SASSANDRA  
    [4.4279, -7.3571,26.00], # TABOU  
    [6.82055,-5.276739,26.00], # YAMOUSSOUKRO  
]


# Create a map
m = folium.Map(location=[6.8276, -5.2893], zoom_start=7, radius=40, blur=15,)

# Add heat map
HeatMap(data).add_to(m)

# Save the map
m.save("temperature_heatmap.html")
