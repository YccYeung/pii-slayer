from app.services.detection.regex_layer import RegexDetection
from app.schemas.detection import PIIEntity, PIIType, DetectionLayer
import pytest

@pytest.mark.parametrize("expected_successful_email", [
    "john@example.com",
    "jane.doe@company.co.uk",
    "user+tag@gmail.com",
    "test123@nhs.net",
    "firstname.lastname@subdomain.org"
])

@pytest.mark.parametrize("expected_failed_email", [
    "notanemail",
    "@missinguser.com",
    "missingdomain@", 
    "nodomain@.com",
    "plaintextc"
])

def test_email_parsing(expected_successful_email, expected_failed_email):
    regexDetection = RegexDetection()

    assert regexDetection.email_parse(expected_successful_email) == [
        PIIEntity(
            text = expected_successful_email,
            pii_type = PIIType.EMAIL,
            start = 0,
            end = len(expected_successful_email),
            confidence = 1.0,
            layer = DetectionLayer.REGEX  
        )
    ]
    assert regexDetection.email_parse(expected_failed_email) == []

@pytest.mark.parametrize("expected_successful_phone_number", [
    "07700900123",
    "07700 900 123",
    "+447700900123",
    "+44 7700 900123",
    "+44 7700 900 123"
])

@pytest.mark.parametrize("expected_failed_phone_number", [
    "12345",
    "notaphone",
    "1234567890123456",
    "0123456",
])

def test_phone_parsing(expected_successful_phone_number, expected_failed_phone_number):
    regexDetection = RegexDetection()

    assert regexDetection.phone_parse(expected_successful_phone_number) == [
        PIIEntity(
            text = expected_successful_phone_number,
            pii_type = PIIType.PHONE,
            start = 0,
            end = len(expected_successful_phone_number),
            confidence = 1.0,
            layer = DetectionLayer.REGEX 
        )
    ]

    assert regexDetection.phone_parse(expected_failed_phone_number) == []

@pytest.mark.parametrize("expected_successful_ni_number", [
    "AB 12 34 56 A",
    "AB123456A",
    "ZY 98 76 54 B",
    "TN 12 34 56 C",
])

@pytest.mark.parametrize("expected_failed_ni_number", [
    "DA 12 34 56 A",
    "AB 12 34 56 E",
    "1234567890",
    "ABCDEFGHI",
])

def test_ni_number_parsing(expected_successful_ni_number, expected_failed_ni_number):
   regexDetection = RegexDetection()

   assert regexDetection.ni_parse(expected_successful_ni_number) == [
        PIIEntity(
            text = expected_successful_ni_number,
            pii_type = PIIType.NI_NUMBER,
            start = 0,
            end = len(expected_successful_ni_number),
            confidence = 1.0,
            layer = DetectionLayer.REGEX 
        ) 
   ]

   assert regexDetection.ni_parse(expected_failed_ni_number) == []

@pytest.mark.parametrize("expected_successful_postal_code", [
    "SW1A 2AA",
    "M1 1AE",
    "B1 1BB",
    "NN1 1AA",
])

@pytest.mark.parametrize("expected_failed_postal_code", [
    "12345",
    "ABCDE",
    "SW1A",
    "1A 2AA",
])

def test_postal_code_parsing(expected_successful_postal_code, expected_failed_postal_code):
    regexDetection = RegexDetection()

    assert regexDetection.postcode_parse(expected_successful_postal_code) == [
        PIIEntity(
            text = expected_successful_postal_code,
            pii_type = PIIType.POSTCODE,
            start = 0,
            end = len(expected_successful_postal_code),
            confidence = 1.0,
            layer = DetectionLayer.REGEX 
        )  
    ]

    assert regexDetection.postcode_parse(expected_failed_postal_code) == []

@pytest.mark.parametrize("expected_successful_credit_card", [
    "1234567890123456",
    "1234 5678 9012 3456",
    "1234-5678-9012-3456",
])

@pytest.mark.parametrize("expected_failed_credit_card", [
    "12345678901234",
    "123456789012345678",
    "abcdefghijklmnop",
])

def test_credit_card_parsing(expected_successful_credit_card, expected_failed_credit_card):
    regexDetection = RegexDetection()

    assert regexDetection.creditcard_parse(expected_successful_credit_card) == [
        PIIEntity(
            text = expected_successful_credit_card,
            pii_type = PIIType.CREDIT_CARD,
            start = 0,
            end = len(expected_successful_credit_card),
            confidence = 1.0,
            layer = DetectionLayer.REGEX
        )
    ]

    assert regexDetection.creditcard_parse(expected_failed_credit_card) == []

@pytest.mark.parametrize("sample_input", [
    "Contact John at john@example.com or call 07700900123." +
    "His NI number is AB 12 34 56 A and postcode is SW1A 2AA." +
    "Card ending 1234 5678 9012 3456."
])

def test_detect_integrated_test(sample_input):
    regexDetection = RegexDetection()

    entities_list = regexDetection.detect(sample_input)

    assert len(entities_list) == 5
    assert any(e.pii_type == PIIType.EMAIL and e.text == "john@example.com" for e in entities_list)
    assert any(e.pii_type == PIIType.PHONE and e.text == "07700900123" for e in entities_list)
    assert any(e.pii_type == PIIType.NI_NUMBER and e.text == "AB 12 34 56 A" for e in entities_list)
    assert any(e.pii_type == PIIType.POSTCODE and e.text == "SW1A 2AA" for e in entities_list)
    assert any(e.pii_type == PIIType.CREDIT_CARD and e.text == "1234 5678 9012 3456" for e in entities_list)