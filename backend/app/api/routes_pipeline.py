from fastapi import APIRouter, UploadFile, File
from backend.app.schemas.schemas import PipelineRunRequest, PipelineRunResponse
from backend.app.services.pipeline_service import PipelineService
import os
import shutil
import json
from backend.app.core.config import settings

router = APIRouter()

@router.post("/pipeline/upload")
async def upload_dataset(file: UploadFile = File(...)):
    os.makedirs(settings.DATA_SAMPLE_DIR, exist_ok=True)
    target_path = os.path.join(settings.DATA_SAMPLE_DIR, "yellow_tripdata_sample.parquet")
    
    with open(target_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
        
    file_size_mb = round(os.path.getsize(target_path) / (1024 * 1024), 2)
    return {
        "status": "UPLOAD_SUCCESS",
        "filename": file.filename,
        "saved_path": target_path,
        "size_mb": file_size_mb,
        "message": f"Dataset '{file.filename}' uploaded successfully ({file_size_mb} MB). Ready for Spark execution."
    }

@router.post("/pipeline/run", response_model=PipelineRunResponse)

def trigger_pipeline_run(payload: PipelineRunRequest = PipelineRunRequest()):
    result = PipelineService.execute_pipeline(sample_size=payload.sample_size or 5000)
    return result

@router.get("/pipeline/manifest")
def get_latest_manifest():
    manifest_path = os.path.join(settings.ARTIFACTS_DIR, "manifest.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r") as f:
            return json.load(f)
    return {"message": "No run manifest found yet. Trigger a pipeline run."}

@router.get("/pipeline/lineage")
def get_lineage():
    lineage_path = os.path.join(settings.ARTIFACTS_DIR, "lineage.json")
    if os.path.exists(lineage_path):
        with open(lineage_path, "r") as f:
            return json.load(f)
    from spark_engine.lineage.audit_tracker import generate_transformation_lineage
    return generate_transformation_lineage()
