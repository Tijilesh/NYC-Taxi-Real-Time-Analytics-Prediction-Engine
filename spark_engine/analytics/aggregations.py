"""
Spatial, Temporal, and Financial Analytical Aggregations on Clean Taxi Data.
Computes:
- Hourly demand patterns (24 hours)
- Day-of-week demand patterns (0..6)
- Top pickup and dropoff locations
- Average fare, distance, and tip rates
"""

from pyspark.sql import DataFrame
from pyspark.sql import functions as F

def compute_kpi_summary(df: DataFrame) -> dict:
    """Computes headline KPIs from valid cleaned taxi trips."""
    summary_row = df.select(
        F.count("*").alias("total_trips"),
        F.coalesce(F.sum("total_amount"), F.lit(0.0)).alias("total_revenue"),
        F.coalesce(F.avg("fare_amount"), F.lit(0.0)).alias("avg_fare"),
        F.coalesce(F.avg("trip_distance"), F.lit(0.0)).alias("avg_distance"),
        F.coalesce(F.avg("duration_seconds") / 60.0, F.lit(0.0)).alias("avg_duration_minutes"),
        F.coalesce(F.avg("tip_amount"), F.lit(0.0)).alias("avg_tip")
    ).collect()[0]

    return {
        "total_trips": int(summary_row["total_trips"]),
        "total_revenue": round(float(summary_row["total_revenue"]), 2),
        "avg_fare": round(float(summary_row["avg_fare"]), 2),
        "avg_distance": round(float(summary_row["avg_distance"]), 2),
        "avg_duration_minutes": round(float(summary_row["avg_duration_minutes"]), 2),
        "avg_tip": round(float(summary_row["avg_tip"]), 2)
    }

def compute_hourly_demand(df: DataFrame) -> list:
    """Aggregates demand and average fare by hour of day (0-23)."""
    hourly_df = df.withColumn("hour", F.hour("tpep_pickup_datetime")) \
                  .groupBy("hour") \
                  .agg(
                      F.count("*").alias("trip_count"),
                      F.round(F.avg("fare_amount"), 2).alias("avg_fare"),
                      F.round(F.avg("trip_distance"), 2).alias("avg_distance")
                  ).orderBy("hour")

    return [row.asDict() for row in hourly_df.collect()]

def compute_spatial_pickup_zones(df: DataFrame, top_n: int = 10) -> list:
    """Aggregates top pickup zones with trip count and average fare."""
    top_zones = df.groupBy("PULocationID") \
                  .agg(
                      F.count("*").alias("trip_count"),
                      F.round(F.avg("fare_amount"), 2).alias("avg_fare"),
                      F.round(F.sum("total_amount"), 2).alias("zone_revenue")
                  ).orderBy(F.desc("trip_count")) \
                  .limit(top_n)

    return [row.asDict() for row in top_zones.collect()]

def compute_spatial_dropoff_zones(df: DataFrame, top_n: int = 10) -> list:
    """Aggregates top dropoff zones."""
    top_zones = df.groupBy("DOLocationID") \
                  .agg(
                      F.count("*").alias("trip_count"),
                      F.round(F.avg("fare_amount"), 2).alias("avg_fare")
                  ).orderBy(F.desc("trip_count")) \
                  .limit(top_n)

    return [row.asDict() for row in top_zones.collect()]
