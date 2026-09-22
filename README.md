# NYC Taxi Real-Time Analytics & Prediction Platform

An end-to-end Big Data & Machine Learning system designed for **Streaming-Based Spatial-Temporal Analytics and Real-Time Taxi Demand Prediction** using **Apache Spark**, **FastAPI**, and **React 18**.

Built as a comprehensive Capstone Project (CP-1 / CP-2) with production architecture, data quality quarantine mechanisms, and reproducible audit tracking.

---

## 🏗️ System Architecture

```
   ┌────────────────────────────────────────────────────────┐
   │                  NYC TLC Yellow Taxi Data              │
   │           (Parquet / Micro-batch Stream Replay)         │
   └───────────────────────────┬────────────────────────────┘
                               │
                               ▼
   ┌────────────────────────────────────────────────────────┐
   │                    PySpark Engine                      │
   │   • Schema Validation & Type Casting                   │
   │   • 14 Data Quality Rules (Valid / Quarantine split)   │
   │   • Spatial & Temporal Window Aggregations             │
   │   • Feature Engineering (Duration, Speed, Zone, Hour)  │
   │   • Random Forest Demand Regression Model              │
   │   • Manifest, Audit & Lineage Tracking                 │
   └─────────────┬────────────────────────────┬─────────────┘
                 │                            │
                 ▼                            ▼
   ┌───────────────────────────┐ ┌──────────────────────────┐
   │    Analytical Storage     │ │     Audit Lineage        │
   │    (Cleaned Parquet /     │ │  (manifest.json &        │
   │     Aggregated Cache)     │ │   lineage.json)          │
   └─────────────┬─────────────┘ └────────────┬─────────────┘
                 │                            │
                 └─────────────┬──────────────┘
                               │
                               ▼
   ┌────────────────────────────────────────────────────────┐
   │                  FastAPI Middle Layer                  │
   │   • /api/health       (System & Spark connectivity)    │
   │   • /api/pipeline     (Run DAG, upload dataset, audit) │
   │   • /api/analytics    (Spatial, Temporal, Fares)       │
   │   • /api/streaming    (Live simulated micro-batch feed)│
   │   • /api/prediction   (Zone next-hour demand inference)│
   │   • /api/data-quality (14 DQ rule statistics & pass %) │
   └───────────────────────────┬────────────────────────────┘
                               │
                               ▼
   ┌────────────────────────────────────────────────────────┐
   │             React 18 Dashboard (Vite + CSS)            │
   │   • Executive Telemetry Dashboard (Trips, Revenue, Fare│
   │   • Live / Streaming Monitor (Latency & 5-min windows) │
   │   • 14 Data Quality Rules & Quarantine Inspector       │
   │   • Spatial & Temporal Analytics (Hotspot Origins)     │
   │   • ML Demand Predictor (Real-time zone inference)     │
   │   • Upload TLC Dataset & Theme Switcher (Dark/Light)   │
   └────────────────────────────────────────────────────────┘
```

---

## ⚡ Core Features

1. **Big Data Processing Core (Apache Spark 3.5)**:
   - Ingestion with strict NYC TLC schema binding.
   - 14 automated domain validation checks separating clean records from quarantine.
   - PySpark window transforms for 24-hour demand curves and zone-to-zone spatial rankings.

2. **Real-Time Streaming Replay Simulation**:
   - Replays historical TLC Parquet records ordered by pickup timestamp.
   - Tumbling 5-minute event-time windows with latency SLA gauges (< 2.5s).

3. **Machine Learning Demand Prediction**:
   - Random Forest Regressor trained on spatial-temporal features (`PULocationID`, `hour`, `day_of_week`, `is_weekend`).
   - Serves real-time inference with 95% confidence intervals and evaluation metrics ($R^2$, MAE).

4. **Decoupled FastAPI REST Service**:
   - High-throughput asynchronous endpoints with CORS middleware and automatic OpenAPI/Swagger documentation.

5. **Modern React 18 Dashboard**:
   - Signature NYC Yellow Cab aesthetic with Light & Dark mode support.
   - Interactive SVG telemetry charts, zone pickers, and lineage inspector.
   - Direct web dataset upload (`.parquet` / `.csv`).

