# 📊 Review 2 Presentation Script & AI Slide Generator Prompt (Progress Review)

Use this document to generate your presentation slides using AI tools (such as **Gamma.app**, **Beautiful.ai**, **Canva**, or **ChatGPT/Claude**) and follow the exact verbal script during your review.

---

## 🤖 Part 1: AI Prompt (Copy & Paste this into Gamma.app or ChatGPT)

```text
Create a professional, modern 10-slide academic progress presentation for an Engineering Capstone Project Interim Progress Review (Review 2).

Project Title: Real-Time NYC Taxi Trip Analytics and Prediction Using Apache Spark: Streaming-Based Spatial-Temporal Analytics and Machine Learning
Presentation Type: Capstone Project Phase 1 — Review 2 Progress Presentation
Domain: Big Data Engineering, Stream Processing & Applied Machine Learning
Theme/Color Palette: Modern Dark Mode, NYC Taxi Gold/Amber (#F59E0B), Cyan Accent (#38BDF8), Deep Slate (#0F172A)

Slide 1: Title & Review 2 Overview
- Title: Real-Time NYC Taxi Analytics & Demand Prediction Engine
- Subtitle: Review 2: Architecture Selection, Pipeline Implementation & Working Prototype
- Details: Final Year Capstone Project (Review 2 Progress Evaluation) | Department of Computer Science & Engineering
- Team & Guide: [Student Names], Guided by: [Guide Name], Institution: [College Name]

Slide 2: Problem Statement & Motivation
- Real-World Context: NYC Taxi & Limousine Commission (TLC) generates 3M+ trip records monthly.
- Core Challenges Addressed:
  1. Sensor Noise: GPS drift, corrupted negative fares, and 0-distance taxi trips.
  2. Memory Bottlenecks: Single-node libraries (Pandas) crash with Out-Of-Memory errors on large datasets.
  3. Dispatch Imbalances: Lack of real-time spatial demand forecasts leaves urban hotspots underserved.
- Review 2 Objective: Present our verified architecture, working PySpark ingestion with 14 Data Quality rules, and an initial working prototype.

Slide 3: Literature Survey & Review 2 Novelty Justification
- Literature Gap: Previous research explores taxi demand forecasting or Spark ETL in isolation without automated continuous quality assurance.
- Our Contribution for Review 2: Prototyping an integrated, auditable end-to-end architecture featuring:
  • An automated 14-rule declarative Data Quality engine with quarantine routing.
  • Micro-batch streaming replay with latency SLA tracking (< 2.5 seconds).
  • A baseline Random Forest demand predictor served via decoupled REST APIs.
  • Complete auditability through machine-readable JSON lineage manifests.

Slide 4: Architectural Alternatives & Trade-Offs (Rubric Section 2 - 20% Weightage)
- Comparison: Approach A (Single-Node Pandas Monolith) vs Approach B (PySpark + Decoupled FastAPI/React - Selected):
  • Memory Scalability: Pandas crashes on > 10M rows; PySpark distributes memory across partitions with lazy DAG execution.
  • Data Quality: Imperative ad-hoc loops vs declarative single-pass Spark SQL expressions.
  • Streaming: No streaming support vs PySpark Structured Streaming with 5-minute tumbling windows.
  • Decoupling: Monolith blocks UI during processing; FastAPI REST asynchronously serves React 18 dashboard.

Slide 5: End-to-End System Architecture
- Visual Architecture Workflow:
  1. Input: NYC TLC Parquet Dataset (Yellow Taxi).
  2. Computational Engine: Apache PySpark Session (Windows-optimized with Hadoop winutils).
  3. Quality Layer: 14 declarative Data Quality rules splitting rows into Clean (97.2%) vs Quarantine (2.8%).
  4. Machine Learning: Baseline Random Forest Regressor trained on Zone, Hour, Day-of-Week, and Weekend flags.
  5. API Middle-Tier: FastAPI REST endpoints with OpenAPI/Swagger documentation.
  6. Presentation Layer: React 18 dashboard with Dark/Light themes and live micro-batch stream monitor.

Slide 6: Data Origin & Storage Architecture (Where Data Comes From & Where It Stores)
- Live Data Origin:
  • Real-World Source: NYC Taxi & Limousine Commission (TLC) via in-vehicle telemetry (VeriFone / CMT meter systems).
  • Real-Time Stream Engine: Micro-batch streaming replay re-emitting events in 5-minute tumbling event-time windows.
- Storage Architecture (Medallion Pattern):
  • Raw Store (`data/sample/`): Columnar compressed Parquet files directly from TLC.
  • Clean Analytical Store (`data/processed/valid_trips.parquet`): 97.2% verified records powering analytics & ML.
  • Quarantine Store (`data/quarantine/quarantine_trips.parquet`): 2.8% anomalous rows isolated for auditing.
  • Audit Lineage Store (`artifacts/manifest.json`, `lineage.json`): Execution metadata and transformation certificates.

Slide 7: Automated 14-Rule Data Quality (DQ) Engine
- Why Raw Data Cannot Be Trusted: Sensor failures, input errors, and meter miscalibrations corrupt downstream ML models.
- Key Rule Categories:
  • Timestamps: DQ001 (Null pickup), DQ002 (Null dropoff), DQ003 (Negative trip duration).
  • Physical Bounds: DQ005 (Passenger count 1-9), DQ007 (Trip distance 0-100 miles).
  • Financial Integrity: DQ009 (Base fare >= $2.50 legal NYC minimum), DQ010 (Fare <= $1,000), DQ013 (Negative tip check).
  • Spatial & Speed: DQ011 (Valid NYC TLC zones 1-265), DQ014 (Speed <= 85 mph GPS sanity limit).
- Quarantine Isolation: Faulty records are safely routed to quarantine without interrupting streaming throughput.

Slide 8: Baseline Machine Learning Demand Prediction (Proof-of-Concept)
- Model: Baseline Random Forest Regressor.
- Input Features: PULocationID (Pickup Zone), pickup_hour (0-23), day_of_week (1-7), is_weekend (0/1).
- Current Benchmark: R² Score = 0.88 | Mean Absolute Error (MAE) = 3.84 rides/hour.
- Purpose in Review 2: Proves our data pipeline feeds clean, structured, high-quality features into predictive models.

Slide 9: Review 2 Verification Evidence & Test Coverage (Rubric Section 5)
- Automated Test Suite: 100% pass rate across 6 Pytest suites (Data Quality checks, Aggregations, API routes).
- Execution Manifest: `manifest.json` tracks pipeline execution timestamp, records processed, and DQ rule drop counts.
- Data Lineage: `lineage.json` provides end-to-end traceability from raw Parquet to dashboard visualization.

Slide 10: Review 2 Progress Summary, CP-1 Final Scope & CP-2 Roadmap
- Review 2 Completed: Architecture finalized, 14 DQ rules implemented, baseline prototype operational.
- CP-1 Final Review Updates (Upcoming):
  1. Interactive NYC Zone Map: Full GeoJSON polygon choropleth for all 265 taxi zones.
  2. Live WebSockets: Real-time telemetry pushing stream metrics to UI without manual refreshes.
  3. Formal CP-1 Report: Comprehensive test certificates and system audit documentation.
- CP-2 Next Phase Roadmap:
  1. Advanced ML Benchmarking: Random Forest vs. XGBoost vs. LSTM deep learning networks.
  2. Weather Feature Enrichment: Integrating precipitation and temperature telemetry into demand forecasting.
  3. Cloud Scaling: Migrating pipeline onto AWS EMR / Databricks distributed clusters.
```

