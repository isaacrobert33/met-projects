import ee
import folium

# Initialize Earth Engine
ee.Initialize(project='ee-isaacrobert')

# Coordinates for the location
latitude = 7.250771
longitude = 5.210266
roi = ee.Geometry.Point([longitude, latitude])  # Region of interest

# Load MODIS NDVI dataset
modis = ee.ImageCollection('MODIS/061/MOD13A1') \
    .filterDate('2021-01-01', '2024-12-31') \
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

# Generate a map for each season
def generate_seasonal_map(season_number, title) -> folium.Element:
    """Generate a map for a specific season."""
    season_images = modis.filter(ee.Filter.eq('season', season_number))
    
    # Calculate mean NDVI for the selected season
    seasonal_mean = season_images.mean().clip(roi)
    
    # Visualization parameters for NDVI (color gradient)
    vis_params = {
        'min': 0.0,
        'max': 0.8,
        'palette': ['blue', 'white', 'green', 'yellow', 'red']
    }
    
    # Create the map with the seasonal mean NDVI image
    map = folium.Map(location=[latitude, longitude], zoom_start=10)
    map.add_ee_layer(seasonal_mean, vis_params, title)
    
    return map

# Adding the layer function to Folium maps
def add_ee_layer(self, ee_image, vis_params, name):
    """Add an Earth Engine image to a Folium map."""
    map_id = ee.Image(ee_image).getMapId(vis_params)
    folium.TileLayer(
        tiles=map_id['tile_fetcher'].url_format,
        attr='Map Data &copy; <a href="https://earthengine.google.com/">Google Earth Engine</a>',
        name=name,
        overlay=True,
        control=True
    ).add_to(self)

# Add the layer method to folium.Map class
folium.Map.add_ee_layer = add_ee_layer

# Generate maps for each season
generate_seasonal_map(1, 'Harmattan (Dry Season)').save('ndvi_maps/Harmattan (Dry Season).html')
generate_seasonal_map(2, 'Hot Dry').save('ndvi_maps/Hot Dry.html')
generate_seasonal_map(3, 'Early Rainy').save('ndvi_maps/Early Rainy.html')
generate_seasonal_map(4, 'Peak Rainy').save('ndvi_maps/Peak Rainy.html')
