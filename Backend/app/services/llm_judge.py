import os
import json
from app.schemas.detection import DetectionResponse
from groq import Groq
from dotenv import load_dotenv
from app.core.prompts import Prompts

class LLMJudge():

    def __init__(self):
        load_dotenv()
        self.groq = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def judge(self, response: DetectionResponse) -> DetectionResponse:
        llm_response = self.groq.chat.completions.create(
            model="llama-3.3-70b-versatile",
            # Deterministic output for consistent results
            temperature=0,
            messages=[
                {
                    "role": "system", "content": Prompts.LLM_AS_JUDGE,
                },
                {
                    "role": "user", "content": f"Original text: {response.original_text}, Redacted text: {response.redacted_text}, Entities count: {response.entity_count}"
                }
            ],
            response_format={
                "type": "json_object"
            } 
        )
        
        try: 
            parsed = json.loads(llm_response.choices[0].message.content or "{}")
            return response.model_copy(update={
                "risk_score": parsed.get("risk_score"),
                "recommendation": parsed.get("recommendation")
            })
        except Exception:
            return response

def get_llm_judge():
    return LLMJudge()