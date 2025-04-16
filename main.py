# ======================================
# 1. Load & Clean Crime Dataset
# ======================================

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from folium.plugins import HeatMap, TimestampedGeoJson
from branca.element import Template, MacroElement
from folium import Map, LayerControl, FeatureGroup
from datetime import datetime

# Load the dataset
df = pd.read_csv("data/chicago_crime_data.csv", low_memory=False)

# Clean up column names and rename
df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
df = df.rename(columns={"date__of_occurrence": "date"})

# Parse date and drop invalid ones
df["date"] = pd.to_datetime(df["date"], format="%m/%d/%Y %I:%M:%S %p", errors="coerce")
df = df.dropna(subset=["date"])

# Extract useful time components
df["hour"] = df["date"].dt.hour
df["weekday"] = df["date"].dt.day_name()
df["month"] = df["date"].dt.month
df["year"] = df["date"].dt.year

# Drop rows missing lat/lon
df = df.dropna(subset=["latitude", "longitude"])

# Keep only relevant columns
columns_to_keep = [
    "primary_description", "date", "hour", "weekday", "month", "year",
    "latitude", "longitude", "arrest"
]
df = df[columns_to_keep]


# ======================================
# 2. Exploratory Data Visualizations
# ======================================

sns.set(style="darkgrid")

# Crime by hour
plt.figure(figsize=(10, 6))
sns.countplot(x="hour", data=df, palette="viridis")
plt.title("Crime Count by Hour of Day")
plt.xlabel("Hour of Day (0–23)")
plt.ylabel("Number of Crimes")
plt.tight_layout()
plt.show()

# Crime by weekday
plt.figure(figsize=(10, 6))
sns.countplot(x="weekday", data=df, order=[
    "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"
], palette="coolwarm")
plt.title("Crime Count by Day of the Week")
plt.xlabel("Day of the Week")
plt.ylabel("Number of Crimes")
plt.tight_layout()
plt.show()

# Crime by month
monthly_counts = df["month"].value_counts().sort_index()
plt.figure(figsize=(10, 6))
sns.lineplot(x=monthly_counts.index, y=monthly_counts.values, marker="o")
plt.title("Crime Trends by Month")
plt.xlabel("Month (1 = Jan, 12 = Dec)")
plt.ylabel("Number of Crimes")
plt.xticks(range(1, 13))
plt.tight_layout()
plt.show()

# Crime by year
yearly_counts = df["year"].value_counts().sort_index()
plt.figure(figsize=(10, 6))
sns.lineplot(x=yearly_counts.index, y=yearly_counts.values, marker="o")
plt.title("Crime Trends by Year")
plt.xlabel("Year")
plt.ylabel("Number of Crimes")
plt.xticks(yearly_counts.index)
plt.tight_layout()
plt.show()


# ======================================
# 3. Sample and Color Coding
# ======================================

homicides = df[df["primary_description"].str.contains("HOMICIDE", case=False)].sample(n=50, random_state=1)
others = df[~df["primary_description"].str.contains("HOMICIDE", case=False)].sample(n=950, random_state=2)
sample_df = pd.concat([homicides, others])

# Color function
def get_color(crime_type):
    crime_type = crime_type.lower()
    if "homicide" in crime_type:
        return "red"
    elif "theft" in crime_type:
        return "blue"
    elif "battery" in crime_type:
        return "orange"
    else:
        return "gray"


# ======================================
# 4. Color-Coded Crime Marker Map
# ======================================

colored_map = folium.Map(location=[41.8781, -87.6298], zoom_start=11)

for _, row in sample_df.iterrows():
    folium.CircleMarker(
        location=[row["latitude"], row["longitude"]],
        radius=3,
        color=get_color(row["primary_description"]),
        fill=True,
        fill_opacity=0.6,
        tooltip=f"{row['primary_description']} - {row['date'].strftime('%b %d, %Y %I:%M %p')}",
        popup=row["primary_description"]
    ).add_to(colored_map)

