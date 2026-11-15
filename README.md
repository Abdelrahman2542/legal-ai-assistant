# Legal AI Assistant

An Arabic AI legal assistant for selected Egyptian laws, built on Retrieval-Augmented Generation (RAG). It retrieves relevant legal articles from a structured database and generates concise Arabic answers with citations (law name and article number).

> **Disclaimer:** This system is an assistive tool for locating legal provisions. It does not replace professional legal advice.

---

## Objective

To build an Arabic AI assistant that reliably answers users' questions about Egyptian law by retrieving relevant legal articles, providing clear citations (law name and article number), and reducing unverified responses.

---

## How It Works

```
User question (Arabic)
        ↓
Retrieval (semantic + keyword-based search)
        ↓
Answer generated only from the retrieved articles
        ↓
Verification step (cited articles must exist in the retrieved context)
        ↓
Answer + sources, or a refusal when no sufficient legal text is found
```

Legal texts are prepared offline: extracted from the official source, split article by article, validated, and stored with metadata (law, article number, source). Adding a new law should not require changes to the core pipeline.

---

## Project Status

- [x] Project structure and FastAPI skeleton
- [x] PDF text extraction (PyMuPDF)
- [ ] Article chunking and validation (in progress)
- [ ] Embeddings and semantic search
- [ ] Keyword search and hybrid retrieval
- [ ] Answer generation with citations
- [ ] Verification step
- [ ] User interface
- [ ] Evaluation on Arabic legal questions

**Initial scope:** Egyptian Labor Law (Law No. 14 of 2025). More laws will be added after the pipeline is validated.

---

## Requirements

- Python `3.13.5`

---

## Installation

### 1. Create and Activate the Virtual Environment (venv)
```bash
python -m venv .venv
.venv\Scripts\activate
```

On macOS / Linux:
```bash
source .venv/bin/activate
```

### 2. Install the required packages
```bash
cd src
pip install -r requirements.txt
```

### 3. Setup the environment variables
```bash
copy .env.example .env
```

On macOS / Linux:
```bash
cp .env.example .env
```

Set your environment variables in the `.env` file, like the `OPENAI_API_KEY` value.

### 4. Run the FastAPI server
```bash
uvicorn main:app --reload
```

- Health check: `http://127.0.0.1:8000/api/v1/`
- Interactive docs: `http://127.0.0.1:8000/docs`

---

## Repository Structure

```
legal-ai-assistant/
├── data/                  # Not tracked by Git
│   ├── raw/               # Original source files (never edited by hand)
│   ├── staging/           # Extracted text
│   └── processed/         # Final article chunks (JSON)
├── src/
│   ├── api/               # FastAPI: routes, controllers, schemas
│   ├── ingestion/         # Extraction, cleaning, chunking, validation
│   ├── retrieval/         # Embeddings and search
│   ├── generation/        # Prompting, LLM client, verification
│   ├── main.py            # FastAPI entry point
│   ├── config.py          # Settings loaded from .env
│   ├── requirements.txt
│   └── .env.example
└── README.md
```

---

## Data

Source files are **not** stored in this repository. Place them locally, one folder per law:

```
data/raw/<law folder>/<source file>.pdf
```

The primary source is the official Egyptian Gazette. Raw files are never modified: every later stage is generated from them by scripts, and manual fixes are kept in a separate `data/corrections.json` so they survive re-processing.

### Run the ingestion pipeline

From the repository root:

```bash
python src/ingestion/cleaner.py
python src/ingestion/chunker.py
```

---

## Team Workflow

- `main` is protected. Each feature is developed on its own branch.
- Changes are merged through Pull Requests reviewed by a teammate.
- Never commit `.env` files or API keys.
- Record experiment results (settings and metrics) for the final report.

---

## Team

| Name | Responsibility |
|---|---|
| [Name] | [Feature area] |
| [Name] | [Feature area] |
| [Name] | [Feature area] |
| [Name] | [Feature area] |

**Supervisor:** [Supervisor name]