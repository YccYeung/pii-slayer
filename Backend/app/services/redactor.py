from app.schemas.detection import PIIEntity, DetectionRequest, DetectionResponse

class Redactor():

    def __init__(self):
        pass

    def redaction(self, text: str, entities: list[PIIEntity]) -> str:
        sorted_entities = sorted(entities, key=lambda e: e.start, reverse=True)

        for e in sorted_entities:

            text = text[:e.start] + "[REDACTED]" + text[e.end:]

        return text

    def anonymization(self, text: str, entities: list[PIIEntity]) -> str:
        pass


    def get_redactor(self):
        return Redactor()