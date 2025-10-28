# Solar PV Energy Dashboard 🌞⚡

A real-time dashboard for visualizing solar PV (photovoltaic) system energy production and distribution.

## 🌟 Live Demo

Visit the dashboard at: [Solar PV Dashboard on Streamlit Cloud](https://adrib1806-solar-pv-dashboard-app-dashboard-xxx.streamlit.app)

## 🚀 Hosting Options

This dashboard can be deployed in two ways:

### 1. Streamlit Cloud (Recommended for Most Users) ✅

**Best for:**
- Quick deployment
- No server management needed
- Free hosting
- Small to medium datasets
- Public dashboards

**Limitations:**
- Data must be uploaded to GitHub
- Limited computing resources
- No direct database connections

### 2. Docker Self-Hosted (Advanced Setup) �

**Best for:**
- Private deployments
- Custom server requirements
- Large datasets
- Real-time data connections
- Need for monitoring system (Prometheus)

**Limitations:**
- Requires server management
- More complex setup
- Additional hosting costs

## 📊 Features

This dashboard displays:
- **Daily Yield**: Hourly energy production with yield, exported, and self-use energy
- **Self Power Status**: Distribution between direct solar use, battery storage, and grid export
- **Real-time Meter**: Current power output gauge
- **Today's Summary**: Total energy metrics for the current day
- **Monthly Statistics**: Aggregated energy data for the month

## 🛠️ Technologies Used

- **Python**: Programming language for data processing
- **Streamlit**: Web dashboard framework
- **Plotly**: Interactive charts and visualizations
- **Pandas**: Data manipulation
- **Prometheus**: Metrics collection and monitoring
- **Docker**: Containerization for easy deployment

## 📁 Project Structure

```
solar-pv-dashboard/
├── app/
│   ├── dashboard.py           # Main Streamlit dashboard
│   └── prometheus_exporter.py # Prometheus metrics exporter
├── data/
│   └── pv_data.csv            # Solar PV data
├── prometheus/
│   └── prometheus.yml         # Prometheus configuration
├── docker-compose.yml         # Docker orchestration
├── Dockerfile                 # Dashboard container
├── Dockerfile.exporter        # Exporter container
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## � Running the Dashboard

### Quick Start with Streamlit ✨
```bash
# Install
pip install -r requirements.txt

# Run
streamlit run app/dashboard.py

# View at http://localhost:8501
```

### Alternative: Docker Setup 🐳
```bash
# Start all services
docker compose up -d

# View at:
# - Dashboard: http://localhost:8501
# - Monitoring: http://localhost:9090
```

### 🛑 How to Stop the Dashboard

In the Terminal where it's running, press:
```
Ctrl + C
```

Or run this command in the project folder:
```bash
docker-compose down
```

### 🔄 How to Restart

Simply run again:
```bash
cd ~/solar-pv-dashboard
docker-compose up
```

(No need for `--build` unless you changed code)

## 📊 Understanding Your Data

### CSV File Format

The CSV file (`data/pv_data.csv`) contains these columns:

| Column | Description |
|--------|-------------|
| Datum | Date (YYYY-MM-DD) |
| Uhrzeit | Time (HH:MM) |
| Leistung_DC_1 (W) | DC Power from solar string 1 |
| Leistung_DC_2 (W) | DC Power from solar string 2 |
| Leistung_AC (W) | AC Power output |
| Energie_Heute (kWh) | Energy produced today |
| Energie_Gesamt (kWh) | Total cumulative energy |
| Modultemperatur (°C) | Solar panel temperature |
| Umgebungstemperatur (°C) | Ambient temperature |
| Spannung_DC_1 (V) | DC Voltage string 1 |
| Spannung_DC_2 (V) | DC Voltage string 2 |

### How to Add More Data

1. Stop the dashboard (Ctrl + C)
2. Edit the file: `data/pv_data.csv`
3. Add new rows following the same format
4. Save the file
5. Restart the dashboard: `docker-compose up`

The dashboard will automatically load the new data!

## 🎨 Dashboard Features

### 1. Daily Yield Chart
- Shows energy production by hour
- Three metrics: Yield (green), Exported (orange), Self-use (light green)
- Bar chart with time labels

### 2. Self Power Status
- Donut chart showing energy distribution
- Direct Solar: Energy used immediately
- Battery: Energy stored
- Grid: Energy exported to grid

### 3. Smart Meter
- Gauge showing current power output
- Displays total energy and cost
- Real-time monitoring

### 4. Today's Summary
- Energy exported
- Direct self-use
- Total yield
- Horizontal bar charts

### 5. Monthly Statistics
- 30-day aggregated data
- Similar metrics to daily view
- Easy comparison

## 🔧 Troubleshooting

### Dashboard won't start

**Problem**: "Cannot connect" or "Address already in use"

**Solution**:
```bash
# Stop any running containers
docker-compose down

# Remove old containers
docker-compose rm -f

# Restart
docker-compose up --build
```

### Data not showing

**Problem**: Dashboard loads but no data appears

**Solution**:
1. Check if CSV file exists: `ls -la data/pv_data.csv`
2. Check CSV file content: `head data/pv_data.csv`
3. Make sure CSV file has data rows (not just headers)

### Docker not found

**Problem**: "docker: command not found"

**Solution**:
1. Install Docker Desktop
2. Open Docker Desktop application
3. Wait for it to fully start
4. Try again

### Port already in use

**Problem**: "Port 8501 is already allocated"

**Solution**:
```bash
# Find what's using the port
lsof -i :8501

# Kill the process (replace PID with actual number from above)
kill -9 PID

# Or change the port in docker-compose.yml
# Change "8501:8501" to "8502:8501"
# Then access at http://localhost:8502
```

## 📝 Customization

### Change Dashboard Port

Edit `docker-compose.yml`:
```yaml
dashboard:
  ports:
    - "8502:8501"  # Change first number
```

### Modify Energy Distribution

Edit `app/dashboard.py`, find function `calculate_energy_distribution()`:
```python
direct_solar_pct = 0.48  # Change this (0.48 = 48%)
battery_pct = 0.35       # Change this
grid_pct = 0.17          # Change this
```

### Update Colors

Edit `app/dashboard.py`, look for color codes:
- `#2E7D32` = Dark green
- `#FFA726` = Orange
- `#C8E6C9` = Light green
- `#E0E0E0` = Gray

## 🐳 Docker Commands Reference

```bash
# Start everything
docker-compose up

# Start in background (detached mode)
docker-compose up -d

# Rebuild and start
docker-compose up --build

# Stop everything
docker-compose down

# View logs
docker-compose logs

# View logs for specific service
docker-compose logs dashboard

# Follow logs in real-time
docker-compose logs -f

# List running containers
docker-compose ps

# Remove everything including volumes
docker-compose down -v
```

## 📈 Prometheus Metrics

The exporter provides these metrics:

- `pv_power_dc1_watts` - DC Power String 1
- `pv_power_dc2_watts` - DC Power String 2
- `pv_power_ac_watts` - AC Power Output
- `pv_energy_today_kwh` - Today's Energy
- `pv_energy_total_kwh` - Total Energy
- `pv_module_temperature_celsius` - Panel Temperature
- `pv_ambient_temperature_celsius` - Outside Temperature
- `pv_voltage_dc1_volts` - DC Voltage String 1
- `pv_voltage_dc2_volts` - DC Voltage String 2
- `pv_total_dc_power_watts` - Combined DC Power
- `pv_efficiency_percent` - System Efficiency
- `pv_exported_energy_kwh` - Exported Energy
- `pv_self_use_energy_kwh` - Self-Used Energy

Access metrics at: http://localhost:8000/metrics

Query in Prometheus at: http://localhost:9090

## 💡 Tips

1. **Keep Docker Desktop running** - The dashboard needs it
2. **Refresh browser** - If data doesn't update, refresh the page
3. **Check Terminal output** - Look for error messages
4. **Use wide screen** - Dashboard is optimized for wide displays
5. **Export data** - You can download charts as PNG from Plotly menu

## 🆘 Getting Help

If something doesn't work:

1. Check Terminal output for error messages
2. Verify Docker Desktop is running
3. Make sure all files are in correct folders
4. Check CSV file format matches expected structure
5. Try rebuilding: `docker-compose up --build`

## 📄 License

This project is for educational and personal use.

## 👨‍💻 Author

Created for solar PV system monitoring and energy flow visualization.

---

**Enjoy monitoring your solar energy! ☀️⚡**
