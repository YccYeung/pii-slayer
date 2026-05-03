from abc import ABC, abstractmethod
from app.schemas.detection import PIIEntity

class BaseDetection(ABC):
    @abstractmethod
    def detect(self, text: str) -> list[PIIEntity]:
        pass