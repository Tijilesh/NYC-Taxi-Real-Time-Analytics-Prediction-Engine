# CP-1 Review 2 Presentation & Defense Guide

## 1. The Novel Contribution Defense
**Question from Reviewer:** *"This already exists. What are you actually doing that is new?"*

> **Your Answer:**  
> *"Sir, we are not claiming that taxi analytics or Spark processing in isolation is a novel invention. Existing literature addresses taxi demand prediction or Spark ETL separately.  
> **Our contribution is the engineering of an integrated, reproducible end-to-end system:** combining automated schema validation, a 14-rule data-quality engine with quarantine separation, spatial-temporal windowed aggregations, runtime auditability (manifest and lineage tracking), and exposing this live through a decoupled FastAPI service and React analytical interface."*

---

## 2. 5-Minute Live Demonstration Walkthrough

### Step 1: Automated Test Evidence (Terminal)
Run the automated test suite to prove data quality, analytics, and endpoints pass 100%:
```powershell
$env:PYTHONPATH="."
.\venv\Scripts\pytest.exe tests\ -v
```
*(All 6 tests pass: schema validation, 14 DQ rules, aggregations, and API health)*

### Step 2: Start the FastAPI Backend
```powershell
.\venv\Scripts\uvicorn.exe backend.app.main:app --reload --port 8000
```
- Open Swagger Docs: `http://127.0.0.1:8000/docs`
- Demonstrate the 6 decoupled API groups:
  - `GET /api/health`
  - `POST /api/pipeline/run`
  - `GET /api/pipeline/manifest`
  - `GET /api/pipeline/lineage`
  - `GET /api/analytics/overview`
  - `GET /api/data-quality/summary`
  - `GET /api/streaming/status`
  - `POST /api/prediction/demand`

### Step 3: Launch the React Dashboard
```powershell
cd frontend
npm run dev
```
- Open `http://localhost:5173/` and navigate through the 6 pages:
  1. **Dashboard**: Headline metrics (Total Trips, Revenue, Average Fare $18.42, Distance), 24h demand chart, top pickup hotspots.
  2. **Live Monitor**: Demonstrates micro-batch streaming replay (records/sec, processing latency < 2.5s, 5-minute event-time windows).
  3. **Data Quality**: Shows the **14 DQ Rules**, pass rate (~98.4%), and isolation into quarantine parquet.
  4. **Analytics**: Spatial breakdown of top pickup and drop-off zones with fare and revenue metrics.
  5. **Demand ML**: Live interactive prediction. Select Zone `#161` (Midtown Center) and Hour `18` to see immediate forecasted demand and confidence intervals.
  6. **Lineage & Manifest**: Live inspection of `manifest.json` and stage-by-stage `lineage.json`.
