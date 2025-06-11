# import ee
# import pandas as pd
# import matplotlib.pyplot as plt

# # Coordinates for the location
# latitude = 7.250771
# longitude = 5.210266

# # Initialize Earth Engine
# ee.Initialize(project='ee-isaacrobert')

# roi = ee.Geometry.Point([longitude, latitude])  # Region of interest

# # Load MODIS NDVI dataset
# modis = (
#     ee.ImageCollection("MODIS/061/MOD13A1")
#     .filterDate("2020-01-01", "2024-10-31")
#     .filterBounds(roi)
#     .select("NDVI")
# )

# # Scale factor for MODIS NDVI (0-1)
# scale_factor = 0.0001


# # Calculate seasonal means
# def add_season(image):
#     """Add a 'season' property to each image based on its month."""
#     month = ee.Date(image.get("system:time_start")).get("month")
#     season = ee.Number(month).expression(
#         "1 * (month >= 3 and month <= 5) + "
#         "2 * (month >= 6 and month <= 8) + "
#         "3 * (month >= 9 and month <= 11) + "
#         "4 * (month >= 12 or month <= 2)",
#         {"month": month},
#     )
#     return image.set("season", season)


# modis = modis.map(add_season)

# # Reduce data to seasonal means
# seasonal_ndvi = (
#     modis.aggregate_array("season")
#     .distinct()
#     .map(
#         lambda season: {
#             "season": season,
#             "mean_ndvi": modis.filter(ee.Filter.eq("season", season))
#             .mean()
#             .reduceRegion(reducer=ee.Reducer.mean(), geometry=roi, scale=500)
#             .get("NDVI"),
#         }
#     )
#     .getInfo()
# )

# # Convert to DataFrame
# df = pd.DataFrame(seasonal_ndvi)
# df["mean_ndvi"] = pd.to_numeric(df["mean_ndvi"]) * scale_factor
# df["season"] = df["season"].map({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"})

# # Plot seasonal NDVI
# df.plot(
#     x="season",
#     y="mean_ndvi",
#     kind="bar",
#     color="green",
#     legend=False,
#     title="Seasonal NDVI Trends for Akure",
# )
# plt.ylabel("Mean NDVI")
# plt.savefig("seasonal_trends.png")


import ee
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import UnivariateSpline

# Initialize Earth Engine
ee.Initialize(project='ee-isaacrobert')

# Coordinates for the location
latitude = 7.250771
longitude = 5.210266
# roi = ee.Geometry.Point([longitude, latitude])  # Region of interest
# Define the region of interest (ROI) as a bounding box (min_lon, min_lat, max_lon, max_lat)
roi = ee.Geometry.BBox(5.15, 7.2, 5.27, 7.3)

# Load MODIS NDVI dataset
modis = ee.ImageCollection('MODIS/061/MOD13A1') \
    .filterDate('2021-01-01', '2021-12-31') \
    .filterBounds(roi) \
    .select('NDVI')

# Scale factor for MODIS NDVI (0-1)
scale_factor = 0.0001

# Define seasons for West Africa
def assign_season(image):
    """Add a 'season' property to each image based on its month."""
    month = ee.Date(image.get('system:time_start')).get('month')
    season = ee.Number(month).expression(
        '1 * (month >= 11 or month <= 2) + '  # Dry Season (Harmattan)
        '2 * (month >= 3 and month <= 5) + '  # Hot Dry
        '3 * (month >= 6 and month <= 7) + '  # Early Rainy
        '4 * (month >= 8 and month <= 10)',   # Peak Rainy
        {'month': month}
    )
    return image.set('season', season)

# Map season property to the dataset
modis = modis.map(assign_season)

# Extract NDVI and metadata
def extract_ndvi(image):
    """Reduce image to extract NDVI and associate with season and date."""
    ndvi_value = image.reduceRegion(
        reducer=ee.Reducer.mean(),
        geometry=roi,
        scale=500
    ).get('NDVI')
    
    return ee.Feature(None, {
        'NDVI': ndvi_value,
        'season': image.get('season'),
        'date': image.date().format('YYYY-MM-dd')
    })

# Apply extraction and convert to a feature collection
ndvi_features = modis.map(extract_ndvi)
ndvi_fc = ee.FeatureCollection(ndvi_features)

