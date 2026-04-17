from enum import Enum

class PIIType(Enum):
    NAME = "NAME"
    ADDRESS = "ADDRESS"
    EMAIL = "EMAIL"
    PHONE = "PHONE"
    POSTCODE = "POSTCODE"
    CREDIT_CARD = "CREDIT_CARD"
    NI_NUMBER = "NI_NUMBER"
    CONTEXTUAL = "CONTEXTUAL"
