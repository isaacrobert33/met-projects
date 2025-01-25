import ee
import pandas as pd
import matplotlib.pyplot as plt

# Coordinates for the location
latitude = 7.250771
longitude = 5.210266

# Initialize Earth Engine
ee.Initialize(proect='ee-isaacrobert')

roi = ee.Geometry.Point([longitude, latitude])  # Region of interest

# Load MODIS NDVI dataset
modis = (
    ee.ImageCollection("MODIS/006/MOD13A1")
    .filterDate("2020-01-01", "2024-10-31")
    .filterBounds(roi)
    .select("NDVI")
)

# Scale factor for MODIS NDVI (0-1)
scale_factor = 0.0001


# Calculate seasonal means
def add_season(image):
    """Add a 'season' property to each image based on its month."""
    month = ee.Date(image.get("system:time_start")).get("month")
    season = ee.Number(month).expression(
        "1 * (month >= 3 and month <= 5) + "
        "2 * (month >= 6 and month <= 8) + "
        "3 * (month >= 9 and month <= 11) + "
        "4 * (month >= 12 or month <= 2)",
        {"month": month},
    )
    return image.set("season", season)


modis = modis.map(add_season)

# Reduce data to seasonal means
seasonal_ndvi = (
    modis.aggregate_array("season")
    .distinct()
    .map(
        lambda season: {
            "season": season,
            "mean_ndvi": modis.filter(ee.Filter.eq("season", season))
            .mean()
            .reduceRegion(reducer=ee.Reducer.mean(), geometry=roi, scale=500)
            .get("NDVI"),
        }
    )
    .getInfo()
)

# Convert to DataFrame
df = pd.DataFrame(seasonal_ndvi)
df["mean_ndvi"] = pd.to_numeric(df["mean_ndvi"]) * scale_factor
df["season"] = df["season"].map({1: "Spring", 2: "Summer", 3: "Fall", 4: "Winter"})

# Plot seasonal NDVI
df.plot(
    x="season",
    y="mean_ndvi",
    kind="bar",
    color="green",
    legend=False,
    title="Seasonal NDVI Trends for Akure",
)
plt.ylabel("Mean NDVI")
plt.savefig("seasonal_trends.png")
