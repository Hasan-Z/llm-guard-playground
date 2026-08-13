# LLM-Guard Playground

An interactive FastAPI + Web UI for testing all features and scanners of [LLM-Guard](https://github.com/protectai/llm-guard).

## ⚠ Python Version Requirement

**Python 3.11.x is required.** (Tested on 3.11.9)

Python 3.12+ has known compatibility issues with LLM-Guard's dependencies (HuggingFace, torch, etc.).

Download Python 3.11.9: https://www.python.org/downloads/release/python-3119/

---

## Quick Start (Windows PowerShell)

### Step 1 — Setup (run once)

```powershell
.\setup_env.ps1
```

This will:
- Locate your Python 3.11 installation
- Create a `.venv` virtual environment
- Install `llm-guard`, `fastapi`, `uvicorn`

### Step 2 — Run (daily)

```powershell
.\run.ps1
```

This will:
- Activate the virtual environment
- Start the FastAPI server on `http://localhost:8000`
- Open the browser automatically

---

## Project Structure

```
llm-guard-playground/
├── backend/
│   ├── main.py              # FastAPI app + routes
│   ├── scanner_registry.py  # All 36 scanners with metadata
│   ├── scan_engine.py       # Scanner instantiation + scan logic
│   └── models.py            # Pydantic request/response schemas
├── frontend/
│   └── index.html           # Single-page UI
├── setup_env.ps1            # One-time environment setup
├── run.ps1                  # Daily launcher
└── README.md
```

---

## Scanners Supported

### Input Scanners (15)
| Scanner | Heavy Model | Configurable |
|---|---|---|
| Anonymize | ✅ | — |
| BanCode | — | — |
| BanCompetitors | — | ✅ |
| BanSubstrings | — | ✅ |
| BanTopics | ✅ | ✅ |
| Code | — | ✅ |
| Gibberish | ✅ | — |
| InvisibleText | — | — |
| Language | — | ✅ |
| PromptInjection | ✅ | — |
| Regex | — | ✅ |
| Secrets | — | — |
| Sentiment | — | ✅ |
| TokenLimit | — | ✅ |
| Toxicity | ✅ | ✅ |

### Output Scanners (21)
BanCode, BanCompetitors, BanSubstrings, BanTopics, Bias, Code, Deanonymize, JSON, Language, LanguageSame, MaliciousURLs, NoRefusal, ReadingTime, FactualConsistency, Gibberish, Regex, Relevance, Sensitive, Sentiment, Toxicity, URLReachability

---

## Notes

- **Heavy scanners** (marked ⚡ in UI) download HuggingFace models on first use. This can take a minute and requires internet access.
- **Output scanners** in this playground run on the sanitized input text (since there's no real LLM connected yet). You can connect a real LLM later via the `/scan` endpoint.
- **Strict Mode** stops the pipeline at the first failed scanner.
- **Warn mode** (default) shows all results even when scanners fail.

---

## API Endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/` | Serves the Web UI |
| `GET` | `/scanners` | Returns all scanner metadata |
| `POST` | `/scan` | Runs selected scanners on a message |
| `GET` | `/health` | Health check |

### POST /scan — Request Body

```json
{
  "message": "Your prompt here",
  "input_scanners": [
    { "name": "Toxicity", "params": { "threshold": 0.5 } },
    { "name": "BanSubstrings", "params": { "substrings": "badword, secret" } }
  ],
  "output_scanners": [
    { "name": "Sentiment", "params": { "threshold": -0.1 } }
  ],
  "strict_mode": false
}
```