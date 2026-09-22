# 📊 CP-1 Review 2 Presentation Script & AI Slide Generator Prompt

Use this document to generate your presentation slides using AI tools (such as **Gamma.app**, **Beautiful.ai**, **Canva**, or **ChatGPT/Claude**) and follow the exact verbal script during your review.

---

## 🤖 Part 1: AI Prompt (Copy & Paste this into Gamma.app or ChatGPT)

```text
Create a professional, modern 10-slide academic presentation for a Final Year Engineering Capstone Project Review (CP-1 Review 2). 

Project Title: Real-Time NYC Taxi Trip Analytics and Prediction Using Apache Spark: Streaming-Based Spatial-Temporal Analytics and Machine Learning
Domain: Big Data Engineering, Stream Processing & Applied Machine Learning
Theme/Color Palette: Modern Dark Mode, NYC Taxi Gold/Amber (#F59E0B), Cyan (#38BDF8), Slate (#0F172A)

Slide 1: Title & Project Overview
- Title: Real-Time NYC Taxi Analytics & Demand Prediction Engine
- Subtitle: Scalable PySpark Stream Processing, Data Quality Quarantine, and Machine Learning
- Student Names, Department, Guide Name, Institution Name, Date

Slide 2: Problem Statement & Motivation
- Context: NYC Taxi & Limousine Commission (TLC) generates 3M+ trip records monthly.
- Challenges: 
  1. Sensor & GPS noise (corrupt records, zero-distance trips, negative fares).
  2. Memory bottlenecks in single-node tools (Pandas crashes on large datasets).
  3. Lack of dynamic fleet dispatching leading to supply-demand imbalances in urban hotspots.
- Goal: Build an integrated, testable, end-to-end platform from data ingestion to live dashboard serving.

Slide 3: Literature Survey & The "Novelty" Defense
- Literature: Prior works studied Spark ETL or taxi demand forecasting in isolation.
- Research Gap: Lack of reproducible, integrated workflows combining strict automated data quarantine, micro-batch streaming replay, and real-time inference serving.
- Our Novel Contribution: Engineering an end-to-end pipeline uniting 14 automated Data Quality rules, micro-batch event-time streaming, Random Forest demand forecasting, and an auditable manifest architecture.

Slide 4: Architectural Alternatives & Trade-Offs (Rubric Section 2)
- Compare Approach A (Single-Node Pandas + Monolith) vs Approach B (PySpark + Decoupled FastAPI/React - Selected).
- Criteria Table:
  • Memory Scalability: Pandas crashes (OOM); PySpark scales horizontally across partitions.
  • Data Quality: Ad-hoc loops vs declarative single-pass DAG filtering.
  • Streaming: No streaming support vs PySpark Structured 5-min tumbling windows.
  • Decoupling: Monolith freezes UI vs asynchronous REST middle-layer.

Slide 5: End-to-End System Architecture Diagram
- Visual Workflow:
  1. Input: NYC TLC Parquet Dataset (Yellow Taxi).
  2. PySpark Engine: Schema validation, 14 DQ checks, windowed spatial/temporal aggregations.
  3. Storage: valid_trips.parquet (97.2% clean) and quarantine_trips.parquet (2.8% isolated).
  4. Machine Learning: Random Forest Regressor trained on zone-hour features.
  5. API Layer: FastAPI REST backend (Swagger endpoints).
  6. Frontend: React 18 dashboard (Dark/Light themes, live streaming monitor).

Slide 6: The 14 Automated Data Quality (DQ) Rules Engine
- Explanation of why raw data cannot be trusted.
- Table of Key Checks:
  • Timestamps: DQ001 (Null pickup), DQ002 (Null dropoff), DQ003 (Negative duration).
  • Operational bounds: DQ005 (Passenger count 1-9), DQ007 (Distance 0-100 miles).
  • Financial bounds: DQ009 (Base fare >= $2.50), DQ010 (Fare <= $1000), DQ013 (Negative tip).
  • Geography & Velocity: DQ011 (Valid TLC zones 1-265), DQ014 (Speed <= 85 mph).
- Isolation: Faulty records routed to quarantine without interrupting stream throughput.

Slide 7: Spatial-Temporal Analytics & Ingestion Replay
- Spatial Analytics: Identification of top pickup hotspots (Zone 161 Midtown, Zone 237 Upper East, Zone 138 LaGuardia Airport).
- Temporal Patterns: 24-hour demand distribution showing morning and evening commuter peaks.
- Streaming Replay Engine: Simulating live streams via 5-minute event-time micro-batches with < 2.5s latency SLA.

Slide 8: Machine Learning Demand Prediction (CP-1 to CP-2 Bridge)
- Model: Random Forest Regressor.
- Features: PULocationID, pickup_hour, day_of_week, is_weekend.
- Performance Metrics: R² Accuracy Score = 0.88, Mean Absolute Error (MAE) = 3.84 trips/hour.
- Real-Time Inference: Instant forecast with 95% confidence intervals for any zone ID and target hour.

Slide 9: Testing Evidence & Audit Lineage (Rubric Section 5)
- Automated Test Suite: 100% test pass rate across 6 Pytest suites (test_data_quality, test_analytics, test_api).
- Auditability: manifest.json records execution runtime, total records, valid/quarantined breakdown, and rule failure counts.
- Lineage: lineage.json tracks stages from ingestion to browser visualization.

Slide 10: Conclusion & CP-2 Roadmap
- CP-1 Summary: Working vertical slice fully operational, verified, and pushed to GitHub.
- CP-2 Next Steps:
  1. Multi-model benchmarking (Random Forest vs XGBoost vs LSTM).
  2. Interactive GeoJSON choropleth map visualization for all 265 NYC taxi zones.
  3. Multi-node cloud deployment (AWS EMR / Databricks).
```

