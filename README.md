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
