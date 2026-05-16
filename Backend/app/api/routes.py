from fastapi import APIRouter, Depends, UploadFile, Response
from app.schemas.detection import PIIEntity, DetectionRequest, DetectionResponse, RedactionMode
from app.services.detection.pipeline import Pipeline, get_pipeline
from app.services.pdf_processor import PdfProcessor, get_pdf_processor

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

@router.post(f"/detect/pdf")
async def pdf_detect(file: UploadFile, pdf_processor: PdfProcessor = Depends(get_pdf_processor), pipeline: Pipeline = Depends(get_pipeline)) -> Response:
    doc_bytes = await file.read()
    doc_content = pdf_processor.extract_text(doc_bytes) 
    return Response(
        media_type="application/pdf",
        headers={
            "Content-Disposition": f"attachment; filename=redacted_{file.filename}"
        },
        content=pdf_processor.detect(doc_bytes, pipeline.run(doc_content, RedactionMode.REDACT).entities)
    )