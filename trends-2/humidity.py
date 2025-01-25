import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap

max_humidity_file = (
    "trends-2/HUMIDITE MAXI ABSOLU 1991-2020.xlsx - HUMIDITE MAXI TABCLIM PL ANABSO.csv"
)
min_humidity_file = (
    "trends-2/HUMIDITE MINI ABSOLU 1991-2020.xlsx - HUMIDITE MINI TABCLIM REQAbsolu.csv"
)

max_df = pd.read_csv(max_humidity_file)
min_df = pd.read_csv(min_humidity_file)

humidity_data = pd.merge(min_df, max_df, on="NOM", suffixes=("_MIN", "_MAX"))
humidity_long = pd.melt(
    humidity_data,
    id_vars=["NOM"],
    value_vars=[
        "JAN_MIN",
        "FEV_MIN",
        "MARS_MIN",
        "AVRIL_MIN",
        "MAI_MIN",
        "JUIN_MIN",
        "JUILLET_MIN",
        "AOUT_MIN",
        "SEPT_MIN",
        "OCT_MIN",
        "NOV_MIN",
        "DEC_MIN",
        "JAN_MAX",
        "FEV_MAX",
        "MARS_MAX",
        "AVRIL_MAX",
        "MAI_MAX",
        "JUIN_MAX",
        "JUILLET_MAX",
        "AOUT_MAX",
        "SEPT_MAX",
        "OCT_MAX",
        "NOV_MAX",
        "DEC_MAX",
    ],
    var_name="Month_Type",
    value_name="Humidity",
)

humidity_long["Month"] = humidity_long["Month_Type"].str.extract(
    r"(JAN|FEV|MARS|AVRIL|MAI|JUIN|JUILLET|AOUT|SEPT|OCT|NOV|DEC)"
)
humidity_long["Type"] = (
    humidity_long["Month_Type"].str.contains("MAX").map({True: "Max", False: "Min"})
)

# Drop the original column
humidity_long.drop(columns=["Month_Type"], inplace=True)

# Visualizations
plt.figure(figsize=(12, 6))
sns.lineplot(
    data=humidity_long, x="Month", y="Humidity", hue="NOM", style="Type", markers=True
)

plt.title("Monthly Min and Max Humidity Trends by City")
plt.xlabel("Month")
plt.ylabel("Humidity (%)")
plt.xticks(rotation=45)
plt.legend(title="City and Type", bbox_to_anchor=(1.05, 1), loc="upper left")
plt.tight_layout()
plt.savefig("humidity_trends.png")

# Pivot data for heatmap
heatmap_data = humidity_long.pivot_table(
    index="Month", columns="NOM", values="Humidity", aggfunc="mean"
)

plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, cmap="YlGnBu", annot=True, fmt=".1f")
plt.title("Heatmap of Monthly Average Humidity Across Cities")
plt.xlabel("City")
plt.ylabel("Month")
plt.savefig("humidity_heatmap.png")


city_locations = {
    "ABIDJAN": [5.359951, -4.008256],
    "YAMOUSSOUKRO": [6.827623, -5.289343],
    "BOUAKE": [7.693850, -5.030311],
    "KORHOGO": [9.458038, -5.629324],
    "DALOA": [6.877370, -6.451774],
    "SAN-PEDRO": [4.748510, -6.636020],
    "MAN": [7.412513, -7.553832],
    "ODIENNE": [9.509167, -7.563543],
    "BONDOUKOU": [8.040936, -2.803568],
    "GAGNOA": [6.131933, -5.950666],
    "ADIAKE": [5.28634, -3.30403],
    "TABOU": [4.42295, -7.3528],
    "SASSANDRA": [4.95384, -6.08531],
    "DIMBOKRO": [6.64678, -4.70519],
}

# Ensure city names match exactly by cleaning data
humidity_data["NOM"] = humidity_data[
    "NOM"
].str.strip()  # Remove leading/trailing spaces
humidity_data["NOM"] = humidity_data["NOM"].str.replace(
    r"[*]", "", regex=True
)  # Remove special characters like '*'

humidity_data.to_csv("merge-humidity.csv")

# Create a Folium map
m = folium.Map(
    location=[6.8276, -5.2893],
    zoom_start=7,
    radius=40,
    blur=15,
)

# Add city markers
for city, coords in city_locations.items():
    # Check if the city exists in the data
    if city in humidity_data["NOM"].values:
        # Get humidity data for the city
        city_data = humidity_data[humidity_data["NOM"] == city]
        min_annual = city_data["MINI ANNUELLE"].values[0]  # Single value assumed
        max_annual = city_data["MAXI ANNUELLE"].values[0]

        # Add marker to the map
        folium.CircleMarker(
            location=coords,
            radius=5,
            color="blue",
            fill=True,
            fill_color="blue",
            popup=f"{city}: Min {min_annual}% | Max {max_annual}%",
        ).add_to(m)
    else:
        print(f"City '{city}' not found in the data. Skipping...")

# Save the map
m.save("humidity_map.html")

# Calculate average annual humidity for each city
humidity_data["AVG_ANNUAL"] = humidity_data.filter(like="JAN").mean(axis=1)

# Add coordinates to the DataFrame
humidity_data["Coordinates"] = humidity_data["NOM"].map(city_locations)

# Create a list of heatmap data (latitude, longitude, intensity)
heatmap_data = [
    [coords[0], coords[1], avg]
    for coords, avg in zip(humidity_data["Coordinates"], humidity_data["AVG_ANNUAL"])
    # if not pd.isnull(coords)  # Ensure coordinates exist
]

# Initialize Folium map
m = folium.Map(
    location=[6.8276, -5.2893],
    zoom_start=7,
    radius=40,
    blur=15,
)

print(heatmap_data)
# Add the heatmap layer
HeatMap(heatmap_data).add_to(m)

# Save map to an HTML file
m.save("geo_humidity_heatmap.html")
print("Heatmap saved as geo_humidity_heatmap.html")
