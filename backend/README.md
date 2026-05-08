# Xiaohongmao Backend

FastAPI service for 小红贸.

## Local run

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8000
```

## Health check

```powershell
curl http://localhost:8000/health
```