6. **Automated Pytest Verification Suite**:
   - 100% test coverage over data quality quarantine rules, analytical calculations, and API endpoints.

---

## 📁 Repository Structure

```
├── backend/
│   ├── app/
│   │   ├── api/             # REST Route controllers (/health, /pipeline, /analytics, /prediction, /streaming)
│   │   ├── core/            # Settings and configuration
│   │   ├── schemas/         # Pydantic validation models
│   │   ├── services/        # Service layer (SparkManager, PipelineService, AnalyticsService, ML)
│   │   └── main.py          # FastAPI application entry point
│   └── requirements.txt     # Python dependencies
├── spark_engine/
│   ├── ingestion/schema.py  # Yellow Taxi schema definition
│   ├── quality/dq_rules.py  # 14 Data Quality rules engine
│   ├── analytics/           # Spatial and temporal aggregations
│   ├── ml/demand_model.py   # Random Forest demand inference model
│   └── lineage/             # Manifest & lineage generator
├── frontend/                # React 18 + Vite dashboard
│   ├── src/
│   │   ├── App.jsx          # Complete application dashboard
│   │   ├── index.css        # Curated typography, themes & glassmorphism
│   │   └── services/api.js  # REST client connecting to FastAPI
│   ├── index.html
│   └── package.json
├── data/
│   ├── sample/              # Input TLC Parquet datasets
│   ├── processed/           # Cleaned analytical Parquet records
│   └── quarantine/          # Isolated anomalous records
├── tests/                   # Automated Pytest suite
│   ├── conftest.py
│   ├── test_data_quality.py
│   ├── test_analytics.py
│   └── test_api.py
├── docs/
│   ├── alternatives_and_tradeoffs.md # Architecture comparison
│   └── cp1_review2_guide.md          # Reviewer defense guide & presentation steps
└── .gitignore
```

---

## 🚀 Quick Start Guide

### 1. Prerequisites
- Python 3.12 (with Java JDK 11+ for Apache Spark)
- Node.js (v18+) & npm

### 2. Backend Setup
```powershell
# Create and activate virtual environment
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt
pip install setuptools

# Run backend API server
$env:PYTHONPATH="."
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000 --reload
```
*Backend Swagger Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)*

### 3. Frontend Setup
```powershell
cd frontend
npm install
npm run dev
```
*Frontend Interface: [http://127.0.0.1:5173](http://127.0.0.1:5173)*

### 4. Running Automated Tests
```powershell
$env:PYTHONPATH="."
pytest tests/ -v
```
All 6 tests verify data quality boundary checks, quarantine routing, analytics, and API health.

---

## 🛡️ 14 Data Quality Rules
| Rule ID | Check | Boundary Condition |
| :--- | :--- | :--- |
| `DQ001` | Null Pickup Timestamp | `tpep_pickup_datetime IS NOT NULL` |
| `DQ002` | Null Dropoff Timestamp | `tpep_dropoff_datetime IS NOT NULL` |
| `DQ003` | Non-Positive Duration | `dropoff_datetime > pickup_datetime` |
| `DQ004` | Duration Ceiling | `duration_seconds <= 86400 (24 hrs)` |
| `DQ005` | Low Passenger Count | `passenger_count > 0` |
| `DQ006` | High Passenger Count | `passenger_count <= 9` |
| `DQ007` | Minimum Distance | `trip_distance > 0.0 miles` |
| `DQ008` | Maximum Distance | `trip_distance <= 100.0 miles` |
| `DQ009` | Base Fare Meter | `fare_amount >= $2.50` |
| `DQ010` | Maximum Fare | `fare_amount <= $1,000.00` |
| `DQ011` | Pickup Location | `PULocationID BETWEEN 1 AND 265` |
| `DQ012` | Dropoff Location | `DOLocationID BETWEEN 1 AND 265` |
| `DQ013` | Negative Tip | `tip_amount >= 0.0` |
| `DQ014` | Velocity Check | `speed <= 85.0 mph` |

---

## 📜 License
Developed for Academic Research & Demonstration purposes.
