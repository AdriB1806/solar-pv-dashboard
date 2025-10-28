# Live Data Integration — solar-pv-dashboard

This short guide explains how to integrate continuously updating (live) data into this repository's dashboard. It covers two deployment patterns that match this workspace:

- Streamlit (Streamlit Cloud or local `streamlit run`) — recommended for quick/public deployments.
- Docker / self-hosted (with optional Prometheus) — recommended for private, high-throughput, or monitored deployments.

Files in this workspace we will use

<<<<<<< HEAD
- `app/dashboard.py` — main Streamlit app (this repo's UI). 
- `data/pv_data.csv` — example static CSV used today. 
- `app/prometheus_exporter.py` — exporter that exposes Prometheus metrics.
- `Dockerfile`, `Dockerfile.exporter`, `docker-compose.yml` — Docker builds and orchestration for self-hosting.
- `.streamlit/config.toml` — streamlit server settings.
=======
## Files in this workspace
- `app/dashboard.py` — main Streamlit UI (change data-loading functions here)
- `data/pv_data.csv` — example static CSV (do NOT write live data here for Streamlit Cloud)
- `app/prometheus_exporter.py` — optional exporter to expose metrics
- `examples/docker-setup/` — Docker + Prometheus setup for static CSV
- `examples/live-ingestion-api/` — (future) live data ingestion examples
- `.streamlit/config.toml` — Streamlit settings
>>>>>>> 836baef (refactor: reorganize repo - move Docker/Prometheus to examples/, separate static CSV from live data approaches)

---

## Streamlit (Cloud or local) — simple, recommended

High-level approach

- The dashboard UI code in `app/dashboard.py` stays , but we should change how it loads data.
- We wont rely on writing/updating files in the repo when deployed to Streamlit Cloud (the filesystem there is ephemeral and we should not push large/continually-changing files to GitHub).
- Best option: wenmake the dashboard load from a stable external source (REST API or a database). Use caching with a short TTL so Streamlit refreshes the data periodically.

Small example: polling a REST API

```python
import pandas as pd
import streamlit as st
import requests

@st.cache_data(ttl=5)  # refresh every 5 seconds
def load_live_data(url):
    r = requests.get(url, timeout=5)
    r.raise_for_status()
    return pd.DataFrame(r.json())

df = load_live_data("https://your-ingestion.example.com/api/latest")
```

Notes and tradeoffs

- Polling interval (TTL): choose 1–10s for near-real-time, or larger to save resources.
- Streamlit Cloud enforces resource limits — don't poll very frequently from many users.
- Keep expensive aggregation on the server side (ingestor or DB) and let Streamlit request a small summary endpoint.

Where to host the data source

- REST API (FastAPI/Flask) that returns recent values or pre-aggregated results.
- Database (Postgres, InfluxDB) that Streamlit queries with a short TTL cache.
- Prometheus: Streamlit can query Prometheus HTTP API for metrics (good for monitoring/time-series analytics).

Quick deployment via Streamlit Cloud

1. Push code that reads from the API (only code and config) to GitHub.
2. On Streamlit Cloud, set the repo and main file (`app/dashboard.py`). Cloud will build from `requirements.txt` and deploy.
3. The public URL updates automatically on pushes.

---


## 2) Prometheus (metrics-first, good for monitoring & history)
What is Prometheus?
- Prometheus is a pull-based time-series monitoring system: it scrapes HTTP endpoints (exporters) and stores metrics for queries, alerting, and history.
- Use it when you need reliable time-series storage, alerts, and easy metric aggregation.

How Prometheus fits here
- Device or exporter exposes metrics (e.g., `pv_power_ac_watts`, `pv_energy_today_kwh`) at `/metrics`.
- Prometheus scrapes the exporter on a schedule and stores data.
- Streamlit queries Prometheus HTTP API (`/api/v1/query` or `/api/v1/query_range`) to get latest values or ranges and render charts.

Streamlit <> Prometheus (example)
```python
import requests, pandas as pd

PROM = "http://prometheus:9090"

def prom_query(query):
    r = requests.get(f"{PROM}/api/v1/query", params={"query": query}, timeout=5); r.raise_for_status()
    res = r.json()["data"]["result"]
    rows = []
    for item in res:
        rows.append({**item.get("metric", {}), "value": float(item["value"][1])})
    return pd.DataFrame(rows)
```

When to use Prometheus
- You need historical time-series, dashboards for ops, or alerting.
- You run self-hosted or have a reachable Prometheus for Streamlit Cloud (via proxy or public endpoint).

Tradeoffs vs REST API
- Prometheus is excellent for metrics and history, less suited as a CRUD store for arbitrary records.
- It adds extra infra but gives robust retention, query power, and alerts.

---



## Docker / Self-hosted — flexible and powerful

High-level approach

- Run an ingestion service that accepts live data from devices (webhooks, MQTT, TCP) and stores it in a database or in-memory store (Redis, InfluxDB).
- Run the Streamlit app as another service that queries the DB/API. Optionally run Prometheus + exporter for metrics and alerting.
- Use `docker-compose.yml` to orchestrate services on a single host.

Minimal ingestion example (FastAPI)

```python
# app/ingestor/main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlalchemy as sa

app = FastAPI()

class Sample(BaseModel):
    timestamp: str
    power_ac_w: float

@app.post('/api/ingest')
async def ingest(sample: Sample):
    # validate and write to DB (psuedocode)
    # db.insert({...})
    return {"ok": True}
```

Docker-compose sketch (add to `docker-compose.yml` or extend)

```yaml
services:
  ingest:
    build: ./app/ingestor
    ports: ['8001:8000']

  postgres:
    image: postgres:15
    environment:
      POSTGRES_PASSWORD: example

  streamlit:
    build: .
    command: streamlit run app/dashboard.py
    ports: ['8501:8501']
    depends_on: ['ingest', 'postgres']

  prometheus:
    image: prom/prometheus
    volumes: ['./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml']
    ports: ['9090:9090']
```

How Streamlit reads live data here

- Streamlit calls the local DB or ingestion API using the same patterns described above.
- Because services are local, you can poll more frequently (milliseconds to seconds) depending on host resources.

Advantages of Docker/self-hosted

- Persistent storage and control over resource limits
- Ability to run collectors, brokers (Redis/Kafka), time-series DBs (InfluxDB) and Prometheus
- Easier to secure and integrate with on-prem devices

---

## Practical checklist for this repository

1. Decide the data ingestion approach: REST API + DB or Prometheus metrics or direct CSV updates.
2. If using Streamlit Cloud: implement an API endpoint and change `app/dashboard.py` to `load_live_data(url)` with `@st.cache_data(ttl=...)`.
3. If self-hosting: add an `ingest` service and a DB/Redis/Influx service in `docker-compose.yml`. Modify `app/dashboard.py` to query the DB or API at short TTLs.
4. For Prometheus: keep or extend `app/prometheus_exporter.py` to expose metrics, and configure `prometheus/prometheus.yml` to scrape it. Streamlit can query Prometheus HTTP API for charts.
5. Implement authentication for ingestion endpoints (API keys / TLS) and protect public endpoints.

## Quick local testing

- Run ingestion mock:

```bash
# run a simple API mock (uvicorn)
uvicorn app.ingestor.main:app --reload --port 8001
```

- Run streamlit locally:

```bash
pip install -r requirements.txt
streamlit run app/dashboard.py
```

## Notes and best practices

- Do not commit live data files to GitHub.
- Use TTL caching and server-side aggregation to reduce load on Streamlit.
- Persist raw data in a durable store for historical analysis (DB or TSDB).
- Monitor performance and adjust poll intervals.
- Secure ingestion endpoints and use HTTPS in production.

---

If you want, I can:

- Add a minimal `app/ingestor` FastAPI scaffold and a `docker-compose` snippet to this repo.
- Patch `app/dashboard.py` with an optional `load_from_api()` implementation and a config variable for the API URL.

Tell me which option to scaffold first: `polling API` (Streamlit Cloud friendly) or `full Docker ingestion + DB`.
