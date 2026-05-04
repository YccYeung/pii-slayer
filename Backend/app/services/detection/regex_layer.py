from app.services.detection.base import BaseDetection
from app.schemas.detection import PIIEntity, DetectionLayer, PIIType
import re

class RegexDetection(BaseDetection):

    def detect(self, text: str) -> list[PIIEntity]:
        return self.email_parse(text) + self.phone_parse(text) + self.ni_parse(text) + self.creditcard_parse(text) + self.postcode_parse(text)

    def email_parse(self, text: str) -> list[PIIEntity]:
        return [
            PIIEntity(
                text = email.group(),
                pii_type = PIIType.EMAIL,
                start = email.start(),
                end = email.end(),
                confidence = 100.0,
                layer = DetectionLayer.REGEX  
            )
            for email in re.finditer(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", text, re.IGNORECASE)
        ]
    
    def phone_parse(self, text: str) -> list[PIIEntity]:
        return [
            PIIEntity(
                text = phone.group(),
                pii_type = PIIType.PHONE,
                start = phone.start(),
                end = phone.end(),
                confidence = 100.0,
                layer = DetectionLayer.REGEX   
            )
            for phone in re.finditer(r"\b0[0-9]{10}\b|\b0[0-9]{4} [0-9]{3} [0-9]{3}\b|\+44\s?[0-9]{4}\s?[0-9]{6}|\(0\)[0-9]{10}", text)
        ]
    
    def ni_parse(self, text: str) -> list[PIIEntity]:
        return [
            PIIEntity(
                text = ni.group(),
                pii_type = PIIType.NI_NUMBER,
                start = ni.start(),
                end = ni.end(),
                confidence = 100.0,
                layer = DetectionLayer.REGEX   
            )
            for ni in re.finditer(r"\b(?![DFIQUV])[A-Z]{1}(?![DFIQUV])[A-Z]{1}[\s-]?[0-9]{2}[\s-]?[0-9]{2}[\s-]?[0-9]{2}[\s-]?[A-D]\b", text, re.IGNORECASE)
        ]

    def postcode_parse(self, text: str) -> list[PIIEntity]:
        return [
            PIIEntity(
                text = postcode.group(),
                pii_type = PIIType.POSTCODE,
                start = postcode.start(),
                end = postcode.end(),
                confidence = 100.0,
                layer = DetectionLayer.REGEX  
            )
            for postcode in re.finditer(r"\b[A-Z]{1,2}[0-9]{1,2}[A-Z]?\s?[0-9][A-Z]{2}\b", text, re.IGNORECASE)
        ]

    def creditcard_parse(self, text: str) -> list[PIIEntity]:
        return [
            PIIEntity(
                text = card_number.group(),
                pii_type = PIIType.CREDIT_CARD,
                start = card_number.start(),
                end = card_number.end(),
                confidence = 100.0,
                layer = DetectionLayer.REGEX  
            )
            for card_number in re.finditer(r"\b[0-9]{4}[\s-]?[0-9]{4}[\s-]?[0-9]{4}[\s-]?[0-9]{4}\b", text)
        ]