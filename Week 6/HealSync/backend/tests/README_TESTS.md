# HealSync backend tests

These tests are written against the uploaded HealSync backend routes, schemas,
authentication dependency, and SQLAlchemy models.

## 1. Install test dependencies

From the `backend` directory:

```powershell
pip install -r requirements-dev.txt
```

Or add `pytest` and `httpx` to your existing backend development dependencies.

## 2. Expected folder structure

Place the `tests` folder beside the backend `app` folder:

```text
backend/
├── app/
│   ├── core/
│   ├── db/
│   ├── routes/
│   ├── schemas/
│   └── main.py
├── tests/
│   ├── conftest.py
│   ├── test_email_validation.py
│   ├── test_patient_permissions.py
│   ├── test_report_permissions.py
│   └── test_staff_permissions.py
└── requirements.txt
```

## 3. Run the tests

From the `backend` directory:

```powershell
python -m pytest -v
```

## Important notes

- Tests use a temporary in-memory SQLite database for test records.
- JWT authentication is overridden with controlled test claims; no live Keycloak login is needed.
- The app lifespan is not run, avoiding real database table creation and MinIO bucket calls.
- Patient and staff creation against Keycloak is not exercised in this first test set.
- These tests check the currently uploaded route behavior. If route paths or role names change, update the corresponding tests.
- The report ownership test assumes the first inserted report has ID 1 in the isolated in-memory database.
