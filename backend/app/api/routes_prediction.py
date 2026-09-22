from fastapi import APIRouter
from datetime import datetime
from backend.app.schemas.schemas import PredictionRequest, PredictionResponse
from spark_engine.ml.demand_model import demand_predictor

router = APIRouter()

@router.post("/prediction/demand", response_model=PredictionResponse)
def predict_taxi_demand(payload: PredictionRequest):
    if payload.target_datetime:
        try:
            target_dt = datetime.fromisoformat(payload.target_datetime)
        except Exception:
            target_dt = datetime.utcnow()
    else:
        target_dt = datetime.utcnow()

    res = demand_predictor.predict_demand(
        zone_id=payload.zone_id,
        target_datetime=target_dt
    )
    return res
