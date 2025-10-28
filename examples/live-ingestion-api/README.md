# Live Data Integration Example 🌐

**Working example** of a solar dashboard with real-time weather data from **OpenWeatherMap API**.

## What's Included
- `dashboard_live.py` — Streamlit dashboard fetching live weather data
- `exporter_live.py` — Prometheus exporter for monitoring
- `.env.example` — Environment variable template

## Data Source
Uses **OpenWeatherMap API** (free tier) to fetch:
- ☁️ Cloud cover (affects solar output)
- 🌡️ Temperature, humidity, wind speed  
- ☀️ UV index
- 📊 5-day weather forecast

Estimates solar power output based on real weather conditions.

## Quick Start

### 1. Get API Key (Free)
- Visit https://openweathermap.org/api
- Sign up for free account
- Get your API key (free tier: 1000 calls/day)

### 2. Configure Secrets

Create `.streamlit/secrets.toml` in the **project root**:
```toml
OPENWEATHER_API_KEY = "api_key"

# Optional: Customize location
LATITUDE = 48.1351   # Munich, Germany
LONGITUDE = 11.5820
```

### 3. Run Locally

```bash
# From project root
streamlit run examples/live-ingestion-api/dashboard_live.py

# Opens at http://localhost:8501
```

### 4. Deploy to Streamlit Cloud

1. Push code to GitHub
2. Go to https://share.streamlit.io
3. Select your repo → `examples/live-ingestion-api/dashboard_live.py`
4. Add API key in **Settings → Secrets**:
   ```toml
   OPENWEATHER_API_KEY = "your_key_here"
   LATITUDE = 48.1351
   LONGITUDE = 11.5820
   ```
5. Deploy! 🚀

## How It Works

```
OpenWeatherMap API (free tier, 1000 calls/day)
        ↓
Streamlit Dashboard (caches for 5 min)
        ↓
Real-time weather → Solar power estimation
```

## Features
- ☀️ **Live weather data** from OpenWeatherMap
- ⚡ **Solar power estimation** based on conditions
- 📈 **5-day forecast** with power predictions
- 🌡️ **Temperature impact** on panel efficiency
- ☁️ **Cloud cover analysis** affecting output
- � **Daily energy estimates** (kWh)
- 🔄 **Auto-refresh** every 5 minutes (cached)

## Power Calculation Model

The dashboard estimates solar output using:
- **Cloud cover**: Reduces output proportionally
- **UV index**: Indicator of solar radiation strength
- **Time of day**: Solar angle simulation (peak at 13:00)
- **Temperature**: Panels lose ~0.5% efficiency per °C above 25°C

*Note: This is a simplified estimation model for demonstration. Real systems use more complex physics.*

## Customization

Edit `dashboard_live.py` to:
- Change location coordinates (`LAT`/`LON`)
- Adjust system capacity (default: 5kW)
- Modify cache TTL (default: 5 minutes)
- Customize power calculation formula

## Optional: Prometheus Monitoring

Run `exporter_live.py` alongside the dashboard to expose metrics for Prometheus scraping.

## API Rate Limits

- **Free tier**: 1,000 calls/day
- **Dashboard cache**: 5 minutes (288 calls/day max)
- **Well within limits** for continuous monitoring
- Add more weather metrics

## Optional: Prometheus Monitoring

If you want metrics monitoring, run the exporter:
```bash
export OPENWEATHER_API_KEY="your_key"
python exporter_live.py

# Metrics at http://localhost:8000/metrics
```

## Notes
- Free API tier: 60 calls/min, 1M calls/month
- Updates every 5 minutes (cached)
- Works on Streamlit Cloud (no server needed!)
- Demo mode available (no API key needed for testing)

See `../../LIVE_DATA_INTEGRATION.md` for more integration patterns.
