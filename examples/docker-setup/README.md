# Docker Setup (Static CSV Data)

This folder contains Docker configuration for running the dashboard locally with static CSV data.

## What's included
- `docker-compose.yml` - Orchestrates dashboard, exporter, and Prometheus
- `Dockerfile` - Dashboard container build
- `Dockerfile.exporter` - Prometheus exporter container build
- `prometheus/` - Prometheus configuration
- `start.sh` / `stop.sh` - Helper scripts

## Quick Start
```bash
cd examples/docker-setup
docker compose up -d

# View at:
# Dashboard: http://localhost:8501
# Prometheus: http://localhost:9090
```

## Stop
```bash
docker compose down
```

## When to use this
- Testing locally before Streamlit Cloud deployment
- Running with Prometheus monitoring
- Self-hosted private deployment
- Learning Docker orchestration

This setup reads from `../../data/pv_data.csv` (static data).
