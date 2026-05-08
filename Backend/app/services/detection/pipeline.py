from app.services.detection.regex_layer import RegexDetection
from app.schemas.detection import PIIEntity, RedactionMode, DetectionResponse
from app.services.redactor import Redactor

class Pipeline():
     
    def __init__(self):
        self.regex = RegexDetection()
        self.redactor = Redactor()     

    def run(self, text: str, mode: RedactionMode) -> DetectionResponse:
        entities_list = self.regex.detect(text)
        if mode == RedactionMode.REDACT:
            return DetectionResponse(
                original_text = text,
                redacted_text = self.redactor.redaction(text, entities_list),
                entities = entities_list,
                entity_count = len(entities_list)
        )
        elif mode == RedactionMode.ANONYMISE:
            pass
    
def get_pipeline():
    return Pipeline()