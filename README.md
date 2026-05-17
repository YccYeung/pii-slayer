<p align="center">
  <img src="frontend/src/pii_slayer_logo.svg" alt="PII Slayer" width="400" />
</p>

# PII Slayer

A three-layer PII detection and redaction tool built with FastAPI, spaCy NER, and Groq LLM. Supports raw text, PDF, and CSV inputs with both redaction and anonymisation modes.

## Supported Modes

**Text Mode** — paste text, detect PII across three detection layers, copy redacted output

**File Mode** — upload a PDF or CSV file, download visually redacted file with risk assessment

## Architecture

PII Slayer uses a confidence-based escalation pipeline:

1. **Regex (Layer 1)** — deterministic pattern matching for structured PII: emails, UK phone numbers, NI numbers, postcodes, credit cards
2. **spaCy NER (Layer 2)** — ML-based named entity recognition for names, organisations, addresses
3. **Groq LLM (Layer 3)** — contextual detection for indirect identifiers: usernames, place of birth, license plates, protected characteristics
4. **LLM Judge** — post-processing risk assessment that evaluates the redacted output and returns a sharability recommendation

## Features

- Three-layer detection pipeline with confidence-based escalation
- Two output modes: `REDACT` (replaces PII with `[REDACTED]`) and `ANONYMISE` (replaces with typed placeholders e.g. `PERSON_1`, `EMAIL_1`)
- PDF visual redaction using PyMuPDF bounding box coordinate mapping — black-box overlays with original layout preserved
- CSV cell-level redaction — replaces matching cells while keeping non-PII columns intact
- LLM-as-judge risk assessment with sharability recommendation (LOW / MEDIUM / HIGH / CRITICAL)
- React frontend with drag-and-drop file upload and one-click copy/download

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, FastAPI, Pydantic |
| Detection Layer 1 | Regex |
| Detection Layer 2 | spaCy (`en_core_web_sm`) |
| Detection Layer 3 + Judge | Groq API (`llama-3.3-70b-versatile`) |
| PDF Processing | PyMuPDF |
| CSV Processing | pandas |
| Frontend | React, TypeScript |

## Getting Started

### Prerequisites

- Python 3.12+
- Node.js 18+
- Groq API key (free at [console.groq.com](https://console.groq.com))

### Installation

```bash
git clone https://github.com/YccYeung/pii-slayer
cd pii-slayer
```

**Backend:**
```bash
cd Backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_sm
```

Create `Backend/.env`:
```
GROQ_API_KEY=your_groq_api_key_here
```

**Frontend:**
```bash
cd frontend
npm install
```

### Running

```bash
# Terminal 1 — backend
cd Backend && fastapi dev app/main.py

# Terminal 2 — frontend
cd frontend && npm start
```

Open [http://localhost:3000](http://localhost:3000)

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/v1/detect/text` | Detect and redact PII in raw text |
| POST | `/api/v1/detect/pdf` | Upload PDF, returns redacted PDF as base64 |
| POST | `/api/v1/detect/csv` | Upload CSV, returns redacted CSV as base64 |

## Known Limitations

- NER may produce false positives on common words used as organisation names (e.g. "Company", "Human Resources")
- LLM layer is non-deterministic — contextual detection results may vary between runs
- PDF redaction requires text-layer PDFs — scanned images are not supported
- CSV redaction operates at cell level — partial matches within a cell are not redacted