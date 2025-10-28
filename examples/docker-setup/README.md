# Docker Setup with Prometheus Monitoring 🐳

Run the solar dashboard locally with Docker Compose, including Prometheus metrics collection.

## What's Included

- **Streamlit Dashboard** (port 8501)
- **Prometheus Exporter** (port 8000)
- **Prometheus Server** (port 9090)

## Quick Start

```bash
# From project root
cd examples/docker-setup

# Start all services
docker compose up -d

# View:
# - Dashboard: http://localhost:8501
# - Prometheus: http://localhost:9090
# - Metrics: http://localhost:8000/metrics
```

## Stop Services

```bash
docker compose down
```

## When to Use This

✅ **Use Docker when you need:**
- Prometheus monitoring and alerting
- Self-hosted private deployment
- Consistent environment across machines
- Local testing before production

❌ **Skip Docker if you just want:**
- Quick local testing → Use `streamlit run app/dashboard.py`
- Public deployment → Use Streamlit Cloud

## Files

- `docker-compose.yml` - Orchestrates all services
- `Dockerfile` - Dashboard container
- `Dockerfile.exporter` - Metrics exporter container
- `prometheus/prometheus.yml` - Prometheus config
- `start.sh` / `stop.sh` - Helper scripts

## Data Source

Reads from `../../data/pv_data.csv` (static CSV data)

For live data integration, see `../live-ingestion-api/`
