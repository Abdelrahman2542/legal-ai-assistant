# legal-ai-assistant

## Requirements 
- Python `3.13.5`

---

## Installation

### 1. Create and Activate the Virtual Environment (venv)
```bash
python -m venv .venv
.venv\Scripts\activate
```
### 1. Install the required packages
```bash
cd src
pip install -r requirements.txt

```
### Setup the environment variables
```bash
copy .env.example .env
```
Set your environment variables in the .env file. Like OPENAI_API_KEY value

### Run fast api server
```bash
uvicorn main:app --reload
```