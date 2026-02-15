import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from folium.plugins import MarkerCluster, HeatMap
from streamlit_folium import folium_static
import joblib
import os


st.set_page_config(
    page_title="NASA Meteorite Analytics",
    page_icon="☄️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Global Background & Font */
    .stApp {
        background-color: #0e1117;
        color: #c9d1d9;
        font-family: 'Roboto', sans-serif;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #58a6ff;
        font-weight: 300;
        letter-spacing: 1px;
    }
    h1 { margin-bottom: 20px; border-bottom: 1px solid #30363d; padding-bottom: 10px; }
    
    /* Metrics */
    div[data-testid="stMetricValue"] {
        color: #ff7b72;
        font-size: 2.5rem;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #161b22;
        border-radius: 4px;
        padding-left: 20px;
        padding-right: 20px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #58a6ff !important;
        color: white !important;
    }

    /* Hide Streamlit Deploy Button */
    .stDeployButton {
        display: none;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    try:
        df = pd.read_csv("cleaned_meteorites.csv")
    except FileNotFoundError:
        st.error("Data file not found! Please ensure 'cleaned_meteorites.csv' is in the folder.")
        df = pd.DataFrame(columns=['name', 'recclass', 'mass', 'year', 'reclat', 'reclong', 'fall'])
    return df

@st.cache_resource
def load_model():
    if os.path.exists("meteorite_model.pkl"):
        return joblib.load("meteorite_model.pkl")
    return None

df = load_data()
model = load_model()


st.sidebar.title("CONTROLS")


min_year = int(df['year'].min()) if not df.empty else 800
max_year = int(df['year'].max()) if not df.empty else 2024
year_range = st.sidebar.slider("Timeframe", min_year, max_year, (1900, 2020))


mass_limit = st.sidebar.select_slider("Minimum Mass (g)", options=[0, 10, 100, 1000, 10000, 100000], value=0)


all_classes = df['recclass'].unique().tolist() if not df.empty else []
selected_classes = st.sidebar.multiselect("Classification", all_classes, default=all_classes[:3] if len(all_classes)>2 else all_classes)


if not df.empty:
    filtered_df = df[
        (df['year'] >= year_range[0]) & 
        (df['year'] <= year_range[1]) & 
        (df['mass'] >= mass_limit) &
        (df['recclass'].isin(selected_classes) if selected_classes else True)
    ]
else:
    filtered_df = df

st.title("ORBITAL IMPACT ANALYTICS")

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Detected Impacts", f"{len(filtered_df):,}")
with col2:
    total_mass_tons = filtered_df['mass'].sum() / 1000000
    st.metric("Total Mass (Tonnes)", f"{total_mass_tons:,.2f}")
with col3:
    avg_year = int(filtered_df['year'].mean()) if not filtered_df.empty else 0
    st.metric("Avg Impact Year", f"{avg_year}")
with col4:
    heaviest = filtered_df['mass'].max() / 1000 if not filtered_df.empty else 0
    st.metric("Heaviest Object (kg)", f"{heaviest:,.1f}")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["GEOSPATIAL MAP", "DATA ANALYSIS", "AI PREDICTION"])

with tab1:
    map_type = st.radio("Map Visualization", ["Clusters", "Heatmap"], horizontal=True)
    
    if not filtered_df.empty:
        m = folium.Map(location=[20, 0], zoom_start=2, tiles="CartoDB dark_matter")
        
        map_data = filtered_df.head(2000) 
        
        if map_type == "Clusters":
            marker_cluster = MarkerCluster().add_to(m)
            for _, row in map_data.iterrows():
                folium.CircleMarker(
                    location=[row['reclat'], row['reclong']],
                    radius=3,
                    color='#58a6ff',
                    fill=True,
                    fill_color='#58a6ff',
                    tooltip=f"{row['name']} ({row['year']}) <br> Mass: {row['mass']}g"
                ).add_to(marker_cluster)
        else:
            heat_data = [[row['reclat'], row['reclong']] for _, row in map_data.iterrows()]
            HeatMap(heat_data, radius=15, blur=20).add_to(m)
            
        folium_static(m, width=None, height=600)
    else:
        st.warning("No data matches filters.")

with tab2:
    c1, c2 = st.columns(2)
    
    with c1:
        st.subheader("Top Classifications")
        if not filtered_df.empty:
            top_classes = filtered_df['recclass'].value_counts().head(10).reset_index()
            top_classes.columns = ['Class', 'Count']
            
            fig_class = px.bar(
                top_classes,
                x='Count',
                y='Class',
                orientation='h',
                color='Count',
                color_continuous_scale='Viridis',
                template="plotly_dark"
            )
            fig_class.update_layout(
                yaxis={'categoryorder':'total ascending'},
                paper_bgcolor="rgba(0,0,0,0)", 
                plot_bgcolor="rgba(0,0,0,0)"
            )
            st.plotly_chart(fig_class, use_container_width=True)

    with c2:
        st.subheader("Temporal Trends")
        if not filtered_df.empty:
            year_counts = filtered_df[filtered_df['year'] > 1800]['year'].value_counts().sort_index()
            fig_trend = px.area(
                x=year_counts.index, 
                y=year_counts.values,
                labels={'x': 'Year', 'y': 'Impact Count'},
                color_discrete_sequence=['#ff7b72'],
                template="plotly_dark"
            )
            fig_trend.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig_trend, use_container_width=True)

with tab3:
    st.subheader("Meteorite Composition Scanner")
    st.markdown("Enter physical parameters to identify the likely **Chemical Classification** (e.g., L6 Chondrite, Iron).")
    
    @st.cache_resource
    def load_type_classifier():
        model_path = "meteorite_model.pkl" 
        if os.path.exists(model_path):
            return joblib.load(model_path)
        return None

    type_model = load_type_classifier()

    if type_model:
        with st.form("type_form"):
            c1, c2 = st.columns(2)
            with c1:
                in_mass = st.number_input("Mass (g)", value=500.0, step=10.0)
                in_lat = st.number_input("Latitude", value=0.0, format="%.4f")
            with c2:
                in_year = st.number_input("Year Found", value=2000, step=1)
                in_long = st.number_input("Longitude", value=0.0, format="%.4f")
            
            submitted = st.form_submit_button("Analyze Composition")
            
            if submitted:
                input_data = pd.DataFrame([[in_mass, in_year, in_lat, in_long]], 
                                        columns=['mass', 'year', 'reclat', 'reclong'])
                
                prediction = type_model.predict(input_data)[0]
                
                pass_proba = False
                if hasattr(type_model, "predict_proba"):
                    try:
                        probs = type_model.predict_proba(input_data)[0]
                        pass_proba = True
                    except:
                        pass_proba = False

                st.markdown("---")
                st.success(f"### Identified Type: **{prediction}**")
                
                if pass_proba:
                    classes = type_model.classes_
                    prob_df = pd.DataFrame({'Class': classes, 'Probability': probs})
                    prob_df = prob_df.sort_values(by='Probability', ascending=False).head(5)
                    
                    st.caption("Confidence Profile:")
                    fig_conf = px.bar(prob_df, x='Probability', y='Class', orientation='h',
                                    color='Probability', range_x=[0, 1],
                                    color_continuous_scale='Viridis')
                    fig_conf.update_layout(yaxis={'categoryorder':'total ascending'},
                                         height=250, margin=dict(l=0, r=0, t=0, b=0),
                                         paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
                    st.plotly_chart(fig_conf, use_container_width=True)

    else:
        st.warning("⚠️ Composition Model not found.")
        st.markdown("""
        **Action Required:**
        1. Run the "Composition Classifier" script in Colab.
        2. Download `meteorite_model.pkl`.
        3. Place it in this folder.
        """)

st.markdown("---")
st.markdown("<center><small>NASA Open Data Portal | Built with Streamlit & Plotly</small></center>", unsafe_allow_html=True)
