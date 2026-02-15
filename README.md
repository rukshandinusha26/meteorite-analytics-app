# ☄️ Orbital Impact Analytics - Meteorite Dashboard

A professional, interactive data science dashboard built with **Streamlit** to visualize and analyze over 30,000 meteorite landings from NASA's Open Data Portal.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.28%2B-ff4b4b)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🌟 Features

### 1. 🌍 Geospatial Intelligence Map
- Interactive global map powered by **Folium**.
- Switch between **Cluster View** (for individualdatapoints) and **Heatmap View** (for impact density).
- Filtering by **Mass**, **Year**, and **Classification**.

### 2. 📊 Advanced Analytics
- Real-time KPIs: **Total Mass Impact**, **Average Impact Year**, and **Heaviest Object**.
- **Temporal Trends**: Area charts showing the discovery rate of meteorites over the last two centuries.
- **Top Classifications**: Horizontal bar charts analyzing the most common meteorite types.

### 3. 🧪 AI Composition Scanner
- **Machine Learning Integration**: Uses a **Random Forest Classifier** (Scikit-Learn).
- **Predictive Modeling**: Input physical parameters (Mass, Location, Year) to predict the meteorite's **Chemical Group** (e.g., L Chondrite vs. Iron).
- **Confidence Profile**: Visualizes the model's certainty across the top potential matches.

---

## 🛠️ Installation

1.  **Clone the Repository** (or download the files):
    ```bash
    git clone https://github.com/yourusername/meteorite-analytics.git
    cd meteorite-analytics
    ```

2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Data Setup**:
    - Ensure `cleaned_meteorites.csv` is in the root directory.
    - Ensure `meteorite_model.pkl` (the trained ML model) is in the root directory.

---

## 🚀 Usage

### Option 1: One-Click Launch (Windows)
Double-click the included `run_app.bat` file to launch the dashboard instantly.

### Option 2: Command Line
Run the following command in your terminal:
```bash
streamlit run app.py
```

The app will open in your default web browser at `http://localhost:8501`.

---

## 📦 Tech Stack

-   **Frontend**: [Streamlit](https://streamlit.io/)
-   **Data Processing**: [Pandas](https://pandas.pydata.org/)
-   **Visualization**: [Plotly Express](https://plotly.com/python/), [Folium](https://python-visualization.github.io/folium/)
-   **Machine Learning**: [Scikit-Learn](https://scikit-learn.org/)

---

## 📂 Project Structure

```
├── app.py                  # Main application source code
├── cleaned_meteorites.csv  # Processed dataset (NASA)
├── meteorite_model.pkl     # Pre-trained Random Forest model
├── requirements.txt        # Python dependencies
└── README.md               # Project documentation
```

## 🔗 Data Source
Data provided by the [NASA Open Data Portal](https://data.nasa.gov/Space-Science/Meteorite-Landings/gh4g-9sfh).

---

