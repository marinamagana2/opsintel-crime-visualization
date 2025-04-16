# OpsIntel: Crime Visualization

Hi! I'm Marina, a junior in college, and this is a project I made to explore and visualize crime data in Chicago. Using Python and cool libraries like pandas, seaborn, and folium, I broke down trends in when and where crimes happen, and built interactive maps to help make it easier to see patterns.

## 🚨 What This Project Does
This script cleans and analyzes a real Chicago crime dataset, then visualizes the data in a few different ways:

### 📊 Charts
- **Bar chart by hour of day** – When do crimes happen most often?
- **Bar chart by weekday** – Which days are the busiest for crime?
- **Line chart by month & year** – Trends over time.

### 🗺️ Maps
- **Simple crime map** – Basic map showing crimes with red markers.
- **Color-coded map** – Markers change color based on the crime type (e.g., red for homicide, blue for theft).
- **Legend included** – So it's clear what each color means.
- **Heatmap** – See where crimes are more concentrated overall.
- **Layered heatmaps by crime type** – Toggle between types like theft, battery, and more.
- **Animated map** – Watch crimes appear in the order they happened!

## 💡 Why I Made This
I wanted to get more hands-on experience with data visualization and mapping, and learn how to communicate trends in an accessible way. I also just think mapping crime data is super interesting and important.

## 🛠️ Tools Used
- Python
- pandas
- matplotlib / seaborn
- folium / branca

## 🔎 How to Run It
1. Make sure you have Python 3 and pip installed.
2. Install the required packages:
```bash
pip install -r requirements.txt
```
3. Run the script:
```bash
python3 main.py
```
4. Open the HTML map files to explore the visualizations:
   - `crime_map.html`
   - `colored_crime_map.html`
   - `crime_heatmap.html`
   - `crime_layers_heatmap.html`
   - `crime_animated_map.html`

## 📁 Dataset
The crime data comes from Chicago’s public crime data portal. Only a sample of rows are used to keep things responsive.

---

Thanks for checking it out! 😊 Let me know if you have any tips, questions, or ideas to improve it!
