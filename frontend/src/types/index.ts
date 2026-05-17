export type PIIType = 'EMAIL' | 'PHONE' | 'NAME' | 'ADDRESS' | 'POSTCODE' | 'NI_NUMBER' | 'CREDIT_CARD' | 'ORG' | 'CONTEXTUAL';
export type DetectionLayer = 'REGEX' | 'NER' | 'LLM';
export type RedactionMode = 'REDACT' | 'ANONYMISE';
export type RiskScore = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export interface PIIEntity {
  text: string;
  pii_type: PIIType;
  start: number;
  end: number;
  confidence: number;
  layer: DetectionLayer;
}

export interface DetectionResponse {
  original_text: string;
  redacted_text: string;
  entities: PIIEntity[];
  entity_count: number;
  risk_score: RiskScore | null;
  recommendation: string | null;
}

export interface FileDetectionResponse {
  redacted_file: string;
  filename: string;
  entity_count: number;
  entities: PIIEntity[];
  risk_score: RiskScore | null;
  recommendation: string | null;
}
