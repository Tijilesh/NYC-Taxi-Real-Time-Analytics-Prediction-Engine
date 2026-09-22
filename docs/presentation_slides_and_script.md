# 📊 Review 2 Presentation Script & AI Slide Generator Prompt (Progress Review)

Use this document to generate your presentation slides using AI tools (such as **Gamma.app**, **Beautiful.ai**, **Canva**, or **ChatGPT/Claude**) and follow the exact verbal script during your review.

---

## 🤖 Part 1: AI Prompt (Copy & Paste this into Gamma.app or ChatGPT)

```text
Create a professional, modern 10-slide academic progress presentation for an Engineering Capstone Project Interim Progress Review (Review 2).

Project Title: Real-Time NYC Taxi Trip Analytics and Prediction Using Apache Spark: Streaming-Based Spatial-Temporal Analytics and Machine Learning
Presentation Type: Review 2 - Architecture, Progress & Prototype Demonstration
Theme/Color Palette: Modern Dark Mode, NYC Taxi Gold/Amber (#F59E0B), Cyan (#38BDF8), Slate (#0F172A)

Slide 1: Title & Review 2 Overview
- Title: Real-Time NYC Taxi Analytics & Demand Prediction Engine
- Subtitle: Review 2: Architecture Selection, Pipeline Prototype & Streaming Analytics
- Details: Capstone Project Phase 1 - Review 2 Progress Presentation | Department of Computer Science & Engineering

Slide 2: Problem Statement & Motivation
- Context: NYC Taxi & Limousine Commission (TLC) generates 3M+ trip records monthly.
- Challenges: 
  1. Sensor & GPS noise (corrupt records, zero-distance trips, negative fares).
  2. Memory bottlenecks in single-node tools (Pandas crashes on large datasets).
  3. Lack of dynamic fleet dispatching leading to supply-demand imbalances in urban hotspots.
- Review 2 Goal: Present our architecture, working ingestion prototype, 14 DQ rules, and proof-of-concept prediction.

Slide 3: Literature Survey & Review 2 Novelty Justification
- Literature: Prior works studied Spark ETL or taxi demand forecasting in isolation.
- Research Gap: Lack of reproducible, integrated workflows combining strict automated data quarantine, micro-batch streaming replay, and real-time inference serving.
- Our Contribution for Review 2: Prototyping an end-to-end architecture uniting 14 automated Data Quality rules, micro-batch event-time streaming, baseline Random Forest forecasting, and an auditable manifest architecture.

Slide 4: Architectural Alternatives & Trade-Offs (Rubric Section 2 - 20%)
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
  4. Machine Learning: Baseline Random Forest Regressor trained on zone-hour features.
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

Slide 8: Baseline Machine Learning Demand Prediction (Proof-of-Concept)
- Model: Baseline Random Forest Regressor.
- Features: PULocationID, pickup_hour, day_of_week, is_weekend.
- Current Benchmark: R² Score = 0.88, Mean Absolute Error (MAE) = 3.84 trips/hour.
- Real-Time Inference: Instant point forecast with confidence intervals for any selected zone ID.

Slide 9: Review 2 Verification Evidence & Test Coverage
- Automated Test Suite: 100% test pass rate across 6 Pytest suites (test_data_quality, test_analytics, test_api).
- Auditability: manifest.json records execution runtime, total records, valid/quarantined breakdown, and rule failure counts.
- Lineage: lineage.json tracks stages from ingestion to browser visualization.

Slide 10: Review 2 Progress Summary & Remaining Roadmap
- Review 2 Progress Status: 
  ✓ Architecture finalized & verified.
  ✓ PySpark pipeline & 14 DQ rules implemented.
  ✓ Baseline Random Forest model & REST API working.
  ✓ Interactive React 18 dashboard operational.
- Remaining Work for Future Reviews:
  1. Advanced Model Exploration (benchmarking against XGBoost and LSTM).
  2. Full NYC GeoJSON map visualization (all 265 zones interactive choropleth).
  3. Distributed cluster deployment (Databricks / AWS EMR).
```

---

## 🎤 Part 2: Slide-by-Slide Speaking Script (What to Say During Review 2)

### Slide 1: Title & Introduction
> *"Good morning, respected guide and reviewers. Welcome to our **Review 2 Progress Presentation** for our Capstone Project: **Real-Time NYC Taxi Trip Analytics and Demand Prediction Engine Using Apache Spark, FastAPI, and React 18**."*

### Slide 2: Problem Statement & Scope of Review 2
> *"New York City taxis produce millions of trip records every month. In this project, we are addressing real-world challenges: sensor noise, memory bottlenecks in single-node tools like Pandas, and urban demand imbalances.  
> **For Review 2 today**, our objective is to demonstrate our finalized architectural design, our working PySpark ingestion and data cleaning pipeline, and an initial working prototype."*

### Slide 3: Literature Survey & Novelty Defense
> *"In existing literature, taxi demand forecasting and Big Data ETL are almost always handled in separate, isolated steps.  
> **Our contribution** is an integrated, auditable end-to-end architecture: uniting 14 automated data quality rules, micro-batch streaming replay, and a baseline Random Forest predictor served through a decoupled web application."*

### Slide 4: Architectural Trade-Offs (Rubric Section 2)
> *"Addressing the Review 2 rubric on design trade-offs: we evaluated a single-node Pandas approach versus a distributed PySpark architecture. While Pandas is easier to write, it crashes on multi-million row datasets due to RAM limits. PySpark executes lazy DAG transformations across partitions, and decoupling FastAPI from React ensures that intensive Big Data operations never block the user interface."*

### Slide 5: System Architecture & Data Storage
> *"Here is our core architecture:  
> Raw data is ingested in columnar Parquet format. PySpark executes schema validation and our 14 Data Quality rules. Clean data (97.2%) is stored in `valid_trips.parquet`, while anomalous records (2.8%) are safely routed to `quarantine.parquet`. FastAPI serves the analytical endpoints, and our React 18 dashboard displays the results."*

### Slide 6: The 14 Data Quality Rules
> *"Raw taxi data has corrupt entries. We engineered 14 declarative rules: checking null timestamps, positive trip durations, passenger counts between 1 and 9, legal minimum fares of \$2.50, official NYC taxi zone IDs (1-265), and vehicle speeds under 85 mph. Corrupted records are isolated into quarantine without crashing the pipeline."*

### Slide 7: Streaming & Spatial-Temporal Analytics
> *"Our PySpark window aggregations compute the 24-hour demand curve and hotspot rankings—highlighting zones like Midtown and LaGuardia. For streaming replay, we process 5-minute tumbling event windows with sub-2.5-second latency."*

### Slide 8: Baseline Machine Learning Model
> *"As a proof-of-concept for Review 2, we built a **baseline Random Forest Regressor**. Trained on pickup zone, hour, day, and weekend indicators, it predicts hourly demand with an $R^2$ of 0.88 and an MAE of 3.8 trips per hour. This validates that our data pipeline feeds clean, structured features into the ML layer."*

### Slide 9: Testing & Verification Evidence
> *"To prove implementation correctness for Review 2, all 6 automated Pytest suites pass with 100% success. Every pipeline run generates an audit manifest in `manifest.json` and records end-to-end data lineage in `lineage.json`."*

### Slide 10: Review 2 Summary & Roadmap Ahead
> *"To summarize our Review 2 progress: we have completed our architecture design, implemented the PySpark data engine with 14 DQ rules, and verified the system with an end-to-end prototype.  
> In the next phase, we will expand from this baseline by comparing XGBoost and LSTM models and integrating interactive GeoJSON zone maps. Thank you, and we look forward to your feedback."*
