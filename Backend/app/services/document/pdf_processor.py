import pymupdf
from app.schemas.detection import PIIEntity

class PdfProcessor():

    def __init__(self):
        pass

    def extract_text(self, file: bytes) -> str: 
        """
        Extracts text content from a PDF file.

        Takes a PDF file in bytes format and extracts its text content 
        by iterating through each page of the document. 

        Args:
            file (bytes): The PDF file in bytes format.

        Returns:
            str: The extracted text content from the PDF file.
        """
        doc = pymupdf.open(stream=file, filetype="pdf")
        return "".join(page.get_text() for page in doc)

    def detect(self, file: bytes, entities: list[PIIEntity]) -> bytes:
        """
        Apply visual PII redaction to a PDF file based on detected entities.

        Iterates each page and performs string matching against each entity.
        Matching text regions are covered with black-box annotations.
        Once all pages are processed, redactions are applied and the
        redacted PDF is returned as bytes for the API response.

        Args:
            file (bytes): The original PDF file content in bytes format.
            entities (list[PIIEntity]): List of detected PII entities to redact.

        Returns:
            bytes: The redacted PDF file as bytes for the API response.
        """
        doc = pymupdf.open(stream=file, filetype="pdf")

        for page in doc:
            for e in entities:
                hits = page.search_for(e.text, flags=pymupdf.TEXT_DEHYPHENATE)
                if hits:
                    for rect in hits:
                        page.add_redact_annot(rect, fill=(0, 0, 0))

            page.apply_redactions(graphics=True, text=True, images=pymupdf.PDF_REDACT_IMAGE_NONE)

        return doc.tobytes()
    
def get_pdf_processor():
    return PdfProcessor()