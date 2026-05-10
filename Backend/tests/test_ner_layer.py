from app.services.detection.ner_layer import NERDetection
from app.schemas.detection import PIIEntity, PIIType, DetectionLayer
import pytest

@pytest.mark.parametrize("simple_input", [
    "John Smith works at Google in London.",
    "Dr. Sarah Connor is the CEO of Anthropic.",
    "Barack Obama visited Microsoft headquarters.",
    "Alice Johnson and Bob Smith met with the team at Amazon.",
    "Yuki Tanaka is a software engineer at Sony in Tokyo.",
    "Marie Curie conducted research at the University of Paris in France."
])

def test_simple_ner_detection(simple_input):
    nerdetection = NERDetection()

    entities_list = nerdetection.detect(simple_input)

    assert len(entities_list) > 0
    assert any(e.pii_type == PIIType.NAME for e in entities_list)
    assert any(e.pii_type == PIIType.ORG for e in entities_list)

@pytest.mark.parametrize("complex_input", [
    "Dr. Priya Sharma from the University of Cambridge met with representatives from Microsoft, Google, and the NHS at the Houses of Parliament in Westminster to discuss AI policy in the United Kingdom.",
    "Hiroshi Tanaka, CEO of Sony Corporation in Tokyo, flew to San Francisco to meet with Tim Cook from Apple and Sundar Pichai from Alphabet at the Stanford Research Institute in California.",
    "Maria González, a senior partner at McKinsey & Company in Madrid, collaborated with teams from Siemens, Volkswagen, and the European Central Bank in Frankfurt to produce a report for the German government.",
    "Professor James O'Brien from Trinity College Dublin worked alongside researchers from MIT, Oxford University, and the World Health Organization in Geneva to develop new guidelines for the United Nations.",
    "In 2019, Jeff Bezos donated $150 million to the Bill & Melinda Gates Foundation in Seattle, while Amazon reported quarterly earnings of $2.3 billion, prompting analysts at Morgan Stanley in New York to revise their forecast for the North American e-commerce market."
])

def test_complex_ner_detection(complex_input):
    nerdetection = NERDetection()

    entities_list = nerdetection.detect(complex_input)

    assert len(entities_list) >= 5
    assert any(e.pii_type == PIIType.NAME for e in entities_list)
    assert any(e.pii_type == PIIType.ORG for e in entities_list)
    assert any(e.pii_type == PIIType.ADDRESS for e in entities_list)