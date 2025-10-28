"""
Live Solar Dashboard - Example with Real API Data
Uses OpenWeatherMap API to fetch solar radiation and weather data
"""
import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
from datetime import datetime, timedelta
import math

# Page config
st.set_page_config(
    page_title="Live Solar PV Dashboard",
    page_icon="☀️",
    layout="wide"
)

# API Configuration
API_KEY = st.secrets.get("OPENWEATHER_API_KEY", "demo")
LAT = float(st.secrets.get("LATITUDE", 48.1351))  # Munich
LON = float(st.secrets.get("LONGITUDE", 11.5820))
CITY = "Munich"

@st.cache_data(ttl=300)  # Cache for 5 minutes
def fetch_weather_data(lat, lon, api_key):
    """Fetch current weather data from OpenWeatherMap"""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Weather API Error: {e}")
        return None

@st.cache_data(ttl=300)
def fetch_forecast_data(lat, lon, api_key):
    """Fetch 5-day forecast"""
    try:
        url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&appid={api_key}&units=metric"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return None

@st.cache_data(ttl=300)
def fetch_uv_data(lat, lon, api_key):
    """Fetch UV index data"""
    try:
        url = f"https://api.openweathermap.org/data/2.5/uvi?lat={lat}&lon={lon}&appid={api_key}"
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        return None

def calculate_estimated_solar_power(cloud_cover, uv_index, time_of_day, temp=25):
    """
    Estimate solar power output based on weather conditions
    Simplified model for 5kW system
    """
    max_power = 5.0  # kW
    
    # Cloud cover factor (0-100%)
    cloud_factor = (100 - cloud_cover) / 100
    
    # UV index factor (0-11+)
    uv_factor = min(uv_index / 10, 1.0)
    
    # Time of day factor (solar angle simulation)
    hour = time_of_day.hour + time_of_day.minute / 60
    if 6 <= hour <= 20:
        # Peak at solar noon (13:00)
        time_factor = abs(math.sin((hour - 6) * math.pi / 14))
    else:
        time_factor = 0
    
    # Temperature factor (panels lose ~0.5% efficiency per °C above 25°C)
    temp_factor = 1 - (max(0, temp - 25) * 0.005)
    
    estimated_power = max_power * cloud_factor * uv_factor * time_factor * temp_factor
    return max(0, estimated_power)

