# tti
Text to Image - sample

## API (FastAPI)

### Setup

```bash
cd tti
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

If you get SSL/certificate errors (e.g. "No matching distribution found" with "from versions: none"), use:

```bash
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r requirements.txt
```

### Run

From the `tti` directory (with venv activated):

```bash
python -m uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000
- Docs (Swagger): http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### Sample routes

- `GET /` — service info
- `GET /health` — health check
- `GET /api/v1/hello` — sample message
- `GET /api/v1/items/{item_id}?q=...` — sample path/query

Add more APIs under `app/routers/` and register them in `app/main.py`.
