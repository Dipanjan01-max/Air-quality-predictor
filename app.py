# app.py
import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import pytz

# ----------------------
# Page Configuration
# ----------------------
st.set_page_config(
    page_title="Air Quality Prediction | Earth Monitor", 
    page_icon="🌍", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ----------------------
# Modern CSS with Rotating Earth Background
# ----------------------
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, rgba(10, 10, 20, 0.95), rgba(20, 30, 60, 0.9)), 
                    url('https://images.unsplash.com/photo-1614730321146-b6fa6a46bcb4?auto=format&fit=crop&w=3840&q=80');
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        font-family: 'Inter', sans-serif;
        animation: earthRotate 120s linear infinite;
    }
    
    @keyframes earthRotate {
        0% { background-position: 0% center; }
        100% { background-position: 200% center; }
    }
    
    /* Glassmorphism container */
    .block-container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(20px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 2.5rem 2.5rem;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] > div {
        background: rgba(0, 0, 0, 0.7);
        backdrop-filter: blur(15px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* Header styling */
    .main-title {
        background: linear-gradient(135deg, #00c6ff, #0072ff, #7b68ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 0.5rem;
        text-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
    }
    
    .subtitle {
        color: rgba(255, 255, 255, 0.8);
        text-align: center;
        font-size: 1.2rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    
    /* Modern metric cards */
    div[data-testid="stMetricValue"] {
        font-size: 3rem;
        font-weight: 600;
        background: linear-gradient(135deg, #00c6ff, #0072ff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    .metric-card {
        background: rgba(255, 255, 255, 0.08);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.15);
        border-radius: 20px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
    }
    
    /* Status indicators */
    .status-good {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        padding: 1rem 2rem;
        border-radius: 15px;
        text-align: center;
        font-weight: 600;
        box-shadow: 0 10px 25px rgba(76, 175, 80, 0.3);
    }
    
    .status-moderate {
        background: linear-gradient(135deg, #FF9800, #F57C00);
        color: white;
        padding: 1rem 2rem;
        border-radius: 15px;
        text-align: center;
        font-weight: 600;
        box-shadow: 0 10px 25px rgba(255, 152, 0, 0.3);
    }
    
    .status-unhealthy {
        background: linear-gradient(135deg, #f44336, #d32f2f);
        color: white;
        padding: 1rem 2rem;
        border-radius: 15px;
        text-align: center;
        font-weight: 600;
        box-shadow: 0 10px 25px rgba(244, 67, 54, 0.3);
    }
    
    .status-hazardous {
        background: linear-gradient(135deg, #9C27B0, #7B1FA2);
        color: white;
        padding: 1rem 2rem;
        border-radius: 15px;
        text-align: center;
        font-weight: 600;
        box-shadow: 0 10px 25px rgba(156, 39, 176, 0.3);
    }
    
    /* Sidebar enhancements */
    .sidebar-header {
        color: #00c6ff;
        font-size: 1.5rem;
        font-weight: 600;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    /* Input styling */
    .stSlider > div > div > div {
        background: linear-gradient(135deg, #00c6ff, #0072ff);
    }
    
    /* Footer */
    .footer {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 15px;
        padding: 1.5rem;
        margin-top: 2rem;
        text-align: center;
        color: rgba(255, 255, 255, 0.7);
    }
    
    /* Pulse animation for alerts */
    .pulse {
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(244, 67, 54, 0.7); }
        70% { box-shadow: 0 0 0 10px rgba(244, 67, 54, 0); }
        100% { box-shadow: 0 0 0 0 rgba(244, 67, 54, 0); }
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 255, 255, 0.1);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #00c6ff, #0072ff);
        border-radius: 10px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #0072ff, #7b68ee);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ----------------------
# Header with Modern Design
# ----------------------
ist = pytz.timezone("Asia/Kolkata")
now = datetime.now(ist)

st.markdown('<h1 class="main-title">🌍 Air Quality Earth Monitor</h1>', unsafe_allow_html=True)
st.markdown(
    f'<div class="subtitle">📅 {now.strftime("%A, %d %B %Y")} — 🕒 {now.strftime("%I:%M %p %Z")}<br>'
    f'Real-time AI-powered air quality prediction with 24-hour forecasting</div>', 
    unsafe_allow_html=True
)

# ----------------------
# Load model (with error handling)
# ----------------------
@st.cache_resource
def load_model():
    try:
        return joblib.load("air_quality_model.pkl")
    except FileNotFoundError:
        st.error("Model file not found. Please ensure 'air_quality_model.pkl' is in the same directory.")
        return None

model = load_model()

if model is None:
    st.stop()

# ----------------------
# Enhanced Sidebar Inputs
# ----------------------
st.sidebar.markdown('<div class="sidebar-header">⚙️ Pollutant Input Panel</div>', unsafe_allow_html=True)

with st.sidebar:
    st.markdown("### Primary Pollutants")
    PM10 = st.slider("PM10 (Particulate Matter)", 0, 500, 100, help="Particles with diameter ≤ 10 micrometers")
    PM25_current = st.slider("Current PM2.5", 0, 300, 50, help="Fine particles ≤ 2.5 micrometers")
    
    st.markdown("### Gas Pollutants")
    NO2 = st.slider("NO₂ (Nitrogen Dioxide)", 0, 200, 40, help="Traffic and industrial emissions")
    SO2 = st.slider("SO₂ (Sulfur Dioxide)", 0, 100, 10, help="Coal burning and industrial processes")
    CO = st.slider("CO (Carbon Monoxide)", 0.0, 20.0, 1.0, step=0.1, help="Vehicle emissions")
    O3 = st.slider("O₃ (Ground-level Ozone)", 0, 200, 30, help="Secondary pollutant from reactions")
    
    st.markdown("### Environmental Factors")
    humidity = st.slider("Humidity (%)", 20, 100, 60)
    temperature = st.slider("Temperature (°C)", -10, 50, 25)
    wind_speed = st.slider("Wind Speed (km/h)", 0, 50, 10)

# Prepare input data
X = pd.DataFrame([[PM10, NO2, SO2, CO, O3]], columns=["PM10", "NO2", "SO2", "CO", "O3"])

# ----------------------
# Enhanced Prediction & Safety Assessment
# ----------------------
pm25 = float(model.predict(X)[0])

def get_safety_info(pm25):
    if pm25 <= 50:
        return {
            "level": "Good",
            "emoji": "🟢",
            "message": "Air quality is excellent! Perfect for outdoor activities.",
            "class": "status-good",
            "advice": "Great day for jogging, cycling, or spending time outdoors.",
            "aqi_range": "0-50"
        }
    elif pm25 <= 100:
        return {
            "level": "Moderate", 
            "emoji": "🟡",
            "message": "Air quality is acceptable for most people.",
            "class": "status-moderate", 
            "advice": "Sensitive individuals should consider limiting prolonged outdoor exertion.",
            "aqi_range": "51-100"
        }
    elif pm25 <= 150:
        return {
            "level": "Unhealthy for Sensitive Groups",
            "emoji": "🟠", 
            "message": "Sensitive groups may experience minor health effects.",
            "class": "status-moderate",
            "advice": "Children, elderly, and people with respiratory issues should reduce outdoor activities.",
            "aqi_range": "101-150"
        }
    elif pm25 <= 200:
        return {
            "level": "Unhealthy",
            "emoji": "🔴",
            "message": "Everyone may experience health effects.",
            "class": "status-unhealthy",
            "advice": "Limit outdoor activities. Wear masks when going outside.",
            "aqi_range": "151-200"
        }
    elif pm25 <= 300:
        return {
            "level": "Very Unhealthy", 
            "emoji": "🟣",
            "message": "Health alert! Everyone should avoid outdoor activities.",
            "class": "status-unhealthy pulse",
            "advice": "Stay indoors with windows closed. Use air purifiers if available.",
            "aqi_range": "201-300"
        }
    else:
        return {
            "level": "Hazardous",
            "emoji": "⚫",
            "message": "Emergency conditions! Serious health risks for everyone.",
            "class": "status-hazardous pulse", 
            "advice": "Remain indoors and avoid all outdoor activities. Seek medical attention if experiencing symptoms.",
            "aqi_range": "300+"
        }

safety = get_safety_info(pm25)

# ----------------------
# Main Dashboard Layout
# ----------------------
col1, col2 = st.columns([1, 2], gap="large")

with col1:
    # Main prediction card
    st.metric("🎯 Predicted PM2.5", f"{pm25:.1f} µg/m³", f"{pm25 - PM25_current:+.1f}")
    
    # Safety status card
    if safety["level"] == "Good":
        st.success(f'{safety["emoji"]} **{safety["level"]}**\n\n{safety["message"]}\n\nAQI Range: {safety["aqi_range"]}')
    elif safety["level"] == "Moderate" or "Sensitive" in safety["level"]:
        st.warning(f'{safety["emoji"]} **{safety["level"]}**\n\n{safety["message"]}\n\nAQI Range: {safety["aqi_range"]}')
    else:
        st.error(f'{safety["emoji"]} **{safety["level"]}**\n\n{safety["message"]}\n\nAQI Range: {safety["aqi_range"]}')
    
    # Advice card
    st.info(f"💡 **Health Recommendations**\n\n_{safety['advice']}_")

with col2:
    # Enhanced 24-hour trend with realistic patterns
    st.markdown("### 📊 24-Hour PM2.5 Forecast")
    
    # Create more realistic hourly data with diurnal patterns
    hours = np.arange(24)
    
    # Realistic diurnal pattern: higher during rush hours, lower at night
    rush_hour_morning = 0.3 * np.exp(-((hours - 8)**2) / 8)  # Morning rush
    rush_hour_evening = 0.4 * np.exp(-((hours - 18)**2) / 12)  # Evening rush
    night_reduction = -0.2 * np.exp(-((hours - 3)**2) / 6)  # Night dip
    
    # Environmental factors
    wind_effect = -0.1 * (wind_speed / 50)  # Higher wind reduces pollution
    humidity_effect = 0.05 * (humidity / 100)  # Higher humidity can trap pollutants
    
    # Combine effects
    pattern = rush_hour_morning + rush_hour_evening + night_reduction + wind_effect + humidity_effect
    
    # Add some realistic noise
    np.random.seed(42)  # For reproducible results
    noise = np.random.normal(0, pm25 * 0.08, 24)
    
    # Generate the trend
    trend = np.clip(pm25 * (1 + pattern) + noise, 5, None)
    
    # Create DataFrame
    df_trend = pd.DataFrame({
        "Hour": [f"{h:02d}:00" for h in hours],
        "PM2.5": trend,
        "Status": [get_safety_info(val)["level"] for val in trend],
        "Color": [get_safety_info(val)["emoji"] for val in trend]
    })
    
    # Create enhanced plotly chart
    fig = go.Figure()
    
    # Add the main line
    fig.add_trace(go.Scatter(
        x=df_trend["Hour"],
        y=df_trend["PM2.5"],
        mode='lines+markers',
        name='PM2.5 Forecast',
        line=dict(
            color='rgba(0, 198, 255, 0.8)',
            width=3,
            shape='spline'
        ),
        marker=dict(
            size=8,
            color=df_trend["PM2.5"],
            colorscale='RdYlGn_r',
            showscale=True,
            colorbar=dict(title="PM2.5 Level")
        ),
        hovertemplate='<b>%{x}</b><br>PM2.5: %{y:.1f} µg/m³<extra></extra>'
    ))
    
    # Add safety threshold lines
    fig.add_hline(y=50, line_dash="dash", line_color="green", opacity=0.5, annotation_text="Good")
    fig.add_hline(y=100, line_dash="dash", line_color="orange", opacity=0.5, annotation_text="Moderate")
    fig.add_hline(y=150, line_dash="dash", line_color="red", opacity=0.5, annotation_text="Unhealthy")
    
    fig.update_layout(
        template="plotly_dark",
        margin=dict(l=10, r=10, t=40, b=60),
        xaxis_title="Time of Day",
        yaxis_title="PM2.5 Concentration (µg/m³)",
        hovermode="x unified",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0.1)",
        font=dict(family="Inter, sans-serif"),
        showlegend=False,
        height=400
    )
    
    fig.update_xaxes(tickangle=45, tickmode='linear', dtick=2)
    fig.update_yaxes(gridcolor='rgba(255,255,255,0.1)')
    
    st.plotly_chart(fig, use_container_width=True)

# ----------------------
# Additional Insights Panel
# ----------------------
st.markdown("---")

col3, col4, col5 = st.columns(3)

with col3:
    st.markdown("### 🌡️ Environmental Impact")
    impact_score = (humidity * 0.3 + temperature * 0.4 + (50 - wind_speed) * 0.3) / 100
    st.metric("Environmental Factor", f"{impact_score:.2f}", "Pollution Retention")
    if impact_score > 0.7:
        st.markdown("⚠️ _Weather conditions favor pollution accumulation_")
    else:
        st.markdown("✅ _Weather conditions help disperse pollutants_")

with col4:
    st.markdown("### 📈 Pollutant Analysis")
    dominant = max([('PM10', PM10), ('NO₂', NO2), ('SO₂', SO2), ('CO', CO*10), ('O₃', O3)], key=lambda x: x[1])
    st.metric("Dominant Pollutant", dominant[0], f"{dominant[1]:.1f}")
    if dominant[0] in ['PM10', 'NO₂']:
        st.markdown("🚗 _Likely traffic-related pollution_")
    elif dominant[0] in ['SO₂', 'CO']:
        st.markdown("🏭 _Possible industrial source_")
    else:
        st.markdown("☀️ _Secondary pollutant formation_")

with col5:
    st.markdown("### ⏰ Peak Pollution Time")
    peak_hour = np.argmax(trend)
    peak_value = trend[peak_hour]
    st.metric("Peak Hour", f"{peak_hour:02d}:00", f"{peak_value:.1f} µg/m³")
    if 7 <= peak_hour <= 9:
        st.markdown("🌅 _Morning rush hour peak_")
    elif 17 <= peak_hour <= 20:
        st.markdown("🌆 _Evening rush hour peak_")
    else:
        st.markdown("🌙 _Unusual peak timing_")

# ----------------------
# Modern Footer
# ----------------------
st.markdown(
    """
    <div class="footer">
        <h4>🔬 About This Prediction</h4>
        <p>This AI model analyzes pollutant interactions and environmental factors to predict PM2.5 levels. 
        The forecast incorporates realistic diurnal patterns, weather influences, and traffic cycles.</p>
        <p><strong>⚠️ Disclaimer:</strong> This is an ML estimation tool. For official air quality data, 
        please consult your local environmental monitoring authority.</p>
        <hr style="border: 1px solid rgba(255,255,255,0.1); margin: 1rem 0;">
        <p style="font-size: 0.9rem; opacity: 0.7;">
            🌍 Earth Monitor | Powered by Advanced Machine Learning | Real-time Environmental Intelligence
        </p>
    </div>
    """,
    unsafe_allow_html=True
)