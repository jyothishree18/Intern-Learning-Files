# HealSync – Hospital Medical Report Management System

## 1. Project Overview

HealSync is a hospital medical report management system designed to manage patient information, staff details, and medical reports securely.

The application provides role-based access control and centralized medical report storage. It uses Keycloak for authentication and authorization, PostgreSQL for database management, and MinIO for object storage.

## 2. Technologies Used

| Component | Technology |
|---|---|
| Backend | Python, FastAPI |
| Frontend | React |
| Database | PostgreSQL |
| Authentication | Keycloak |
| Object Storage | MinIO |
| Containerization | Docker, Docker Compose |
| API Testing | Swagger UI, Postman |

## 3. User Roles

- **Admin:** Manages patients, staff, and system operations.
- **Doctor:** Accesses authorized patient information and medical reports.
- **Lab Technician:** Manages medical report uploads.
- **Patient:** Can access their own medical information and reports.

## 4. Project Structure

```text
HealSync/
│
├── backend/
│   ├── app/
│   ├── Dockerfile
│   └── requirements.txt
│
├── frontend/
│   ├── src/
│   └── Dockerfile
│
├── keycloak/
│   └── healsync-realm.json
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## 5. Prerequisites

Install the following before running the project:

- Docker Desktop
- Docker Compose
- Git

## 6. Environment Configuration

Clone the repository:

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd HealSync
```

Create your environment file:

```bash
cp .env.example .env
```

On Windows PowerShell, you can use:

```powershell
Copy-Item .env.example .env
```

Update `.env` with your local development credentials.

Do not commit `.env` or real passwords to GitHub.

## 7. Run the Application

Build and start all services:

```bash
docker compose up -d --build
```

Check running containers:

```bash
docker compose ps
```

View logs:

```bash
docker compose logs -f
```

Stop the application:

```bash
docker compose down
```

Persistent database and storage volumes are configured in Docker Compose.

## 8. Application URLs

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| Keycloak Admin Console | http://localhost:8080 |
| MinIO Console | http://localhost:9001 |
| PostgreSQL | localhost:5432 |

## 9. Keycloak Configuration

HealSync uses Keycloak for user authentication and role-based authorization.

The project configures:

- A dedicated `healsync` realm.
- Frontend client configuration.
- Admin, doctor, lab technician, and patient roles.
- Backend service-account authentication.

The Docker Compose configuration starts Keycloak with realm import enabled.

Realm export file:

```text
keycloak/healsync-realm.json
```

Use the development admin credentials configured in `.env` to access the Keycloak Admin Console.

## 10. Database

HealSync uses PostgreSQL to store application data, including patient, staff, and medical report information.

Docker Compose manages the PostgreSQL database and persistent storage.

## 11. Medical Report Storage

HealSync uses MinIO for storing uploaded medical report files.

The backend connects to MinIO through the internal Docker network.

The configured bucket name is:

```text
healsync-reports
```

The backend provides report download URLs for accessing stored files.

## 12. Security Features

- Keycloak-based authentication.
- Role-based access control.
- Patient ownership verification.
- Protected API endpoints.
- Service-account authentication for Keycloak user management.
- Environment-based configuration for sensitive credentials.

## 13. API Documentation

After starting the application, open:

http://localhost:8000/docs

Use Swagger UI to explore and test the available API endpoints.

---

**HealSync – Secure and Centralized Hospital Medical Report Management.**
