import base64
from fastapi import APIRouter, Depends, UploadFile, Response
from app.schemas.detection import PIIEntity, DetectionRequest, DetectionResponse, RedactionMode, FileDetectionResponse
from app.services.detection.pipeline import Pipeline, get_pipeline
from app.services.document.pdf_processor import PdfProcessor, get_pdf_processor
from app.services.document.csv_processor import CSVProcessor, get_csv_processor

router = APIRouter()
version = "v1"

@router.get("/")
async def root():
    return {"message": "Hello World"}

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/detect/text")
async def detect(request: DetectionRequest, pipeline: Pipeline = Depends(get_pipeline)) -> DetectionResponse:
    return pipeline.run(request.text, request.mode)

@router.post("/detect/pdf")
async def pdf_detect(file: UploadFile, pdf_processor: PdfProcessor = Depends(get_pdf_processor), pipeline: Pipeline = Depends(get_pipeline)) -> FileDetectionResponse:
    doc_bytes = await file.read()
    doc_content = pdf_processor.extract_text(doc_bytes)
    result = pipeline.run(doc_content, RedactionMode.REDACT)
    redacted_bytes = pdf_processor.detect(doc_bytes, result.entities)
    return FileDetectionResponse(
        redacted_file = base64.b64encode(redacted_bytes).decode("utf-8"),
        filename = f"redacted_{file.filename}",
        risk_score = result.risk_score,
        recommendation = result.recommendation,
        entity_count = result.entity_count,
        entities = result.entities
    )

@router.post("/detect/csv")
async def csv_detect(file: UploadFile, csv_processor: CSVProcessor = Depends(get_csv_processor), pipeline: Pipeline = Depends(get_pipeline)) -> FileDetectionResponse:
    doc_bytes = await file.read()
    doc_content = csv_processor.extract_text(doc_bytes)
    result = pipeline.run(doc_content, RedactionMode.REDACT)
    redacted_bytes = csv_processor.detect(doc_bytes, result.entities)
    return FileDetectionResponse(
        redacted_file = base64.b64encode(redacted_bytes).decode("utf-8"),
        filename = f"redacted_{file.filename}",
        risk_score = result.risk_score,
        recommendation = result.recommendation,
        entity_count = result.entity_count,
        entities = result.entities
    )