# Export data to Python for plotting
ndvi_data = ndvi_fc.getInfo()['features']
data = [{'NDVI': f['properties']['NDVI'],
         'season': f['properties']['season'],
         'date': f['properties']['date']} for f in ndvi_data]

# Convert to pandas DataFrame
df = pd.DataFrame(data)
df['NDVI'] = pd.to_numeric(df['NDVI'], errors='coerce') * scale_factor
df['season'] = df['season'].map({
    1: 'Dry Season (Harmattan)',
    2: 'Hot Dry',
    3: 'Early Rainy',
    4: 'Peak Rainy'
})
df['date'] = pd.to_datetime(df['date'])

# Remove rows with NaN NDVI values
df = df.dropna(subset=['NDVI'])

# Boxplot of seasonal NDVI
plt.figure(figsize=(10, 6))
df.boxplot(column='NDVI', by='season', grid=False, patch_artist=True,
           boxprops=dict(facecolor='lightgreen', color='green'),
           medianprops=dict(color='red'), whiskerprops=dict(color='green'))
plt.title('Seasonal NDVI Trend (2021-2024)')
plt.suptitle('')
plt.xlabel('Season')
plt.ylabel('NDVI')
plt.xticks(rotation=15)
plt.savefig('ak_seasonal_trend_3.png')

# Plot NDVI trends over time, grouped by season
plt.figure(figsize=(12, 6))
for season, group in df.groupby('season'):
    plt.plot(group['date'], group['NDVI'], label=season)

plt.title('NDVI Trends Over Time by Season (2021)')
plt.xlabel('Date')
plt.ylabel('NDVI')
plt.legend(title='Season')
plt.grid(True, linestyle='--', alpha=0.5)
plt.savefig('ak_seasonal_trend_line_plot.png')

# Calculate seasonal averages
seasonal_avg = df.groupby('season')['NDVI'].mean()
print(seasonal_avg)

# Plot smoothened seasonal NDVI trends using UnivariateSpline for each season
# plt.figure(figsize=(12, 6))
# for season, group in df.groupby('season'):
#     # Extract x (date) and y (NDVI) values
#     x = group['date'].map(lambda date: date.toordinal())  # Convert date to ordinal for smoothing
#     y = group['NDVI']
    
#     # Apply a smoothing function (UnivariateSpline)
#     spline = UnivariateSpline(x, y, s=0.5)  # s controls the smoothness
#     x_smooth = np.linspace(min(x), max(x), 1000)
#     y_smooth = spline(x_smooth)
    
#     # Convert smoothened x values back to dates
#     x_smooth_dates = pd.to_datetime(x_smooth, origin='julian', unit='D')

#     # Plot the smooth trend line
#     plt.plot(x_smooth_dates, y_smooth, label=season)

# plt.title('Smoothed NDVI Trends Over Time by Season (2021-2024)')
# plt.xlabel('Date')
# plt.ylabel('NDVI')
# plt.legend(title='Season')
# plt.grid(True, linestyle='--', alpha=0.5)

# plt.savefig('seasonal_smooth_trend.png')




######################## SPATIAL MAPS ##################################
# Calculate mean NDVI for the specified time range
# mean_ndvi = modis.mean()

# # Scale NDVI values (MODIS NDVI values need to be scaled by 0.0001)
# scaled_ndvi = mean_ndvi.multiply(0.0001)

# # Visualization parameters
# ndvi_vis = {
#     'min': 0.0,
#     'max': 1.0,
#     'palette': ['brown', 'yellow', 'green'],  # NDVI color scale
# }

# # Create a folium map centered at the given coordinates
# center = [latitude, longitude]
# m = folium.Map(location=center, zoom_start=12)

# # Add NDVI layer to the map
# ndvi_tile = folium.Map(
#     location=center,
#     zoom_start=12
# )

# ndvi_map_id = ee.Image(scaled_ndvi).getMapId(ndvi_vis)
# folium.TileLayer(
#     tiles=ndvi_map_id['tile_fetcher'].url_format,
#     attr='Map Data &copy; Google Earth Engine',
#     name='Mean NDVI',
#     overlay=True,
#     control=True
# ).add_to(m)

# # Add layer control to the map
# folium.LayerControl().add_to(m)

# # Display the map
# m.save('ndvi_spatial_map.html')