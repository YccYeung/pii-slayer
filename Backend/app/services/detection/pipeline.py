from app.services.detection.regex_layer import RegexDetection
from app.services.detection.ner_layer import NERDetection
from app.schemas.detection import PIIEntity, RedactionMode, DetectionResponse
from app.services.redactor import Redactor
import re

class Pipeline():
     
    def __init__(self):
        self.regex = RegexDetection()
        self.ner = NERDetection()
        self.redactor = Redactor()     

    def run(self, text: str, mode: RedactionMode) -> DetectionResponse:
        processed_input = self.input_processing(text)
        entities_list = self.regex.detect(processed_input) + self.ner.detect(processed_input)
        if mode == RedactionMode.REDACT:
            return DetectionResponse(
                original_text = text,
                redacted_text = self.redactor.redaction(processed_input, entities_list),
                entities = entities_list,
                entity_count = len(entities_list)
        )
        elif mode == RedactionMode.ANONYMISE:
            pass

    def input_processing(self, text: str) -> str:
        text = text.replace("\n", " ").replace("\t", " ").strip()
        return re.sub("[\s]+", " ", text)
    
def get_pipeline():
    return Pipeline()