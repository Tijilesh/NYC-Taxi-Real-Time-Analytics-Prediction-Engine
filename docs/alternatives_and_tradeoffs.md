# Alternatives and Trade-Offs (CP-1 Review 2 Rubric - 20%)

## Evaluation Criteria
1. **Scalability & Memory Efficiency**: Ability to process millions of monthly trip records without driver Out-Of-Memory (OOM) failures.
2. **Data Quality & Quarantine Isolation**: Declarative, vectorizable rule evaluation and partition routing.
3. **Execution Lineage & Auditability**: Traceability from raw input batch through cleaning, validation, and analytics.
4. **Modularity & Decoupling**: Separation of compute-heavy analytics from user-facing serving interfaces.

---

## Alternative 1: Single-Node Pandas + Monolithic Web Framework
- **Architecture**: Raw CSV/Parquet $\rightarrow$ Pandas DataFrame $\rightarrow$ Single Flask/Streamlit application.
- **Advantages**:
  - Simpler initial scripting.
  - No Java/Hadoop runtime dependencies.
- **Critical Limitations**:
  - **Memory Bottleneck**: Pandas loads entire datasets in-memory and duplicates buffers during aggregations, failing on monthly TLC datasets (>10M records).
  - **Lack of Streaming Architecture**: Cannot handle continuous micro-batch window operations with watermarks.
  - **Tight Coupling**: Heavy compute blocks API threads, degrading user response latency.

---

## Alternative 2: PySpark Engine + Decoupled FastAPI & React (Selected Architecture)
- **Architecture**:
  - **Big Data Compute Layer**: PySpark with lazy DAG evaluation, distributed partition memory, and structured event-time windows.
  - **Analytical Storage**: Columnar Parquet for aggregated metrics + SQLite/MySQL for execution metadata.
  - **Application Middle-Layer**: FastAPI for high-throughput asynchronous REST serving.
  - **Frontend Interface**: React 18 for reactive KPIs, live streaming visualization, and interactive ML queries.
- **Why Selected**:
  - Meets real-world TLC data scale without memory saturation.
  - Enables strict separation of valid vs. quarantined records via declarative rules.
  - Provides decoupled, audit-ready manifests and lineage per execution.
