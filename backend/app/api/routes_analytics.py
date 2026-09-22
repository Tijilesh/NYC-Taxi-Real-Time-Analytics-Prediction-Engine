from fastapi import APIRouter
from backend.app.schemas.schemas import AnalyticsOverviewResponse, DQSummaryResponse
from backend.app.services.analytics_service import AnalyticsService

router = APIRouter()

@router.get("/analytics/overview", response_model=AnalyticsOverviewResponse)
def get_analytics_overview():
    return AnalyticsService.get_overview_analytics()

@router.get("/data-quality/summary", response_model=DQSummaryResponse)
def get_data_quality_summary():
    return AnalyticsService.get_data_quality_summary()
