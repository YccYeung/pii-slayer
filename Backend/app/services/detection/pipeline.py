from app.services.detection.regex_layer import RegexDetection
from app.services.detection.ner_layer import NERDetection
from app.services.detection.llm_layer import LLMDetection
from app.schemas.detection import PIIEntity, RedactionMode, DetectionResponse
from app.services.redactor import Redactor
import re

class Pipeline():
     
    def __init__(self):
        self.regex = RegexDetection()
        self.ner = NERDetection()
        self.llm = LLMDetection()
        self.redactor = Redactor()     

    def run(self, text: str, mode: RedactionMode) -> DetectionResponse:
        processed_input = self.input_processing(text)
        entities_list = self.regex.detect(processed_input) + self.ner.detect(processed_input) + self.llm.detect(processed_input)
        entities_list = self.deduplication(entities_list)
        if mode == RedactionMode.REDACT:
            return DetectionResponse(
                original_text = text,
                redacted_text = self.redactor.redaction(processed_input, entities_list),
                entities = entities_list,
                entity_count = len(entities_list)
            )
        elif mode == RedactionMode.ANONYMISE:
            return DetectionResponse(
                original_text = text,
                redacted_text = self.redactor.anonymization(processed_input, entities_list),
                entities = entities_list,
                entity_count = len(entities_list)
            )

    def input_processing(self, text: str) -> str:
        text = text.replace("\n", " ").replace("\t", " ").strip()
        return re.sub("[\s]+", " ", text)
    
    def deduplication(self, entities: list[PIIEntity]) -> list[PIIEntity]:
        """
        Remove overlapping entity spans using a greedy interval approach.
        Sorts by start index, then keeps the highest confidence entity when spans overlap.
        """
        entities.sort(key=lambda x : x.start)
        result_list = []

        for e in entities:
            if not result_list or e.start >= result_list[-1].end:
                result_list.append(e)
            else:
                if e.confidence > result_list[-1].confidence:
                    result_list[-1] = e

        return result_list

def get_pipeline():
    return Pipeline()