import matplotlib.pyplot as plt
import geopandas as gpd
from shapely.geometry import Polygon, Point

# Define the outer polygon
outer_coords = [
    (0.0, 0.0), (0.0, 30.0), (0.0, 40.0), (0.0, 50.0), 
    (50.0, 50.0), (40.0, 0.0), (30.0, 0.0), (0.0, 0.0)
]
outer_polygon = Polygon(outer_coords)

# Define the inner polygon
inner_coords = [
    (0.0, 5.0), (5.0, 5.0), (5.0, 0.0), (0.0, 10.0), (10.0, 10.0), (10.0, 0.0), (0.0, 5.0)
]
inner_polygon = Polygon(inner_coords)

# Create GeoSeries
gdf = gpd.GeoSeries([outer_polygon, inner_polygon])

# Plot
fig, ax = plt.subplots(figsize=(8, 8))
gdf.plot(ax=ax, edgecolor='black', facecolor=['none', 'red'])
ax.set_title("Geographic Map with Two Polygons")
ax.set_xlabel("Longitude")
ax.set_ylabel("Latitude")
plt.grid(True)
plt.savefig("map.png")
