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
        Perform contextual PII detection using the Groq LLM (Layer 3).

        Sends the input text to the LLM with a structured prompt to identify
        PII types that regex and NER cannot reliably detect, such as usernames,
        place of birth, license plates, and protected characteristics.

        LLM-provided character indices are unreliable, so entity positions are
        recalculated by searching for the matched text in the original input.
        Any hallucinated entities not found in the original text are discarded.

        Falls back to an empty list on any parsing or API failure to ensure
        the pipeline continues without interruption.

        Args:
            text (str): The input text to analyse for contextual PII.

        Returns:
            list[PIIEntity]: Detected contextual PII entities with recalculated
                            positions and a fixed confidence score of 0.75.
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
            parsed = json.loads(llm_response.choices[0].message.content or '{"entities": []}')
            entities = []

            # LLM-provided indices are unreliable, recalculate from actual text position
            for entity in parsed["entities"]:
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