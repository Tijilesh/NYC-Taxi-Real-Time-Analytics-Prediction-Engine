"""
FastAPI Main Application Entry Point
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.api.routes_health import router as health_router
from backend.app.api.routes_pipeline import router as pipeline_router
from backend.app.api.routes_analytics import router as analytics_router
from backend.app.api.routes_prediction import router as prediction_router
from backend.app.api.routes_streaming import router as streaming_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Real-Time NYC Taxi Trip Analytics, Data Quality Quarantine, and Demand Prediction Platform using Apache Spark & FastAPI."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health_router, prefix=settings.API_V1_PREFIX, tags=["Health"])
app.include_router(pipeline_router, prefix=settings.API_V1_PREFIX, tags=["Pipeline"])
app.include_router(analytics_router, prefix=settings.API_V1_PREFIX, tags=["Analytics & Data Quality"])
app.include_router(prediction_router, prefix=settings.API_V1_PREFIX, tags=["Machine Learning"])
app.include_router(streaming_router, prefix=settings.API_V1_PREFIX, tags=["Streaming"])

@app.get("/")
def root():
    return {
        "system": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "docs": "/docs"
    }
