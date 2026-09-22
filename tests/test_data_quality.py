import tempfile
import json
import os
import pytest
from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, IntegerType, DoubleType, TimestampType
from spark_engine.quality.dq_rules import apply_data_quality_rules

def _create_df_from_json(spark: SparkSession, rows: list):
    schema = StructType([
        StructField("VendorID", IntegerType(), True),
        StructField("tpep_pickup_datetime", TimestampType(), True),
        StructField("tpep_dropoff_datetime", TimestampType(), True),
        StructField("passenger_count", IntegerType(), True),
        StructField("trip_distance", DoubleType(), True),
        StructField("PULocationID", IntegerType(), True),
        StructField("DOLocationID", IntegerType(), True),
        StructField("payment_type", IntegerType(), True),
        StructField("fare_amount", DoubleType(), True),
        StructField("extra", DoubleType(), True),
        StructField("mta_tax", DoubleType(), True),
        StructField("tip_amount", DoubleType(), True),
        StructField("tolls_amount", DoubleType(), True),
        StructField("improvement_surcharge", DoubleType(), True),
        StructField("total_amount", DoubleType(), True),
        StructField("congestion_surcharge", DoubleType(), True),
        StructField("Airport_fee", DoubleType(), True),
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

def test_data_quality_all_pass(spark):
    clean_data = [{
        "VendorID": 1,
        "tpep_pickup_datetime": "2026-09-20 10:00:00",
        "tpep_dropoff_datetime": "2026-09-20 10:18:00",
        "passenger_count": 2,
        "trip_distance": 3.5,
        "PULocationID": 161,
        "DOLocationID": 230,
        "payment_type": 1,
        "fare_amount": 15.50,
        "extra": 0.5,
        "mta_tax": 0.5,
        "tip_amount": 3.00,
        "tolls_amount": 0.0,
        "improvement_surcharge": 0.3,
        "total_amount": 19.80,
        "congestion_surcharge": 2.5,
        "Airport_fee": 0.0
    }]
    df = _create_df_from_json(spark, clean_data)
    valid_df, quarantine_df = apply_data_quality_rules(df)

    assert valid_df.count() == 1
    assert quarantine_df.count() == 0

def test_data_quality_quarantine_violations(spark):
    dirty_data = [
        # Negative duration
        {
            "VendorID": 1,
            "tpep_pickup_datetime": "2026-09-20 10:00:00",
            "tpep_dropoff_datetime": "2026-09-20 09:50:00",
            "passenger_count": 1,
            "trip_distance": 2.0,
            "PULocationID": 161,
            "DOLocationID": 162,
            "payment_type": 1,
            "fare_amount": 10.0,
            "extra": 0.0,
            "mta_tax": 0.5,
            "tip_amount": 0.0,
            "tolls_amount": 0.0,
            "improvement_surcharge": 0.3,
            "total_amount": 10.8,
            "congestion_surcharge": 0.0,
            "Airport_fee": 0.0
        },
        # Negative fare
        {
            "VendorID": 1,
            "tpep_pickup_datetime": "2026-09-20 10:00:00",
            "tpep_dropoff_datetime": "2026-09-20 10:15:00",
            "passenger_count": 1,
            "trip_distance": 2.0,
            "PULocationID": 161,
            "DOLocationID": 162,
            "payment_type": 1,
            "fare_amount": -15.0,
            "extra": 0.0,
            "mta_tax": 0.5,
            "tip_amount": 0.0,
            "tolls_amount": 0.0,
            "improvement_surcharge": 0.3,
            "total_amount": -14.2,
            "congestion_surcharge": 0.0,
            "Airport_fee": 0.0
        },
        # Invalid Location ID
        {
            "VendorID": 1,
            "tpep_pickup_datetime": "2026-09-20 10:00:00",
            "tpep_dropoff_datetime": "2026-09-20 10:15:00",
            "passenger_count": 1,
            "trip_distance": 2.0,
            "PULocationID": 999,
            "DOLocationID": 162,
            "payment_type": 1,
            "fare_amount": 12.0,
            "extra": 0.0,
            "mta_tax": 0.5,
            "tip_amount": 0.0,
            "tolls_amount": 0.0,
            "improvement_surcharge": 0.3,
            "total_amount": 12.8,
            "congestion_surcharge": 0.0,
            "Airport_fee": 0.0
        }
    ]
    df = _create_df_from_json(spark, dirty_data)
    valid_df, quarantine_df = apply_data_quality_rules(df)

    assert valid_df.count() == 0
    assert quarantine_df.count() == 3

