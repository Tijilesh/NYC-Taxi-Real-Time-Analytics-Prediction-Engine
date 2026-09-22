"""
Pydantic Schemas for Request and Response Serialization
"""

from typing import List, Dict, Optional, Any
from pydantic import BaseModel, Field
from datetime import datetime

class HealthResponse(BaseModel):
    status: str
    spark_available: bool
    version: str
    timestamp: str

class PipelineRunRequest(BaseModel):
    sample_size: Optional[int] = Field(default=5000, description="Records to process in this run")
    generate_synthetic_if_missing: bool = True

class PipelineRunResponse(BaseModel):
    run_id: str
    status: str
    duration_seconds: float
    total_records: int
    valid_records: int
    quarantine_records: int
    data_quality_pass_pct: float
    dq_breakdown: Dict[str, int]
    manifest_path: str

class KPISummary(BaseModel):
    total_trips: int
    total_revenue: float
    avg_fare: float
    avg_distance: float
    avg_duration_minutes: float
    avg_tip: float

class HourlyDemandPoint(BaseModel):
    hour: int
    trip_count: int
    avg_fare: float
    avg_distance: float

class SpatialZoneMetric(BaseModel):
    PULocationID: Optional[int] = None
    DOLocationID: Optional[int] = None
    trip_count: int
    avg_fare: float
    zone_revenue: Optional[float] = None

class AnalyticsOverviewResponse(BaseModel):
    kpis: KPISummary
    hourly_demand: List[HourlyDemandPoint]
    top_pickup_zones: List[SpatialZoneMetric]
    top_dropoff_zones: List[SpatialZoneMetric]

class DQRuleMetric(BaseModel):
    rule_id: str
    name: str
    description: str
    violations_count: int
    rejection_pct: float

class DQSummaryResponse(BaseModel):
    total_records: int
    valid_records: int
    quarantine_records: int
    valid_pct: float
    rules: List[DQRuleMetric]

class PredictionRequest(BaseModel):
    zone_id: int = Field(default=161, description="Pickup Location ID (1-265)")
    target_datetime: Optional[str] = Field(default=None, description="ISO format datetime (e.g. 2026-09-21T18:00:00)")

class PredictionResponse(BaseModel):
    zone_id: int
    target_hour: int
    day_of_week: int
    is_weekend: bool
    predicted_trips_next_hour: float
    confidence_interval: List[float]
    model_metadata: Dict[str, Any]

class StreamingStatusResponse(BaseModel):
    status: str
    records_received: int
    records_processed: int
    rejected_records: int
    processing_latency_sec: float
    current_window: str
    throughput_records_per_sec: float
