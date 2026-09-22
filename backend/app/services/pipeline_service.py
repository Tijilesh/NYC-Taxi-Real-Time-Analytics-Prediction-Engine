"""
Pipeline Service: Executes PySpark ETL & Data Quality over NYC TLC Parquet data.
"""

import os
import time
import uuid
import pandas as pd
from datetime import datetime
from pyspark.sql import functions as F

from backend.app.core.config import settings
from backend.app.services.spark_service import SparkManager
from spark_engine.quality.dq_rules import apply_data_quality_rules, DQ_RULES_METADATA
from spark_engine.lineage.audit_tracker import generate_run_manifest, generate_transformation_lineage

class PipelineService:
    @classmethod
    def get_sample_path(cls) -> str:
        sample_path = os.path.join(settings.DATA_SAMPLE_DIR, "yellow_tripdata_sample.parquet")
        if not os.path.exists(sample_path):
            raise FileNotFoundError(f"Input taxi parquet dataset not found at {sample_path}")
        return sample_path

    @classmethod
    def execute_pipeline(cls, sample_size: int = 10000) -> dict:
        start_time = time.time()
        run_id = f"RUN-{uuid.uuid4().hex[:8].upper()}"

        spark = SparkManager.get_spark()
        sample_file = cls.get_sample_path()

        # Read parquet directly via PySpark
        raw_df = spark.read.parquet(sample_file).limit(sample_size)
        total_records = raw_df.count()

        # Apply 14 Data Quality Rules
        valid_df, quarantine_df = apply_data_quality_rules(raw_df)
        valid_df.cache()
        quarantine_df.cache()

        valid_count = valid_df.count()
        quarantine_count = quarantine_df.count()

        # Calculate rule violation breakdowns
        dq_breakdown = {
            "DQ001": 0,
            "DQ002": 0,
            "DQ003": int(quarantine_df.filter("duration_seconds <= 0").count()),
            "DQ004": int(quarantine_df.filter("duration_seconds > 86400").count()),
            "DQ005": int(quarantine_df.filter("passenger_count <= 0").count()),
            "DQ006": int(quarantine_df.filter("passenger_count > 9").count()),
            "DQ007": int(quarantine_df.filter("trip_distance <= 0").count()),
            "DQ008": int(quarantine_df.filter("trip_distance > 100").count()),
            "DQ009": int(quarantine_df.filter("fare_amount < 2.50").count()),
            "DQ010": int(quarantine_df.filter("fare_amount > 1000").count()),
            "DQ011": int(quarantine_df.filter("PULocationID < 1 OR PULocationID > 265").count()),
            "DQ012": int(quarantine_df.filter("DOLocationID < 1 OR DOLocationID > 265").count()),
            "DQ013": int(quarantine_df.filter("tip_amount < 0").count()),
            "DQ014": int(quarantine_df.filter("speed_mph > 85").count()),
        }

        # Write clean and quarantine datasets
        processed_path = os.path.join(settings.DATA_PROCESSED_DIR, "valid_trips.parquet")
        os.makedirs(settings.DATA_PROCESSED_DIR, exist_ok=True)
        # Select key analytical columns and save
        valid_cols = [
            "VendorID", "tpep_pickup_datetime", "tpep_dropoff_datetime", 
            "passenger_count", "trip_distance", "PULocationID", "DOLocationID", 
            "fare_amount", "tip_amount", "total_amount", "duration_seconds", "speed_mph"
        ]
        available_cols = [c for c in valid_cols if c in valid_df.columns]
        valid_df.select(available_cols).toPandas().to_parquet(processed_path, index=False)

        quarantine_path = os.path.join(settings.DATA_QUARANTINE_DIR, "quarantine_trips.parquet")
        os.makedirs(settings.DATA_QUARANTINE_DIR, exist_ok=True)
        if quarantine_count > 0:
            quarantine_df.select(available_cols).toPandas().to_parquet(quarantine_path, index=False)

        duration = time.time() - start_time

        # Generate Manifest & Lineage
        manifest = generate_run_manifest(
            run_id=run_id,
            status="SUCCESS",
            duration_seconds=duration,
            total_records=total_records,
            valid_records=valid_count,
            quarantine_records=quarantine_count,
            dq_breakdown=dq_breakdown,
            input_path=sample_file,
            output_path=processed_path
        )
        generate_transformation_lineage()

        return {
            "run_id": run_id,
            "status": "SUCCESS",
            "duration_seconds": round(duration, 2),
            "total_records": total_records,
            "valid_records": valid_count,
            "quarantine_records": quarantine_count,
            "data_quality_pass_pct": round((valid_count / total_records * 100) if total_records > 0 else 100.0, 2),
            "dq_breakdown": dq_breakdown,
            "manifest_path": os.path.join(settings.ARTIFACTS_DIR, "manifest.json")
        }
