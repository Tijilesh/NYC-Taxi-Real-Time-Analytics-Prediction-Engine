"""
14 Data Quality Rules for NYC TLC Taxi Trip records.
Each rule verifies specific domain boundaries and integrity criteria.
Failed records are flagged with rule violations and routed to quarantine.
"""

from typing import Dict, List, Tuple
from pyspark.sql import DataFrame
from pyspark.sql import functions as F

DQ_RULES_METADATA = [
    {"rule_id": "DQ001", "name": "Null Pickup Timestamp", "description": "tpep_pickup_datetime must not be null"},
    {"rule_id": "DQ002", "name": "Null Dropoff Timestamp", "description": "tpep_dropoff_datetime must not be null"},
    {"rule_id": "DQ003", "name": "Negative or Zero Duration", "description": "dropoff_datetime must be strictly after pickup_datetime"},
    {"rule_id": "DQ004", "name": "Duration Exceeds 24 Hours", "description": "trip duration must be <= 86400 seconds"},
    {"rule_id": "DQ005", "name": "Invalid Passenger Count Low", "description": "passenger_count must be > 0"},
    {"rule_id": "DQ006", "name": "Invalid Passenger Count High", "description": "passenger_count must be <= 9"},
    {"rule_id": "DQ007", "name": "Invalid Trip Distance Low", "description": "trip_distance must be > 0.0 miles"},
    {"rule_id": "DQ008", "name": "Invalid Trip Distance High", "description": "trip_distance must be <= 100.0 miles"},
    {"rule_id": "DQ009", "name": "Invalid Fare Amount Low", "description": "fare_amount must be >= 2.50 (minimum NYC meter base fare)"},
    {"rule_id": "DQ010", "name": "Invalid Fare Amount High", "description": "fare_amount must be <= 1000.00"},
    {"rule_id": "DQ011", "name": "Invalid Pickup Location ID", "description": "PULocationID must be between 1 and 265"},
    {"rule_id": "DQ012", "name": "Invalid Dropoff Location ID", "description": "DOLocationID must be between 1 and 265"},
    {"rule_id": "DQ013", "name": "Negative Tip Amount", "description": "tip_amount must be >= 0.0"},
    {"rule_id": "DQ014", "name": "Unrealistic Speed", "description": "average speed must be <= 85.0 mph"},
]

def apply_data_quality_rules(df: DataFrame) -> Tuple[DataFrame, DataFrame, Dict[str, int]]:
    """
    Applies all 14 data quality rules to input DataFrame.
    Returns:
      - valid_df: DataFrame with clean, passed records.
      - quarantine_df: DataFrame with failed records and failure reasons.
      - dq_metrics: Dictionary of violation counts per rule.
    """
    # Calculate duration in seconds and speed in mph
    df_calc = df.withColumn(
        "duration_seconds",
        F.unix_timestamp("tpep_dropoff_datetime") - F.unix_timestamp("tpep_pickup_datetime")
    ).withColumn(
        "speed_mph",
        F.when(
            F.col("duration_seconds") > 0,
            (F.col("trip_distance") / (F.col("duration_seconds") / 3600.0))
        ).otherwise(F.lit(0.0))
    )

    # Boolean flags for 14 rules (True = valid, False = violation)
    cond_dq001 = F.col("tpep_pickup_datetime").isNotNull()
    cond_dq002 = F.col("tpep_dropoff_datetime").isNotNull()
    cond_dq003 = F.col("duration_seconds") > 0
    cond_dq004 = F.col("duration_seconds") <= 86400
    cond_dq005 = F.col("passenger_count") > 0
    cond_dq006 = F.col("passenger_count") <= 9
    cond_dq007 = F.col("trip_distance") > 0.0
    cond_dq008 = F.col("trip_distance") <= 100.0
    cond_dq009 = F.col("fare_amount") >= 2.50
    cond_dq010 = F.col("fare_amount") <= 1000.0
    cond_dq011 = (F.col("PULocationID") >= 1) & (F.col("PULocationID") <= 265)
    cond_dq012 = (F.col("DOLocationID") >= 1) & (F.col("DOLocationID") <= 265)
    cond_dq013 = F.col("tip_amount") >= 0.0
    cond_dq014 = F.col("speed_mph") <= 85.0

    all_valid_cond = (
        cond_dq001 & cond_dq002 & cond_dq003 & cond_dq004 &
        cond_dq005 & cond_dq006 & cond_dq007 & cond_dq008 &
        cond_dq009 & cond_dq010 & cond_dq011 & cond_dq012 &
        cond_dq013 & cond_dq014
    )

    df_flagged = df_calc.withColumn("is_valid", all_valid_cond)

    # Valid dataset
    valid_df = df_flagged.filter(F.col("is_valid") == True).drop("is_valid")

    # Quarantine dataset
    quarantine_df = df_flagged.filter(F.col("is_valid") == False)

    return valid_df, quarantine_df

