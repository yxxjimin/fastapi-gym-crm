# FastAPI Template

FastAPI 템플릿
- ⚡️ **FastAPI**
- 📦 **Poetry**
- 🐳 **Docker Compose**
- 🐬 **MySQL**
- 🐘 **SQLAlchemy**

## Project Settings

- Python 3.12
- Poetry 1.8.3

## How to Run

### Install Dependencies
```bash
poetry install
```

### Database via Docker Compose
```bash
docker compose up -d
```

### Run Uvicorn
```bash
poetry run uvicorn main:app --port 8080
```