# Main dashboard
st.markdown("# ☀️ Live Solar PV Dashboard")
st.markdown(f"**Location:** {CITY} (Lat {LAT:.4f}, Lon {LON:.4f}) | **Last Update:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
st.markdown("---")

# Fetch live data
weather_data = fetch_weather_data(LAT, LON, API_KEY)
forecast_data = fetch_forecast_data(LAT, LON, API_KEY)
uv_data = fetch_uv_data(LAT, LON, API_KEY)

if weather_data and API_KEY != "demo":
    # Extract current weather metrics
    cloud_cover = weather_data.get("clouds", {}).get("all", 0)
    temp = weather_data.get("main", {}).get("temp", 25)
    humidity = weather_data.get("main", {}).get("humidity", 0)
    wind_speed = weather_data.get("wind", {}).get("speed", 0)
    pressure = weather_data.get("main", {}).get("pressure", 0)
    visibility = weather_data.get("visibility", 0) / 1000  # km
    weather_desc = weather_data.get("weather", [{}])[0].get("description", "N/A").title()
    
    # Get UV index
    uv_index = uv_data.get("value", 5) if uv_data else 5
    
    # Calculate current power estimate
    current_time = datetime.now()
    estimated_power = calculate_estimated_solar_power(cloud_cover, uv_index, current_time, temp)
    
    # Key metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "⚡ Current Power",
            f"{estimated_power:.2f} kW",
            delta=f"{(estimated_power/5.0)*100:.1f}% capacity"
        )
    
    with col2:
        st.metric(
            "🌡️ Temperature",
            f"{temp:.1f}°C",
            delta=None
        )
    
    with col3:
        st.metric(
            "☁️ Cloud Cover",
            f"{cloud_cover}%",
            delta=f"UV: {uv_index:.1f}"
        )
    
    with col4:
        efficiency = (100 - cloud_cover) * 0.85
        st.metric(
            "📊 Efficiency",
            f"{min(efficiency, 100):.1f}%",
            delta=f"{humidity}% humidity"
        )
    
    st.markdown("---")
    
    # Power gauge and weather details
    col_gauge, col_weather = st.columns([1, 1])
    
    with col_gauge:
        st.subheader("Current Power Output")
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number",
            value=estimated_power,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "Power (kW)"},
            gauge={
                'axis': {'range': [None, 5.0]},
                'bar': {'color': "#FFA726"},
                'steps': [
                    {'range': [0, 2.5], 'color': '#E8F5E9'},
                    {'range': [2.5, 5.0], 'color': '#C8E6C9'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 4.5
                }
            }
        ))
        fig_gauge.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
        st.plotly_chart(fig_gauge, use_container_width=True)
    
    with col_weather:
        st.subheader("Weather Conditions")
        st.write(f"**Conditions:** {weather_desc}")
        st.write(f"**Visibility:** {visibility:.1f} km")
        st.write(f"**Pressure:** {pressure} hPa")
        st.write(f"**Wind Speed:** {wind_speed} m/s")
        st.write(f"**UV Index:** {uv_index:.1f}")
        
        # Sun position indicator (simplified)
        hour = current_time.hour
        if 6 <= hour <= 20:
            sun_position = "☀️ Daylight"
        else:
            sun_position = "🌙 Night"
        st.write(f"**Sun Status:** {sun_position}")
    
    # 5-day forecast
    if forecast_data:
        st.markdown("---")
        st.subheader("5-Day Power Forecast")
        
        forecast_list = forecast_data.get("list", [])
        forecast_df = pd.DataFrame([
            {
                "datetime": datetime.fromtimestamp(item["dt"]),
                "temp": item["main"]["temp"],
                "clouds": item["clouds"]["all"],
                "estimated_power_kw": calculate_estimated_solar_power(
                    item["clouds"]["all"],
                    uv_index,
                    datetime.fromtimestamp(item["dt"]),
                    item["main"]["temp"]
                )
            }
            for item in forecast_list[:40]  # 5 days, 3-hour intervals
        ])
        
        # Power forecast chart
        fig_forecast = go.Figure()
        fig_forecast.add_trace(go.Scatter(
            x=forecast_df["datetime"],
            y=forecast_df["estimated_power_kw"],
            mode='lines',
            name='Estimated Power',
            line=dict(color='#2E7D32', width=2),
            fill='tozeroy',
            fillcolor='rgba(46, 125, 50, 0.2)'
        ))
        
        fig_forecast.update_layout(
            title="Solar PV Power Forecast (5 Days)",
            xaxis_title="Date/Time",
            yaxis_title="Power (kW)",
            hovermode='x unified',
            height=400
        )
        st.plotly_chart(fig_forecast, use_container_width=True)
        
        # Daily energy estimate
        st.markdown("---")
        st.subheader("Daily Energy Production Estimate")
        
        forecast_df['date'] = forecast_df['datetime'].dt.date
        daily_energy = forecast_df.groupby('date')['estimated_power_kw'].sum() * 3 / 1000  # kWh (3-hour intervals)
        
        fig_daily = go.Figure()
        fig_daily.add_trace(go.Bar(
            x=[str(d) for d in daily_energy.index],
            y=daily_energy.values,
            name='Daily Energy',
            marker_color='#FF9800'
        ))
        
        fig_daily.update_layout(
            title="Estimated Daily Energy Production (kWh)",
            xaxis_title="Date",
            yaxis_title="Energy (kWh)",
            height=350
        )
        st.plotly_chart(fig_daily, use_container_width=True)
        
        # Temperature vs Power correlation
        col_temp, col_cloud = st.columns(2)
        
        with col_temp:
            fig_temp = go.Figure()
            fig_temp.add_trace(go.Scatter(
                x=forecast_df["datetime"],
                y=forecast_df["temp"],
                mode='lines+markers',
                name='Temperature',
                line=dict(color='#FF5722', width=2)
            ))
            fig_temp.update_layout(
                title="Temperature Forecast",
                xaxis_title="Date/Time",
                yaxis_title="Temperature (°C)",
                height=300
            )
            st.plotly_chart(fig_temp, use_container_width=True)
        
        with col_cloud:
            fig_cloud = go.Figure()
            fig_cloud.add_trace(go.Scatter(
                x=forecast_df["datetime"],
                y=forecast_df["clouds"],
                mode='lines+markers',
                name='Cloud Cover',
                line=dict(color='#607D8B', width=2),
                fill='tozeroy'
            ))
            fig_cloud.update_layout(
                title="Cloud Cover Forecast",
                xaxis_title="Date/Time",
                yaxis_title="Cloud Cover (%)",
                height=300
            )
            st.plotly_chart(fig_cloud, use_container_width=True)
    
    # Data table
    st.markdown("---")
    with st.expander("📊 View Forecast Data Table"):
        if forecast_data and 'forecast_df' in locals():
            display_df = forecast_df[['datetime', 'temp', 'clouds', 'estimated_power_kw']].copy()
            display_df.columns = ['Timestamp', 'Temp (°C)', 'Clouds (%)', 'Power (kW)']
            st.dataframe(display_df, use_container_width=True)

elif API_KEY == "demo":
    st.warning("⚠️ **Demo Mode** - Please configure your OpenWeatherMap API key")
    st.markdown("""
    ### How to get started:
    1. Get a free API key from [OpenWeatherMap](https://openweathermap.org/api)
    2. Add to `.streamlit/secrets.toml`:
       ```toml
       OPENWEATHER_API_KEY = "your_api_key_here"
       ```
    3. Refresh the page
    
    **Features:**
    - Real-time weather data
    - 5-day solar power forecast
    - UV index tracking
    - Cloud cover analysis
    - Temperature impact on efficiency
    """)
else:
    st.error("❌ Failed to fetch weather data. Please check your API key and internet connection.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <small>Powered by <a href='https://openweathermap.org/' target='_blank'>OpenWeatherMap API</a> | 
    Data updates every 5 minutes | 
    Power estimates based on weather conditions</small>
</div>
""", unsafe_allow_html=True)
