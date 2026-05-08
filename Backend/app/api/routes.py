from fastapi import APIRouter
from app.schemas.detection import PIIEntity, DetectionRequest, DetectionResponse
from app.services.detection.pipeline import Pipeline, get_pipeline

router = APIRouter()
version = "v1"

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post(f"/detect/text")
async def detect(request: DetectionRequest, pipeline: Pipeline = Depends(get_pipeline)) -> DetectionResponse:
    return pipeline.run(request.text, request.mode)