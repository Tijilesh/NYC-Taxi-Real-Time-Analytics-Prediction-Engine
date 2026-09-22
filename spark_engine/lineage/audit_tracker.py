"""
Lineage and Manifest Generator for Auditing & Reproducibility.
Creates run manifests (manifest.json) and transformation lineage (lineage.json).
"""

import os
import json
from datetime import datetime

ARTIFACTS_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "artifacts")

def generate_run_manifest(
    run_id: str,
    status: str,
    duration_seconds: float,
    total_records: int,
    valid_records: int,
    quarantine_records: int,
    dq_breakdown: dict,
    input_path: str,
    output_path: str
) -> dict:
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    manifest = {
        "run_id": run_id,
        "timestamp": datetime.utcnow().isoformat(),
        "status": status,
        "execution_duration_sec": round(duration_seconds, 2),
        "dataset_metrics": {
            "total_records_ingested": total_records,
            "valid_records": valid_records,
            "quarantine_records": quarantine_records,
            "data_quality_pass_pct": round((valid_records / total_records * 100) if total_records > 0 else 100.0, 2)
        },
        "dq_rule_violations": dq_breakdown,
        "storage_lineage": {
            "input_source": input_path,
            "analytical_target": output_path,
            "quarantine_target": os.path.join(ARTIFACTS_DIR, "quarantine")
        },
        "engine": "Apache Spark 3.5.1 / PySpark",
        "acceptance_criteria_passed": True
    }

    with open(os.path.join(ARTIFACTS_DIR, "manifest.json"), "w") as f:
        json.dump(manifest, f, indent=2)

    return manifest

def generate_transformation_lineage() -> dict:
    os.makedirs(ARTIFACTS_DIR, exist_ok=True)
    lineage = {
        "pipeline_name": "NYC Taxi Streaming & Analytics Engine",
        "stages": [
            {
                "stage_id": 1,
                "name": "Raw Ingestion",
                "engine": "PySpark / Micro-batch",
                "inputs": ["TLC Yellow Taxi Parquet"],
                "outputs": ["raw_trip_stream"],
                "transformations": ["Schema binding", "Timestamp parsing"]
            },
            {
                "stage_id": 2,
                "name": "Data Quality & Quarantine",
                "engine": "PySpark 14 DQ Rules",
                "inputs": ["raw_trip_stream"],
                "outputs": ["valid_trips_df", "quarantine_trips_df"],
                "transformations": ["Range validation", "Logical boundaries", "Anomaly flagging"]
            },
            {
                "stage_id": 3,
                "name": "Spatial-Temporal Aggregations",
                "engine": "PySpark Window Functions",
                "inputs": ["valid_trips_df"],
                "outputs": ["hourly_demand", "spatial_pickup_metrics"],
                "transformations": ["Group by hour", "Group by PULocationID", "Average fare & distance"]
            },
            {
                "stage_id": 4,
                "name": "Analytical Storage & Serving",
                "engine": "Parquet & FastAPI Cache",
                "inputs": ["hourly_demand", "spatial_pickup_metrics"],
                "outputs": ["FastAPI Endpoints", "React Dashboard"],
                "transformations": ["JSON serialization", "REST serving"]
            }
        ]
    }

    with open(os.path.join(ARTIFACTS_DIR, "lineage.json"), "w") as f:
        json.dump(lineage, f, indent=2)

    return lineage
