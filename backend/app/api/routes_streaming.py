from fastapi import APIRouter
from backend.app.schemas.schemas import StreamingStatusResponse
from backend.app.services.streaming_service import StreamingMonitorService

router = APIRouter()

@router.get("/streaming/status", response_model=StreamingStatusResponse)
def get_streaming_status():
    return StreamingMonitorService.get_streaming_status()
