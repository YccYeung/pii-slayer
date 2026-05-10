from enum import Enum
from pydantic import BaseModel

class PIIType(str, Enum):
    NAME = "NAME"
    ADDRESS = "ADDRESS"
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    POSTCODE = "POSTCODE"
    CREDIT_CARD = "CREDIT_CARD"
    NI_NUMBER = "NI_NUMBER"
    ORG = "ORG"
    CONTEXTUAL = "CONTEXTUAL"

class DetectionLayer(str, Enum):
    REGEX = "REGEX"
    NER = "NER"
    LLM = "LLM"

class RedactionMode(str, Enum):
    REDACT = "REDACT"
    ANONYMISE = "ANONYMISE"

class PIIEntity(BaseModel):
    text: str
    pii_type: PIIType
    start: int
    end: int
    confidence: float
    layer: DetectionLayer

class DetectionRequest(BaseModel):
    text: str
    mode: RedactionMode

class DetectionResponse(BaseModel):
    original_text: str
    redacted_text: str
    entities: list[PIIEntity]
    entity_count: int