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

class RiskScore(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class DetectionRequest(BaseModel):
    text: str
    mode: RedactionMode

class DetectionResponse(BaseModel):
    original_text: str
    redacted_text: str
    entities: list[PIIEntity]
    entity_count: int
    risk_score: RiskScore | None = None
    recommendation: str | None = None

class FileDetectionResponse(BaseModel):
    redacted_file: str  # base64 encoded
    filename: str
    entity_count: int
    entities: list[PIIEntity]
    risk_score: RiskScore | None = None
    recommendation: str | None = None