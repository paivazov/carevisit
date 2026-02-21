# CareVisit Service

Test project with care visits.

## Setup & Run

**1. Install dependencies**
```bash
poetry install
```

**2. Configure environment**

Copy `.env.example` to `.env` and fill in the values (or edit `.env` directly).

**3. Apply migrations**
```bash
python manage.py migrate
```

**4. Pre-fill control sequences**
```bash
python manage.py prefill_control_sequences
```

**5. Create a superuser**
```bash
python manage.py createsuperuser
```

**6. Start the development server**
```bash
python manage.py runserver
```

**7. (Optional) Start Celery worker and beat**
```bash
celery -A CareVisitService worker -l warning
celery -A CareVisitService beat -l warning
```

## API Docs

Swagger UI is available at [http://localhost:8000/docs/](http://localhost:8000/docs/).

To authenticate, obtain a token via `POST /api/auth/token/` and enter `Bearer <token>` in the **Authorize** dialog.

---

## FastAPI Microservice — Visit Overlap Checker

A small service that checks if a caregiver already has a conflicting
visit for a proposed time window. It connects to the same PostgreSQL db as
the Django service in read-only mode.

### Install dependencies

```bash
cd fastapi_service
poetry install
```

### Run

```bash
uvicorn fastapi_service.main:app --reload --port 8001
```

Interactive docs available at [http://localhost:8001/docs](http://localhost:8001/docs).

### Endpoint

```
POST /visits/check-overlap
```

**Request body:**
```json
{
  "caregiver_id": 1,
  "start_date_time": "2026-02-21T10:00:00Z",
  "end_date_time": "2026-02-21T12:00:00Z"
}
```

**Response:**
```json
{
  "has_overlap": true,
  "conflicting_visit_id": 42
}
```

Returns `has_overlap: false` with `conflicting_visit_id: null` when no conflict is found.
