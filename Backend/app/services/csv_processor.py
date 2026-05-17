import pandas
from io import BytesIO, StringIO
from app.schemas.detection import PIIEntity

class CSVProcessor():

    def __init__(self):
        pass

    def extract_text(self, file: bytes) -> str:
        """
        Extract all cell values from a CSV file as a single string for pipeline processing.
    
        Flattens the DataFrame into a comma-separated string so the detection pipeline
        can process all cell content without needing to understand the CSV structure.

        Args:
            file (bytes): The CSV file content in bytes format.

        Returns:
            str: All cell values flattened into a single comma-separated string.
        """
        csv_file = pandas.read_csv(BytesIO(file))
        return ", ".join(csv_file.fillna("").astype(str).values.flatten())
        
    def detect(self, file: bytes, entities: list[PIIEntity]) -> bytes:
        """
        Apply PII redaction to a CSV file cell by cell.
    
        Builds a set of detected entity texts for O(1) lookup efficiency,
        then iterates over each cell and replaces any matching value with [REDACTED].
        Returns the redacted CSV as encoded bytes for the API response.

        Args:
            file (bytes): The original CSV file content in bytes format.
            entities (list[PIIEntity]): List of detected PII entities to redact.

        Returns:
            bytes: The redacted CSV file as encoded bytes for the API response.
        """
        csv_file = pandas.read_csv(BytesIO(file))

        entities_text = {e.text for e in entities}

        for col in csv_file.columns:
            for idx, cell in csv_file[col].items():
                if str(cell) in entities_text:
                    csv_file.at[idx, col] = "[REDACTED]"

        return csv_file.to_csv(index=False).encode()
            
def get_csv_processor():
    return CSVProcessor()