---

## 🎤 Part 2: Slide-by-Slide Speaking Script (What to Say During Review 2)

### Slide 1: Title & Introduction
> *"Good morning, respected guide and reviewers. Welcome to our **Review 2 Progress Presentation** for our Capstone Project: **Real-Time NYC Taxi Trip Analytics and Demand Prediction Engine Using Apache Spark, FastAPI, and React 18**."*

### Slide 2: Problem Statement & Scope of Review 2
> *"New York City taxis produce millions of trip records every month. In this project, we are addressing three real-world challenges: sensor noise, memory bottlenecks in single-node tools like Pandas, and urban demand imbalances.  
> **For Review 2 today**, our objective is to demonstrate our finalized architectural design, our working PySpark ingestion and data cleaning pipeline, and an initial working prototype."*

### Slide 3: Literature Survey & Novelty Defense
> *"In existing literature, taxi demand forecasting and Big Data ETL are almost always handled in separate, isolated steps.  
> **Our contribution** is an integrated, auditable end-to-end architecture: uniting 14 automated data quality rules, micro-batch streaming replay, and a baseline Random Forest predictor served through a decoupled web application."*

### Slide 4: Architectural Trade-Offs (Rubric Section 2)
> *"Addressing the Review 2 rubric on design trade-offs: we evaluated a single-node Pandas approach versus a distributed PySpark architecture. While Pandas is easier to write, it crashes on multi-million row datasets due to RAM limits. PySpark executes lazy DAG transformations across partitions, and decoupling FastAPI from React ensures that intensive Big Data operations never block the user interface."*

