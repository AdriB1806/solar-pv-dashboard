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
## 💻 Running & Deploying the Dashboard

### Quick Start with Streamlit (local) ✨
Run locally for development or quick testing:

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app/dashboard.py

# Open: http://localhost:8501
```

### Deploy directly from Streamlit Cloud (quick share)
If you want the app publicly hosted with minimal ops, use Streamlit Cloud:

1. Push your repo to GitHub : your `app/dashboard.py` is the main file.
2. Visit https://share.streamlit.io and sign in with GitHub.
3. Click "New app" → select `AdriB1806/solar-pv-dashboard` → branch `main` → main file `app/dashboard.py` → Deploy.

Streamlit Cloud will build the environment from `requirements.txt`, run the app and provide a public URL (the link appears in the Cloud UI). Changes pushed to `main` auto-redeploy.

### Alternative: Docker (self-hosted, short)
Use Docker when you need a private server, more resources, or monitoring (Prometheus):

```bash
<<<<<<< HEAD
=======
# Start all services (dashboard + exporter + prometheus)
│   ├── dashboard.py           # Main Streamlit dashboard

# View:
# Dashboard: http://localhost:8501
# Prometheus UI: http://localhost:9090
```

To stop:

```bash
# Stop and remove containers
docker compose down
```

## 📁 Repository Structure

```
solar-pv-dashboard/
├── app/
│   ├── dashboard.py           # Main Streamlit dashboard
│   └── prometheus_exporter.py # Prometheus metrics exporter  
├── data/
│   └── pv_data.csv            # Solar PV data (static example)
├── examples/
│   ├── docker-setup/          # Docker + Prometheus setup
│   │   ├── docker-compose.yml
│   │   ├── Dockerfile
│   │   └── README.md
│   └── live-ingestion-api/    # Future: live data examples
├── .streamlit/                # Streamlit configuration
├── requirements.txt           # Python dependencies
├── LIVE_DATA_INTEGRATION.md   # Guide for live data
└── README.md                  # This file
```

## 💻 Running & Deploying

### Method 1: Streamlit (Recommended) ✨
**For quick deployment and sharing**

Local testing:
```bash
pip install -r requirements.txt
streamlit run app/dashboard.py
# Open http://localhost:8501
```

Deploy to Streamlit Cloud:
1. Push code to GitHub
2. Visit https://share.streamlit.io
3. Select: `AdriB1806/solar-pv-dashboard` → `main` → `app/dashboard.py`
4. Deploy (auto-updates on push)

### Method 2: Docker (Advanced) 🐳
**For self-hosting with monitoring**

```bash
cd examples/docker-setup
docker compose up -d

# View:
# - Dashboard: http://localhost:8501
# - Prometheus: http://localhost:9090
```

Stop: `docker compose down`

See `examples/docker-setup/README.md` for details.

## 🔄 Live Data Integration

This repo currently uses static CSV data. For live/real-time data:
- **Streamlit Cloud**: Poll a REST API or database
- **Docker**: Add ingestion service + database

See **[LIVE_DATA_INTEGRATION.md](LIVE_DATA_INTEGRATION.md)** for full guide.
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
>>>>>>> 836baef (refactor: reorganize repo - move Docker/Prometheus to examples/, separate static CSV from live data approaches)
# Start all services
docker compose up -d

# View at:
# - Dashboard: http://localhost:8501
# - Monitoring: http://localhost:9090
```

To stop:



In the Terminal where it's running, press:
```
Ctrl + C
```

Or run this command in the project folder:
```bash
docker-compose down
```

To rebuild after code changes use `docker compose up --build -d`.






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

This project is for educational and personal use (THI "Project PV Dashboard")

## 👨‍💻 Author

Created for solar PV system monitoring and energy flow visualization.

---

**Enjoy monitoring your solar energy! ☀️⚡**
