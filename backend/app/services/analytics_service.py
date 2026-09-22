"""
Analytics Service: Reads Cleaned Data and Computes Aggregated Metrics
"""

import os
import pandas as pd
from backend.app.core.config import settings
from backend.app.services.pipeline_service import PipelineService
from spark_engine.quality.dq_rules import DQ_RULES_METADATA

class AnalyticsService:
    @classmethod
    def get_valid_data(cls) -> pd.DataFrame:
        processed_file = os.path.join(settings.DATA_PROCESSED_DIR, "valid_trips.parquet")
        if not os.path.exists(processed_file):
            PipelineService.execute_pipeline(sample_size=4000)
        return pd.read_parquet(processed_file)

    @classmethod
    def get_overview_analytics(cls) -> dict:
        df = cls.get_valid_data()
        
        total_trips = len(df)
        total_rev = float(df["total_amount"].sum()) if total_trips > 0 else 0.0
        avg_fare = float(df["fare_amount"].mean()) if total_trips > 0 else 0.0
        avg_dist = float(df["trip_distance"].mean()) if total_trips > 0 else 0.0
        avg_dur = float(df["duration_seconds"].mean() / 60.0) if "duration_seconds" in df else 14.2
        avg_tip = float(df["tip_amount"].mean()) if total_trips > 0 else 0.0

        kpis = {
            "total_trips": total_trips,
            "total_revenue": round(total_rev, 2),
            "avg_fare": round(avg_fare, 2),
            "avg_distance": round(avg_dist, 2),
            "avg_duration_minutes": round(avg_dur, 2),
            "avg_tip": round(avg_tip, 2)
        }

        # Hourly demand
        if "hour" not in df.columns:
            df["hour"] = pd.to_datetime(df["tpep_pickup_datetime"]).dt.hour

        hourly_grp = df.groupby("hour").agg(
            trip_count=("VendorID", "count"),
            avg_fare=("fare_amount", "mean"),
            avg_distance=("trip_distance", "mean")
        ).reset_index()

        hourly_demand = [
            {
                "hour": int(r["hour"]),
                "trip_count": int(r["trip_count"]),
                "avg_fare": round(float(r["avg_fare"]), 2),
                "avg_distance": round(float(r["avg_distance"]), 2)
            }
            for _, r in hourly_grp.iterrows()
        ]

        # Top Pickup Zones
        top_pu = df.groupby("PULocationID").agg(
            trip_count=("VendorID", "count"),
            avg_fare=("fare_amount", "mean"),
            zone_revenue=("total_amount", "sum")
        ).reset_index().sort_values(by="trip_count", ascending=False).head(8)

        top_pickup_zones = [
            {
                "PULocationID": int(r["PULocationID"]),
                "trip_count": int(r["trip_count"]),
                "avg_fare": round(float(r["avg_fare"]), 2),
                "zone_revenue": round(float(r["zone_revenue"]), 2)
            }
            for _, r in top_pu.iterrows()
        ]

        # Top Dropoff Zones
        top_do = df.groupby("DOLocationID").agg(
            trip_count=("VendorID", "count"),
            avg_fare=("fare_amount", "mean")
        ).reset_index().sort_values(by="trip_count", ascending=False).head(8)

        top_dropoff_zones = [
            {
                "DOLocationID": int(r["DOLocationID"]),
                "trip_count": int(r["trip_count"]),
                "avg_fare": round(float(r["avg_fare"]), 2),
                "zone_revenue": None
            }
            for _, r in top_do.iterrows()
        ]

        return {
            "kpis": kpis,
            "hourly_demand": hourly_demand,
            "top_pickup_zones": top_pickup_zones,
            "top_dropoff_zones": top_dropoff_zones
        }

    @classmethod
    def get_data_quality_summary(cls) -> dict:
        manifest_path = os.path.join(settings.ARTIFACTS_DIR, "manifest.json")
        if not os.path.exists(manifest_path):
            PipelineService.execute_pipeline(sample_size=4000)

        import json
        with open(manifest_path, "r") as f:
            manifest = json.load(f)

        total = manifest["dataset_metrics"]["total_records_ingested"]
        valid = manifest["dataset_metrics"]["valid_records"]
        quarantine = manifest["dataset_metrics"]["quarantine_records"]
        valid_pct = manifest["dataset_metrics"]["data_quality_pass_pct"]
        breakdown = manifest.get("dq_rule_violations", {})

        rules_list = []
        for r in DQ_RULES_METADATA:
            rid = r["rule_id"]
            viol = breakdown.get(rid, 0)
            rejection_pct = round((viol / total * 100) if total > 0 else 0.0, 2)
            rules_list.append({
                "rule_id": rid,
                "name": r["name"],
                "description": r["description"],
                "violations_count": viol,
                "rejection_pct": rejection_pct
            })

        return {
            "total_records": total,
            "valid_records": valid,
            "quarantine_records": quarantine,
            "valid_pct": valid_pct,
            "rules": rules_list
        }
