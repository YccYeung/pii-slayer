from app.schemas.detection import PIIEntity, DetectionRequest, DetectionResponse

class Redactor():

    def redaction(self, text: str, entities: list[PIIEntity]) -> str:
        sorted_entities = sorted(entities, key=lambda e: e.start, reverse=True)

        for e in sorted_entities:

            text = text[:e.start] + "[REDACTED]" + text[e.end:]

        return text

    def anonymization(self, text: str, entities: list[PIIEntity]) -> str:
        sorted_entities = sorted(entities, key=lambda e: e.start, reverse=True)

        entities_tracker = {
            "NAME": 0,
            "EMAIL": 0,
            "PHONE": 0,
            "ORG": 0,
            "ADDRESS": 0,
            "POSTCODE": 0,
            "CREDIT_CARD": 0,
            "NI_NUMBER": 0,
            "CONTEXTUAL": 0
        }

        for e in sorted_entities:

            entities_tracker[e.pii_type.value] += 1

        for e in sorted_entities:

            text = text[:e.start] + "[" + e.pii_type.value + "_" + str(entities_tracker.get(e.pii_type.value)) +"]" + text[e.end:]
            entities_tracker[e.pii_type.value] -= 1
            
        return text

    def get_redactor(self):
        return Redactor()