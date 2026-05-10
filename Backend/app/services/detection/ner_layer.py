from app.services.detection.base import BaseDetection
from app.schemas.detection import PIIEntity, DetectionLayer, PIIType
import spacy

class NERDetection(BaseDetection):

    def __init__(self):
        self.nlp = spacy.load("en_core_web_trf")
        self.accepted_entities_mapping = {
            "PERSON":PIIType.NAME,
            "LOC":PIIType.ADDRESS,
            "GPE":PIIType.ADDRESS,
            "ORG":PIIType.ORG,
        }

    def detect(self, text: str) -> list[PIIEntity]:
        doc = self.nlp(text)

        return [
            PIIEntity(
                text=entitiy.text,
                pii_type=self.accepted_entities_mapping.get(entitiy.label_),
                start=entitiy.start_char,
                end=entitiy.end_char,
                confidence=0.85,
                layer=DetectionLayer.NER
            )
            for entitiy in doc.ents if entitiy.label_ in self.accepted_entities_mapping
        ]  