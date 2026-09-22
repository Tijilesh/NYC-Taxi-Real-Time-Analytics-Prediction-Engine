import tempfile
import json
import os
import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType, TimestampType
from spark_engine.analytics.aggregations import compute_kpi_summary, compute_hourly_demand, compute_spatial_pickup_zones

def _create_analytics_df(spark: SparkSession, rows: list):
    schema = StructType([
        StructField("VendorID", IntegerType(), True),
        StructField("tpep_pickup_datetime", TimestampType(), True),
        StructField("tpep_dropoff_datetime", TimestampType(), True),
        StructField("passenger_count", IntegerType(), True),
        StructField("trip_distance", DoubleType(), True),
        StructField("duration_seconds", DoubleType(), True),
        StructField("PULocationID", IntegerType(), True),
        StructField("DOLocationID", IntegerType(), True),
        StructField("fare_amount", DoubleType(), True),
        StructField("tip_amount", DoubleType(), True),
        StructField("total_amount", DoubleType(), True),
    ])
    
    with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
        for row in rows:
            f.write(json.dumps(row) + "\n")
        temp_path = f.name
        
    try:
        df = spark.read.schema(schema).option("timestampFormat", "yyyy-MM-dd HH:mm:ss").json(temp_path)
        df.cache().count()
        return df
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

def test_analytics_aggregations(spark):
    rows = [
        {
            "VendorID": 1,
            "tpep_pickup_datetime": "2026-09-20 14:00:00",
            "tpep_dropoff_datetime": "2026-09-20 14:20:00",
            "passenger_count": 1,
            "trip_distance": 4.0,
            "duration_seconds": 1200.0,
            "PULocationID": 161,
            "DOLocationID": 230,
            "fare_amount": 20.0,
            "tip_amount": 4.0,
            "total_amount": 26.5
        },
        {
            "VendorID": 2,
            "tpep_pickup_datetime": "2026-09-20 14:00:00",
            "tpep_dropoff_datetime": "2026-09-20 14:20:00",
            "passenger_count": 2,
            "trip_distance": 6.0,
            "duration_seconds": 1200.0,
            "PULocationID": 161,
            "DOLocationID": 237,
            "fare_amount": 30.0,
            "tip_amount": 6.0,
            "total_amount": 38.5
        }
    ]

    df = _create_analytics_df(spark, rows)

    kpis = compute_kpi_summary(df)
    assert kpis["total_trips"] == 2
    assert kpis["avg_fare"] == 25.0
    assert kpis["total_revenue"] == 65.0
    assert kpis["avg_distance"] == 5.0

    hourly = compute_hourly_demand(df)
    assert len(hourly) == 1
    assert hourly[0]["hour"] == 14
    assert hourly[0]["trip_count"] == 2

    zones = compute_spatial_pickup_zones(df)
    assert len(zones) == 1
    assert zones[0]["PULocationID"] == 161
    assert zones[0]["trip_count"] == 2

