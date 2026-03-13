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

### Environment (MongoDB, scheduler)

Copy `.env.example` to `.env` and set `MONGODB_URL` (default `mongodb://localhost:27017`). MongoDB must be running for the app and the daily trends job.

### Sample routes

- `GET /` — service info
- `GET /health` — health check
- `GET /api/v1/hello` — sample message
- `GET /api/v1/items/{item_id}?q=...` — sample path/query
- `POST /api/v1/trends/run-job` — run Google trends job now (fetch top 5, store in MongoDB)
- `GET /api/v1/trends/latest?limit=10` — latest stored trends

### Daily Google trends job

A job runs **every day at 9 AM** (server time): it fetches the top 5 Google trending searches and stores them in the `google_trends` collection. Configure via env: `TRENDS_JOB_CRON`, `TRENDS_TOP_N`, `TRENDS_COUNTRY`. See `.env.example`.

Add more APIs under `app/routers/` and register them in `app/main.py`.
