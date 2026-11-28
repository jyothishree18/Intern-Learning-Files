# HealSync – Frontend

## 1. Overview

The HealSync frontend is developed using React. It provides a user-friendly interface for managing hospital patients, staff members, and medical reports.

The frontend communicates with the FastAPI backend through REST APIs and uses Keycloak for user authentication and role-based access.

## 2. Technologies Used

| Technology | Purpose |
|---|---|
| React | Frontend development |
| JavaScript | Application logic |
| HTML5 | Page structure |
| CSS3 | Styling and layout |
| Vite | Development server and build tool |
| Axios / Fetch API | Backend API communication |
| Keycloak | Authentication and authorization |

## 3. Folder Structure

```text
Frontend/
│
├── public/
│   └── Images and static assets
│
├── src/
│   ├── assets/
│   ├── components/
│   ├── pages/
│   ├── services/
│   ├── App.jsx
│   ├── App.css
│   ├── index.css
│   └── main.jsx
│
├── index.html
├── package.json
├── package-lock.json
├── vite.config.js
├── Dockerfile
└── README.md
```

## 4. Main Features

### Patient Management
- Add new patients.
- View patient details.
- Edit patient information.
- Delete patient records.

### Staff Management
- Add hospital staff members.
- View staff details.
- Manage staff information.

### Medical Report Management
- Upload medical reports.
- View uploaded reports.
- Access report download URLs.

### Authentication
- Keycloak-based login.
- Role-based access.
- Protected application pages.

## 5. User Roles

The frontend supports the following user roles:

- **Admin:** Accesses administrative features.
- **Doctor:** Accesses authorized patient and report information.
- **Lab Technician:** Manages medical report uploads.
- **Patient:** Views their own medical information and reports.

## 6. Prerequisites

Install the following:

- Node.js 20+
- npm
- Docker Desktop

## 7. Installation

Navigate to the Frontend directory:

```bash
cd Frontend
```

Install dependencies:

```bash
npm install
```

## 8. Run the Frontend Locally

Start the development server:

```bash
npm run dev
```

Open the application:

http://localhost:5173

## 9. Backend Integration

The frontend communicates with the FastAPI backend using REST API endpoints.

Backend API:

http://localhost:8000

Swagger documentation:

http://localhost:8000/docs

The frontend uses the configured backend API address to perform patient, staff, and medical report operations.

## 10. Run Using Docker

From the main HealSync project directory:

```bash
docker compose up -d --build frontend
```

Check frontend logs:

```bash
docker compose logs -f frontend
```

Access the application:

http://localhost:5173

## 11. Authentication and Security

Keycloak is integrated to provide authentication and role-based access control.

The frontend uses authentication tokens when communicating with protected backend endpoints.

Sensitive credentials and environment-specific configuration should not be committed to GitHub.

## 12. Build for Production

To create a production build:

```bash
npm run build
```

The generated production files are stored in the `dist/` directory.

---

**HealSync Frontend – A React-based interface for hospital medical report management.**
