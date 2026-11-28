# HealSync – Hospital Medical Report Management System

## 1. Project Overview

HealSync is a hospital medical report management system designed to securely manage patient information, staff details, and medical reports.

The application provides role-based access control and centralized medical report storage. It uses Keycloak for authentication and authorization, PostgreSQL for database management, and MinIO for object storage.

The system is developed using FastAPI and React and deployed using Docker Compose.

## 2. Technologies Used

| Component | Technology |
|---|---|
| Backend | Python, FastAPI |
| Frontend | React |
| Database | PostgreSQL |
| Authentication and Authorization | Keycloak |
| Object Storage | MinIO |
| Containerization | Docker, Docker Compose |
| API Testing | Swagger UI, Postman |
| Programming Language | Python, JavaScript |

## 3. User Roles

HealSync supports role-based access control through Keycloak.

- **Admin:** Manages patients, staff, and system operations.
- **Doctor:** Accesses authorized patient information and medical reports.
- **Lab Technician:** Manages medical report uploads.
- **Patient:** Can access their own medical information and reports.

Each role has permissions based on its responsibilities.

## 4. Project Structure

```text
HealSync/
│
├── backend/
│   ├── app/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── README.md
│
├── frontend/
│   ├── src/
│   ├── Dockerfile
│   ├── package.json
│   └── README.md
│
├── keycloak/
│   ├── healsync-realm-export.json
│   └── README.md
│
├── docker-compose.yml
├── .env.example
├── .gitignore
└── README.md
```

## 5. Prerequisites

Install the following software before running the project:

- Docker Desktop
- Docker Compose
- Git
- A modern web browser

Make sure Docker Desktop is running before executing Docker Compose commands.

## 6. Environment Configuration

The project uses environment variables to manage database credentials, Keycloak configuration, and object storage credentials.

### Step 1: Create the environment file

Copy `.env.example` and create a local `.env` file in the HealSync project root.

**Windows PowerShell:**

```powershell
Copy-Item .env.example .env
```

**Linux/macOS:**

```bash
cp .env.example .env
```

### Step 2: Configure environment variables

Open `.env` and update the required development credentials.

The configuration includes:

- PostgreSQL database credentials.
- Keycloak administrator credentials.
- Keycloak backend service-account client ID and secret.
- MinIO root credentials.
- S3 access key and secret key.
- Storage bucket configuration.

Use your own local development values.

**Security Note:** Never upload `.env` or expose actual passwords, API credentials, or client secrets on GitHub. Only commit `.env.example` with placeholder values.

## 7. Run the Application Using Docker Compose

Run all HealSync services from the project root directory.

### Step 1: Build and start services

```bash
docker compose up -d --build
```

### Step 2: Check container status

```bash
docker compose ps
```

Verify that the required services are running and that database and storage health checks pass.

### Step 3: View application logs

```bash
docker compose logs -f
```

To view backend logs separately:

```bash
docker compose logs -f backend
```

### Step 4: Stop the application

```bash
docker compose down
```

Docker Compose uses persistent volumes for database and object-storage data.

## 8. Application URLs

After successfully starting the services, access the application through the following URLs.

| Service | URL |
|---|---|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| Swagger UI | http://localhost:8000/docs |
| Keycloak Admin Console | http://localhost:8080 |
| MinIO Console | http://localhost:9001 |
| PostgreSQL | Internal Docker network: `db:5432` |

**Note:** PostgreSQL is accessed internally by the backend through the Docker network. Its port is not published to the host machine.

## 9. Keycloak Configuration

HealSync uses Keycloak as its Identity and Access Management (IAM) solution.

Keycloak provides user authentication, authorization, and role-based access control.

### Realm Configuration

- **Realm Name:** `healsync`
- **Identity Provider:** Keycloak
- **Backend Client:** `healsync-backend`
- **Frontend Client:** `healsync-frontend`

### Backend Service Account

The backend uses a confidential Keycloak client with service accounts enabled.

The service account allows the backend to communicate with Keycloak for authorized user-management operations.

The client credentials are configured through environment variables.

### Realm Import

The Keycloak realm configuration is stored in:

```text
keycloak/healsync-realm-export.json
```

Docker Compose starts Keycloak with realm import enabled.

### Application Roles

- `admin`
- `doctor`
- `lab_tech`
- `patient`

Access to application features is controlled according to assigned roles and permissions.

## 10. Database Management

HealSync uses PostgreSQL as its relational database.

It stores application information, including:

- Patient details.
- Staff information.
- Medical report metadata.
- Related application records.

The backend communicates with PostgreSQL through SQLAlchemy.

Docker Compose manages the database container and persistent storage volume.

## 11. Medical Report Storage

HealSync uses MinIO for object storage of uploaded medical reports.

The backend communicates with MinIO through the internal Docker network.

### Storage Configuration

- **Storage Service:** MinIO
- **Bucket Name:** `healsync-reports`
- **Internal Endpoint:** `http://minio:9000`
- **Console:** `http://localhost:9001`

The backend provides report download URLs for accessing stored files.

## 12. Security Features

HealSync implements the following security features:

- Keycloak-based authentication.
- Role-based access control.
- Patient ownership verification.
- Protected API endpoints.
- Backend service-account authentication.
- Environment-based configuration for sensitive credentials.
- Separation of application services using Docker Compose.
- Restricted PostgreSQL host-port exposure.

## 13. API Documentation and Testing

HealSync provides interactive API documentation through Swagger UI.

After starting the application, open:

http://localhost:8000/docs

Swagger UI can be used to:

- Explore available API endpoints.
- View request and response schemas.
- Submit API requests.
- Test authentication-protected endpoints.
- Verify API responses.

Postman can also be used for API testing and authentication workflows.

## 14. GitHub and Configuration Security

The project uses `.gitignore` to exclude sensitive and unnecessary files.

The following files and directories should not be committed:

- `.env`
- Python virtual environments.
- `__pycache__/`
- `node_modules/`
- Build and temporary files.

The `.env.example` file is provided as a template for configuring the application.

Never commit real credentials or access tokens.

---

**HealSync – Secure and Centralized Hospital Medical Report Management System.**
