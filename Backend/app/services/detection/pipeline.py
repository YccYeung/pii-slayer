from app.services.detection.regex_layer import RegexDetection
from app.schemas.detection import PIIEntity

class pipeline():
    
    def __init__(self):
        self.regex = RegexDetection()     

    def run(self, text: str) -> list[PIIEntity]:
        return self.regex.detect(text)