# Add legend
legend_html = """
{% macro html(this, kwargs) %}
<div style="position: fixed; bottom: 50px; left: 50px; z-index:9999; background-color:white;
padding: 10px; border:2px solid grey; border-radius:5px; box-shadow: 2px 2px 6px rgba(0,0,0,0.3); font-size:14px;">
    <b>Crime Type Legend</b><br>
    <i style="background:red; width:10px; height:10px; display:inline-block; border-radius:50%;"></i> Homicide<br>
    <i style="background:blue; width:10px; height:10px; display:inline-block; border-radius:50%;"></i> Theft<br>
    <i style="background:orange; width:10px; height:10px; display:inline-block; border-radius:50%;"></i> Battery<br>
    <i style="background:gray; width:10px; height:10px; display:inline-block; border-radius:50%;"></i> Other
</div>
{% endmacro %}
"""
legend = MacroElement()
legend._template = Template(legend_html)
colored_map.get_root().add_child(legend)
colored_map.save("colored_crime_map.html")
print("Color-coded crime map saved as 'colored_crime_map.html'")


# ======================================
# 5. Glow Heatmap
# ======================================

heatmap = folium.Map(location=[41.8781, -87.6298], zoom_start=11)
heat_data = [[row["latitude"], row["longitude"]] for _, row in sample_df.iterrows()]
HeatMap(heat_data, radius=10, blur=15).add_to(heatmap)
heatmap.save("crime_heatmap.html")
print("Heatmap saved as 'crime_heatmap.html'")


# ======================================
# 6. Layered Heatmap by Crime Type
# ======================================

crime_type_map = folium.Map(location=[41.8781, -87.6298], zoom_start=11)
crime_categories = {"Homicide": [], "Theft": [], "Battery": [], "Other": []}

for _, row in sample_df.iterrows():
    crime = row["primary_description"].lower()
    coord = [row["latitude"], row["longitude"]]
    if pd.isnull(coord[0]) or pd.isnull(coord[1]):
        continue
    if "homicide" in crime:
        crime_categories["Homicide"].append(coord)
    elif "theft" in crime:
        crime_categories["Theft"].append(coord)
    elif "battery" in crime:
        crime_categories["Battery"].append(coord)
    else:
        crime_categories["Other"].append(coord)

for crime_type, coords in crime_categories.items():
    fg = folium.FeatureGroup(name=crime_type)
    HeatMap(coords, radius=10, blur=15).add_to(fg)
    fg.add_to(crime_type_map)

folium.LayerControl().add_to(crime_type_map)
crime_type_map.save("crime_layers_heatmap.html")
print("Layered crime heatmap saved as 'crime_layers_heatmap.html'")


# ======================================
# 7. Animated Timestamped Map
# ======================================

animated_sample = sample_df.sample(n=200, random_state=3)
features = []

for _, row in animated_sample.iterrows():
    if pd.isnull(row["latitude"]) or pd.isnull(row["longitude"]):
        continue
    timestamp = row["date"].strftime("%Y-%m-%dT%H:%M:%S")
    features.append({
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row["longitude"], row["latitude"]],
        },
        "properties": {
            "time": timestamp,
            "popup": row["primary_description"],
            "icon": "circle",
            "iconstyle": {
                "fillColor": get_color(row["primary_description"]),
                "fillOpacity": 0.6,
                "stroke": False,
                "radius": 5
            }
        }
    })

animated_map = folium.Map(location=[41.8781, -87.6298], zoom_start=11)

TimestampedGeoJson(
    {"type": "FeatureCollection", "features": features},
    period="PT1H",
    add_last_point=True,
    auto_play=True,
    loop=False,
    max_speed=1,
    loop_button=True,
    date_options="YYYY-MM-DD HH:mm",
    time_slider_drag_update=True,
).add_to(animated_map)

animated_map.save("crime_animated_map.html")
print("Animated crime map saved as 'crime_animated_map.html'")
