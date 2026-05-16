from app.services.detection.base import BaseDetection
from app.schemas.detection import PIIEntity, DetectionLayer, PIIType
from app.core.prompts import Prompts
import os
import json
from groq import Groq
from dotenv import load_dotenv

class LLMDetection(BaseDetection):

    def __init__(self):
        load_dotenv()
        self.groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def detect(self, text: str) -> list[PIIEntity]:
        """
        Layer 3 detection: contextual PII that regex and NER cannot catch.
        Sends text to Groq LLM and parses structured JSON response.
        Falls back to empty list on any failure to avoid breaking the pipeline.
        """
        llm_response = self.groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            # Deterministic output for consistent results
            temperature=0,
            messages=[
                {
                    "role": "system", "content": Prompts.LLM_PII_DETECTION,
                },
                {
                    "role": "user", "content": text
                }
            ],
            response_format={
                "type": "json_object"
            } 
        )
        try: 
            llm_response = json.loads(llm_response.choices[0].message.content or '{"entities": []}')
            entities = []

            # LLM-provided indices are unreliable, recalculate from actual text position
            for entity in llm_response["entities"]:
                start = text.find(entity["text"])
                if start == -1:
                    # Skip hallucinated entities not found in original text
                    continue
                end = start + len(entity["text"])
                entities.append(PIIEntity(
                    text=entity["text"],
                    pii_type=PIIType.CONTEXTUAL,
                    start=start,
                    end=end,
                    confidence=0.75,
                    layer=DetectionLayer.LLM
                ))
            return entities
        except Exception:
            return []