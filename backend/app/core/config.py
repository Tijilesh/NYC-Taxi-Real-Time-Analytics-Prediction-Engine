"""
FastAPI Backend Application Configuration
"""

import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "NYC Taxi Real-Time Analytics & Prediction Engine"
    API_V1_PREFIX: str = "/api"
    VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # Storage paths
    BASE_DIR: str = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    DATA_SAMPLE_DIR: str = os.path.join(BASE_DIR, "data", "sample")
    DATA_PROCESSED_DIR: str = os.path.join(BASE_DIR, "data", "processed")
    DATA_QUARANTINE_DIR: str = os.path.join(BASE_DIR, "data", "quarantine")
    ARTIFACTS_DIR: str = os.path.join(BASE_DIR, "artifacts")
    
    # Metadata persistence
    DATABASE_URL: str = f"sqlite:///{os.path.join(BASE_DIR, 'taxi_metadata.db')}"

    class Config:
        env_file = ".env"

settings = Settings()
