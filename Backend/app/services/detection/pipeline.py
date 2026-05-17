from app.services.detection.regex_layer import RegexDetection
from app.services.detection.ner_layer import NERDetection
from app.services.detection.llm_layer import LLMDetection
from app.schemas.detection import PIIEntity, RedactionMode, DetectionResponse
from app.services.redactor import Redactor
from app.services.llm_judge import LLMJudge
import re

class Pipeline():
     
    def __init__(self):
        self.regex = RegexDetection()
        self.ner = NERDetection()
        self.llm = LLMDetection()
        self.redactor = Redactor()   
        self.llm_judge = LLMJudge()  

    def run(self, text: str, mode: RedactionMode) -> DetectionResponse:
        """
        Orchestrate the full PII detection, redaction, and risk assessment pipeline.

        Processes input through three detection layers (regex, NER, LLM), deduplicates
        overlapping entity spans, applies redaction or anonymisation based on the
        requested mode, then passes the result to the LLM judge for residual risk
        assessment.

        Args:
            text (str): The raw input text to process.
            mode (RedactionMode): The redaction mode -- REDACT or ANONYMISE.

        Returns:
            DetectionResponse: Contains original text, redacted text, detected entities,
                            entity count, risk score, and sharability recommendation.
        """
        processed_input = self.input_processing(text)
        entities_list = self.deduplication(self.regex.detect(processed_input) 
                                           + self.ner.detect(processed_input) 
                                           + self.llm.detect(processed_input))

        process_methods = {
           RedactionMode.REDACT: self.redactor.redaction,
           RedactionMode.ANONYMISE: self.redactor.anonymization
        }

        return self.llm_judge.judge(DetectionResponse(
            original_text = text,
            redacted_text = process_methods[mode](processed_input, entities_list),
            entities = entities_list,
            entity_count = len(entities_list) 
        ))

    def input_processing(self, text: str) -> str:
        """
        Sanitise raw input text before pipeline processing.

        Normalises whitespace by replacing newlines and tabs with spaces,
        strips leading/trailing whitespace, and collapses multiple spaces into one.

        Args:
            text (str): The raw input text from the API request.

        Returns:
            str: The sanitised text ready for detection.
        """
        text = text.replace("\n", " ").replace("\t", " ").strip()
        return re.sub("[\s]+", " ", text)
    
    def deduplication(self, entities: list[PIIEntity]) -> list[PIIEntity]:
        """
        Remove overlapping entity spans using a greedy interval approach.

        Sorts entities by start index, then keeps the highest confidence entity
        when two spans overlap. Ensures each character position is covered by
        at most one entity before redaction is applied.

        Args:
            entities (list[PIIEntity]): List of detected entities from all layers.

        Returns:
            list[PIIEntity]: Deduplicated list with no overlapping spans.
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