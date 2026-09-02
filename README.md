# ResQGrid

ResQGrid is an emergency incident dispatch platform. Phase 1 provides the
PostgreSQL/PostGIS schema, async FastAPI service, and nearest-responder
assignment flow.

## Phase 1 architecture

- `docker-compose.yml` runs PostgreSQL with PostGIS and Redis.
- `backend/app/db/` contains the async SQLAlchemy engine and four core models:
   `responders`, `responder_locations`, `incidents`, and `incident_assignments`.
- `backend/app/services/dispatch_service.py` finds the nearest available
   responder within 5 km and commits the assignment transaction.
- `backend/app/api/dispatch.py` exposes `POST /dispatch/{incident_id}`.
- `backend/app/main.py` exposes `/health`, `/health/db`, and registers the
   dispatch router.

The React frontend remains scaffolded for a later phase.

## Local development

Copy `.env.example` to `.env` if configuration overrides are needed, then start
the infrastructure:

```bash
docker compose up -d
```

From `backend/`, run the API with the repository virtual environment:

```powershell
$env:PYTHONPATH = "."
..\.venv\Scripts\python.exe -m uvicorn app.main:app --reload --port 8000
```

Open Swagger at `http://127.0.0.1:8000/docs` and use `POST /dispatch/{incident_id}`.
If port 8000 is occupied, choose another port such as `8001`.

## Health checks

```text
GET /health
GET /health/db
```

The database health endpoint confirms the async connection and reports the
installed PostGIS version.

## Dependencies

Backend dependencies are pinned in [`backend/requirements.txt`](backend/requirements.txt).
The Phase 1 stack includes FastAPI, Uvicorn, SQLAlchemy async, asyncpg, and
GeoAlchemy2.