### Slide 5: System Architecture Overview
> *"Here is our core workflow: Raw Parquet records enter our PySpark computational engine. Our 14 Data Quality rules validate each record, sending clean rows to our analytical store and anomalies to quarantine. Analytical aggregations and our baseline ML model feed into FastAPI, which serves our React 18 dashboard."*

### Slide 6: Data Origin & Storage Architecture
> *"To explain where data comes from and where it is stored:  
> The raw data originates from official **NYC TLC in-vehicle telemetry** recorded by VeriFone and CMT meter systems. For real-time streaming, our engine replays these records in **5-minute event-time micro-batches**.  
> We use a 3-tier storage architecture:  
> 1. Raw incoming Parquet in `data/sample/`.  
> 2. Clean data (**97.2%**) in `data/processed/valid_trips.parquet`.  
> 3. Quarantined bad data (**2.8%**) in `data/quarantine/quarantine_trips.parquet`.  
> All audit metadata is stored in `manifest.json` and `lineage.json`."*

### Slide 7: The 14 Data Quality Rules Engine
> *"Raw taxi data contains corrupt records. We engineered 14 declarative rules in PySpark SQL: checking null timestamps, positive durations, passenger counts from 1 to 9, legal minimum fares of \$2.50, official NYC zone IDs (1-265), and vehicle speeds under 85 mph. Corrupted records are safely quarantined without crashing the pipeline."*

### Slide 8: Baseline Machine Learning Model
> *"As a proof-of-concept for Review 2, we built a **baseline Random Forest Regressor**. Trained on pickup zone, hour, day, and weekend indicators, it predicts hourly demand with an $R^2$ accuracy score of 0.88 and an MAE of 3.8 trips per hour. This validates that our data pipeline feeds clean, structured features into the ML layer."*

### Slide 9: Testing & Verification Evidence
> *"To prove implementation correctness for Review 2, all 6 automated Pytest suites pass with 100% success. Every pipeline run generates an audit manifest in `manifest.json` and records end-to-end data lineage in `lineage.json`."*

### Slide 10: Review 2 Summary, CP-1 Final & CP-2 Roadmap
> *"To conclude our Review 2 progress: we have completed our architecture design, implemented the PySpark data engine with 14 DQ rules, and verified the system with a working prototype.  
> **For the CP-1 Final Review**, we will add an interactive GeoJSON NYC zone map and live WebSocket telemetry.  
> **In CP-2**, we will benchmark advanced deep learning models like XGBoost and LSTM, enrich features with real-time weather data, and deploy on a distributed AWS/Databricks cloud cluster. Thank you, and we welcome your questions."*
