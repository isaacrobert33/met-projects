import ee
# import geopandas as gpd
import matplotlib.pyplot as plt
import numpy as np
import folium
from folium.plugins import HeatMap

# Initialize Earth Engine
ee.Initialize(project='ee-isaacrobert')

# # Coordinates for the location
# latitude = 7.250771
# longitude = 5.210266
# roi = ee.Geometry.Point([longitude, latitude]).buffer(8000)  # Region of interest

# # Load MODIS NDVI dataset
# modis = ee.ImageCollection('MODIS/061/MOD13A1') \
#     .select('NDVI')

# # Scale factor for MODIS NDVI (0-1)
# scale_factor = 0.0001

# # Function to clip the image to the region of interest
# def clip_to_roi(image):
#     return image.clip(roi)

# # Function to extract image for each year and display it
# def create_spatial_map(year):
#     # Filter for the specific year
#     modis_year = modis.filterDate(f'{year}-01-01', f'{year}-12-31') \
#                       .mean()  # Take the mean NDVI for the year
    
#     # Clip to region of interest
#     modis_year_clipped = clip_to_roi(modis_year)
    
#     # Fetch image data and transform to numpy array
#     ndvi_data = modis_year_clipped.reduceRegion(
#         reducer=ee.Reducer.mean(),
#         geometry=roi,
#         scale=500,
#         maxPixels=1e8
#     ).getInfo()
    
#     # Extract NDVI value
#     ndvi_value = ndvi_data['NDVI'] * scale_factor
    
#     # Since we are working with a small region, generate a dummy 2x2 map for visualization
#     # Normally, we would sample an area around the point
#     dummy_map = np.full((2, 2), ndvi_value)
#     print(dummy_map)
    
#     # Create the plot
#     plt.figure(figsize=(10, 8))
#     plt.imshow(dummy_map, cmap='YlGn', interpolation='none', origin='upper')
#     plt.colorbar(label='NDVI')
#     plt.title(f'Spatial Map of NDVI for {year}')
#     plt.xlabel('Longitude')
#     plt.ylabel('Latitude')
#     plt.savefig(f'yearly_maps/{year}.png')

# # Create spatial maps for 2020 to 2024
# for year in range(2020, 2025):
#     create_spatial_map(year)


# Coordinates for the location
latitude = 7.250771
longitude = 5.210266
roi = ee.Geometry.Point([longitude, latitude])  # Region of interest

# Load MODIS NDVI dataset
modis = ee.ImageCollection('MODIS/061/MOD13A1') \
    .select('NDVI')

# Function to filter by season
def filter_by_season(image_collection, season_months):
    """
    Filters the image collection to only include images from the specified season (months).
    """
    return image_collection.filter(ee.Filter.calendarRange(season_months[0], season_months[1], 'month'))

# Function to clip image to region of interest (ROI)
def clip_to_roi(image):
    return image.clip(roi)

# Function to create Folium map with NDVI data overlay for each season and year
def create_seasonal_map(year, season_months, season_name):
    # Filter MODIS data for the specific year and season
    modis_season = modis.filterDate(f'{year}-01-01', f'{year}-12-31')
    modis_season_filtered = filter_by_season(modis_season, season_months)
    
    # Take the mean NDVI for the season
    modis_season_mean = modis_season_filtered.mean()
    
    # Clip to region of interest (ROI)
    modis_season_clipped = clip_to_roi(modis_season_mean)
    
    # Get map ID for the NDVI season layer with colorful vegetation cover
    map_id_dict = modis_season_clipped.getMapId({
        'min': 0,    # Min NDVI (No vegetation, bare ground)
        'max': 10000, # Max NDVI (Dense vegetation)
        'palette': ['yellow', 'orange', 'red', 'green', 'blue']  # Color palette for vegetation cover
    })
    
    # Construct the tile URL for the NDVI map
    map_id = map_id_dict['mapid']
    tile_url = f'https://earthengine.googleapis.com/v1alpha/maps/{map_id}/tiles/{{z}}/{{x}}/{{y}}?token={map_id_dict["token"]}'
    
    # Create the base map centered on the ROI (Nigeria)
    folium_map = folium.Map(location=[latitude, longitude], zoom_start=7)
    
    # Add the seasonal NDVI tile layer to the map
    folium.TileLayer(
        tiles=tile_url,
        attr=f"MODIS NDVI {year} {season_name}",
        overlay=True,
        name=f"{season_name} {year}"
    ).add_to(folium_map)
    
    # Display the map with a layer control
    folium_map.add_child(folium.LayerControl())
    
    return folium_map

# Generate maps for each year (2020-2024) and each season

# Define the seasons (Rainy: April - October, Dry: November - March)
seasons = {
    "Rainy": (4, 10),  # April to October
    "Dry": (11, 3)     # November to March
}

# Generate maps for each year and season
for year in range(2020, 2025):
    for season_name, season_months in seasons.items():
        folium_map = create_seasonal_map(year, season_months, season_name)
        folium_map.save(f'yearly_maps/{season_name}_vegetation_cover_map_{year}.html')