# HealSync – Backend

## 1. Overview

The HealSync backend is developed using FastAPI. It provides REST APIs for managing patient information, hospital staff, and medical reports.

It integrates PostgreSQL for database management, Keycloak for authentication and authorization, and MinIO for medical report storage.

## 2. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| FastAPI | REST API development |
| PostgreSQL | Database |
| SQLAlchemy | Database ORM |
| Pydantic | Data validation |
| Keycloak | Authentication and role-based authorization |
| JWT | Token-based authentication |
| MinIO | Medical report storage |
| Docker | Application containerization |

## 3. Backend Folder Structure

```text
backend/
│
├── app/
│   ├── core/
│   │   └── Authentication and configuration
│   │
│   ├── db/
│   │   └── Database, models and CRUD operations
│   │
│   ├── exceptions/
│   │   └── Custom exceptions and handlers
│   │
│   ├── routes/
│   │   └── API endpoints
│   │
│   ├── schemas/
│   │   └── Pydantic schemas
│   │
│   ├── services/
│   │   └── Business logic
│   │
│   └── main.py
│
├── Dockerfile
├── requirements.txt
└── README.md
```

## 4. Main Backend Modules

### Patient Management
- Register new patients.
- Retrieve patient details.
- Update patient information.
- Delete patient records.
- Verify patient ownership.

### Staff Management
- Create staff accounts.
- Retrieve staff details.
- Delete staff records.
- Validate staff roles and email uniqueness.

### Medical Report Management
- Upload medical reports.
- Retrieve report details.
- Manage report records.
- Generate report download URLs.
- Store files using MinIO.

### Authentication and Authorization
- Validate Keycloak access tokens.
- Verify user roles.
- Restrict API access based on permissions.
- Use a Keycloak service account for user management.

## 5. API Endpoints

The main API resources are:

| Resource | Endpoint | Purpose |
|---|---|---|
| Patients | `/patients` | Patient management |
| Patient Details | `/patients/{patient_id}` | Retrieve individual patient |
| Staff | `/staff` | Staff management |
| Reports | `/reports` | Medical report management |

Refer to Swagger UI for the complete endpoint list and HTTP methods.

## 6. Environment Configuration

Create a `.env` file in the main HealSync project directory using `.env.example`.

Configure the required environment variables for:

- PostgreSQL connection
- Keycloak server
- Keycloak service account
- MinIO credentials
- S3 bucket configuration

Do not hardcode passwords, client secrets, or other sensitive credentials in source code.

## 7. Installation and Execution

### Prerequisites
- Python 3.12+
- Docker Desktop
- Docker Compose

### Run using Docker Compose

From the main `HealSync/` directory:

```bash
docker compose up -d --build backend
```

Check backend logs:

```bash
docker compose logs -f backend
```

### Access Swagger UI

Open the following URL:

http://localhost:8000/docs

Swagger UI allows you to explore and test the backend API endpoints.

## 8. Database

PostgreSQL is used to store:

- Patient information
- Staff information
- Medical report metadata

SQLAlchemy is used to interact with the database.

## 9. Authentication and Security

HealSync uses Keycloak for authentication and role-based access control.

Supported roles:

- Admin
- Doctor
- Lab Technician
- Patient

Patients are restricted to accessing their own records. Protected endpoints require valid authentication and appropriate permissions.

## 10. File Storage

MinIO is used for storing uploaded medical report files.

The backend communicates with MinIO through the internal Docker network and provides download URLs for accessing reports.

## 11. API Testing

API endpoints can be tested using:

- Swagger UI
- Postman

Authentication-protected endpoints require a valid Keycloak access token.

---

**HealSync Backend – FastAPI-based REST API for secure hospital medical report management.**