---

## 🎤 Part 2: Slide-by-Slide Speaking Script (What to Say During the Review)

### Slide 1: Title
> *"Good morning, respected guide and reviewers. Today we present our Capstone Project 1: **Real-Time NYC Taxi Trip Analytics and Demand Prediction Engine Using Apache Spark, FastAPI, and React 18**."*

### Slide 2: Problem Statement
> *"New York City taxis generate millions of trip records each month. However, real-world fleet managers face two critical bottlenecks: first, sensor and meter data contains significant noise, such as negative fares and zero-distance trips; second, traditional Python tools like Pandas run into Out-Of-Memory errors when processing datasets of this scale. Our project addresses this by developing a robust, scalable pipeline that cleans, validates, analyzes, and predicts trip demand."*

### Slide 3: Novelty & Research Contribution
> *"If we look at existing literature, researchers have explored taxi demand forecasting or Spark ETL independently.  
> **Our contribution is the engineering of an integrated, auditable end-to-end software system**: we combine an automated 14-rule data-quality quarantine mechanism, micro-batch streaming replay, spatial-temporal analytics, and real-time Random Forest demand inference, served directly through a decoupled web application."*

### Slide 4: Architectural Trade-Offs (Rubric 20%)
> *"For our architecture, we rigorously compared two approaches:  
> A single-node Pandas monolith versus a decoupled PySpark and FastAPI architecture. While Pandas is simpler for small scripts, it fails completely on multi-million row datasets. PySpark distributes memory across partitions with lazy DAG execution. Furthermore, decoupling FastAPI from React ensures that heavy data computations in the background never freeze the user's dashboard."*

### Slide 5: System Architecture & Data Storage
> *"Here is our end-to-end architecture:  
> Raw data is ingested in columnar **Apache Parquet** format. PySpark executes schema validation and our 14 Data Quality rules. Clean data (97.2%) is stored in `valid_trips.parquet`, while anomalous records (2.8%) are safely routed to `quarantine.parquet`. FastAPI serves the analytical endpoints, and our React 18 interface provides live telemetry."*

### Slide 6: The 14 Data Quality Rules
> *"To ensure data integrity, every row must pass 14 domain boundary rules. For instance: timestamps must be non-null and duration must be positive; passenger count must be between 1 and 9; base fares must satisfy the NYC legal minimum of \$2.50; location IDs must fall within the 265 official TLC zones; and speeds above 85 mph are flagged as GPS anomalies. Failed rows are isolated into quarantine without crashing the pipeline."*

### Slide 7: Streaming & Spatial-Temporal Analytics
> *"On the analytical side, our PySpark window functions compute the 24-hour demand pattern and hotspot rankings. We identify top origin zones such as Midtown Center and LaGuardia Airport. For streaming, we replay official TLC Parquet records into 5-minute tumbling event windows, maintaining sub-2.5 second latency."*

### Slide 8: Machine Learning Demand Prediction
> *"As a bridge into CP-2, we implemented an initial **Random Forest Regressor** model. By engineering features like pickup location, hour of the day, day of the week, and weekend indicators, the model predicts passenger demand for any zone in real time with an $R^2$ accuracy score of 0.88 and a Mean Absolute Error of under 4 trips per hour."*

### Slide 9: Testing & Verification Evidence
> *"Our project is backed by verified testing evidence. All 6 automated Pytest suites pass with 100% success, verifying our DQ quarantine logic, analytics calculations, and API endpoints. Additionally, every pipeline execution writes an audit certificate to `manifest.json` and records transformation stages in `lineage.json`."*

### Slide 10: Conclusion & Next Steps
> *"In conclusion, for CP-1 Review 2 we have delivered a fully functional vertical slice from raw ingestion to web dashboard. For CP-2, we will expand this foundation with XGBoost/LSTM model comparisons and interactive GeoJSON map polygons. Thank you, and we are ready for your questions."*
