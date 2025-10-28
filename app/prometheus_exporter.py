"""
Prometheus exporter for Solar PV metrics
Exposes metrics from the CSV data in Prometheus format
"""

from prometheus_client import start_http_server, Gauge, Counter
import pandas as pd
import time
from datetime import datetime

# Define Prometheus metrics
pv_power_dc1 = Gauge('pv_power_dc1_watts', 'DC Power from String 1 in Watts')
pv_power_dc2 = Gauge('pv_power_dc2_watts', 'DC Power from String 2 in Watts')
pv_power_ac = Gauge('pv_power_ac_watts', 'AC Power Output in Watts')
pv_energy_today = Gauge('pv_energy_today_kwh', 'Energy produced today in kWh')
pv_energy_total = Gauge('pv_energy_total_kwh', 'Total energy produced in kWh')
pv_module_temp = Gauge('pv_module_temperature_celsius', 'Module temperature in Celsius')
pv_ambient_temp = Gauge('pv_ambient_temperature_celsius', 'Ambient temperature in Celsius')
pv_voltage_dc1 = Gauge('pv_voltage_dc1_volts', 'DC Voltage String 1 in Volts')
pv_voltage_dc2 = Gauge('pv_voltage_dc2_volts', 'DC Voltage String 2 in Volts')

# Calculated metrics
pv_total_dc_power = Gauge('pv_total_dc_power_watts', 'Total DC Power from both strings')
pv_efficiency = Gauge('pv_efficiency_percent', 'System efficiency (AC/DC power ratio)')
pv_exported_energy = Gauge('pv_exported_energy_kwh', 'Energy exported to grid')
pv_self_use_energy = Gauge('pv_self_use_energy_kwh', 'Energy used directly')

def load_pv_data():
    """Load PV data from CSV"""
    try:
        df = pd.read_csv('data/pv_data.csv')
        df.columns = df.columns.str.strip()
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return None

def update_metrics():
    """Update Prometheus metrics with latest data"""
    df = load_pv_data()
    
    if df is None or df.empty:
        return
    
    # Get the latest row (most recent data)
    latest = df.iloc[-1]
    
    # Update basic metrics
    pv_power_dc1.set(latest['Leistung_DC_1 (W)'])
    pv_power_dc2.set(latest['Leistung_DC_2 (W)'])
    pv_power_ac.set(latest['Leistung_AC (W)'])
    pv_energy_today.set(latest['Energie_Heute (kWh)'])
    pv_energy_total.set(latest['Energie_Gesamt (kWh)'])
    pv_module_temp.set(latest['Modultemperatur (°C)'])
    pv_ambient_temp.set(latest['Umgebungstemperatur (°C)'])
    pv_voltage_dc1.set(latest['Spannung_DC_1 (V)'])
    pv_voltage_dc2.set(latest['Spannung_DC_2 (V)'])
    
    # Calculate and update derived metrics
    total_dc = latest['Leistung_DC_1 (W)'] + latest['Leistung_DC_2 (W)']
    pv_total_dc_power.set(total_dc)
    
    # Calculate efficiency (AC/DC ratio)
    if total_dc > 0:
        efficiency = (latest['Leistung_AC (W)'] / total_dc) * 100
        pv_efficiency.set(efficiency)
    else:
        pv_efficiency.set(0)
    
    # Calculate exported and self-use energy (40/60 split)
    total_energy = df['Energie_Heute (kWh)'].sum()
    pv_exported_energy.set(total_energy * 0.40)
    pv_self_use_energy.set(total_energy * 0.60)
    
    print(f"[{datetime.now()}] Metrics updated - AC Power: {latest['Leistung_AC (W)']}W, "
          f"Today: {latest['Energie_Heute (kWh)']}kWh")

if __name__ == '__main__':
    # Start Prometheus metrics server on port 8000
    print("Starting Prometheus exporter on port 8000...")
    start_http_server(8000)
    
    print("Exporter running. Metrics available at http://localhost:8000/metrics")
    
    # Update metrics every 30 seconds
    while True:
        try:
            update_metrics()
            time.sleep(30)
        except KeyboardInterrupt:
            print("\nShutting down exporter...")
            break
        except Exception as e:
            print(f"Error updating metrics: {e}")
            time.sleep(30)
