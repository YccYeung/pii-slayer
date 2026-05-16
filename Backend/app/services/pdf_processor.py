import pymupdf
from app.schemas.detection import PIIEntity

class PdfProcessor():

    def __init__(self):
        pass

    def extract_text(self, file: bytes) -> str: 
        doc = pymupdf.open(stream=file, filetype="pdf")
        return "".join(page.get_text() for page in doc)

    def detect(self, file: bytes, entities: list[PIIEntity]) -> bytes:
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