from fastapi import APIRouter
from datetime import datetime
from backend.app.schemas.schemas import HealthResponse
from backend.app.services.spark_service import SparkManager
from backend.app.core.config import settings

router = APIRouter()

@router.get("/health", response_model=HealthResponse)
def get_health():
    return {
        "status": "HEALTHY",
        "spark_available": SparkManager.is_available(),
        "version": settings.VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }
