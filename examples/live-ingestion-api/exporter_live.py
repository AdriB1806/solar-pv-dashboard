"""
Prometheus Exporter for Live Solar Data
Fetches weather/solar data from OpenWeatherMap and exposes as Prometheus metrics
"""
from prometheus_client import start_http_server, Gauge
import requests
import time
import os
from datetime import datetime
import math

# Prometheus metrics
pv_estimated_power_watts = Gauge('pv_estimated_power_watts', 'Estimated solar power output in watts')
pv_cloud_cover_percent = Gauge('pv_cloud_cover_percent', 'Cloud cover percentage')
pv_temperature_celsius = Gauge('pv_temperature_celsius', 'Ambient temperature')
pv_humidity_percent = Gauge('pv_humidity_percent', 'Humidity percentage')
pv_wind_speed_mps = Gauge('pv_wind_speed_mps', 'Wind speed in meters per second')
pv_uv_index = Gauge('pv_uv_index', 'UV index')
pv_efficiency_percent = Gauge('pv_efficiency_percent', 'Estimated solar efficiency')

# Configuration
API_KEY = os.getenv("OPENWEATHER_API_KEY", "demo")
LAT = float(os.getenv("LATITUDE", "48.1351"))  # Munich
LON = float(os.getenv("LONGITUDE", "11.5820"))
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", "300"))  # 5 minutes

def calculate_estimated_solar_power(cloud_cover, uv_index, current_hour):
    """Estimate solar power output based on weather conditions"""
    max_power = 5000  # Watts (5kW system)
    
    # Cloud cover factor
    cloud_factor = (100 - cloud_cover) / 100
    
    # UV index factor
    uv_factor = min(uv_index / 11, 1.0)
    
    # Time of day factor
    if 6 <= current_hour <= 20:
        time_factor = abs(math.sin((current_hour - 6) * math.pi / 14))
    else:
        time_factor = 0
    
    estimated_power = max_power * cloud_factor * uv_factor * time_factor
    return max(0, estimated_power)

def fetch_and_update_metrics():
    """Fetch weather data and update Prometheus metrics"""
    try:
        url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&appid={API_KEY}&units=metric"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        # Extract metrics
        cloud_cover = data.get("clouds", {}).get("all", 0)
        temp = data.get("main", {}).get("temp", 0)
        humidity = data.get("main", {}).get("humidity", 0)
        wind_speed = data.get("wind", {}).get("speed", 0)
        uv_index = 5  # Default (OpenWeatherMap free tier doesn't include UV)
        
        # Calculate estimated power
        current_hour = datetime.now().hour
        estimated_power = calculate_estimated_solar_power(cloud_cover, uv_index, current_hour)
        efficiency = (100 - cloud_cover) * 0.8
        
        # Update Prometheus metrics
        pv_estimated_power_watts.set(estimated_power)
        pv_cloud_cover_percent.set(cloud_cover)
        pv_temperature_celsius.set(temp)
        pv_humidity_percent.set(humidity)
        pv_wind_speed_mps.set(wind_speed)
        pv_uv_index.set(uv_index)
        pv_efficiency_percent.set(efficiency)
        
        print(f"[{datetime.now()}] Metrics updated - Power: {estimated_power:.0f}W, Clouds: {cloud_cover}%, Temp: {temp:.1f}°C")
        
    except Exception as e:
        print(f"[{datetime.now()}] Error fetching data: {e}")

if __name__ == "__main__":
    # Start Prometheus HTTP server
    port = int(os.getenv("EXPORTER_PORT", "8000"))
    start_http_server(port)
    print(f"Prometheus exporter running on port {port}")
    print(f"Metrics available at http://localhost:{port}/metrics")
    print(f"Polling interval: {POLL_INTERVAL}s")
    
    if API_KEY == "demo":
        print("WARNING: Using demo mode. Set OPENWEATHER_API_KEY environment variable for live data.")
    
    # Poll loop
    while True:
        fetch_and_update_metrics()
        time.sleep(POLL_INTERVAL)
