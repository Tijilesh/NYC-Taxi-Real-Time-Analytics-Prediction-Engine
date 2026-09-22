import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_api_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "HEALTHY"
    assert "spark_available" in data

def test_api_prediction():
    res = client.post("/api/prediction/demand", json={"zone_id": 161})
    assert res.status_code == 200
    data = res.json()
    assert data["zone_id"] == 161
    assert "predicted_trips_next_hour" in data
    assert len(data["confidence_interval"]) == 2

def test_api_streaming_status():
    res = client.get("/api/streaming/status")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "RUNNING"
    assert data["records_processed"] > 0
