from app.services.detection.llm_layer import LLMDetection
from app.schemas.detection import PIIType, DetectionLayer
import pytest

@pytest.mark.parametrize("contextual_input", [
    "The only female surgeon in the Manchester Royal Infirmary night shift told me she had concerns about the new policy.",
    "My colleague who sits next to the window in the Edinburgh office handles all the invoices.",
    "The only Black partner at the firm resigned last month after the incident.",
])
def test_llm_contextual_detection(contextual_input):
    llm = LLMDetection()
    entities = llm.detect(contextual_input)
    assert len(entities) > 0
    assert any(e.pii_type == PIIType.CONTEXTUAL for e in entities)
    assert any(e.layer == DetectionLayer.LLM for e in entities)

def test_llm_empty_on_no_pii():
    llm = LLMDetection()
    entities = llm.detect("The weather in London is nice today.")
    assert entities == []