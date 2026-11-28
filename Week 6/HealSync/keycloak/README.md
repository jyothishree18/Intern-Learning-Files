# HealSync – Keycloak Configuration

## Overview
This folder contains the Keycloak realm configuration used for authentication and role-based access control in the HealSync application.

## Realm
- **Realm name:** `healsync`
- **Identity Provider:** Keycloak
- **Purpose:** Manage user authentication, authorization, and application roles.

## Client Configuration

### Backend Client
- **Client ID:** `healsync-backend`
- **Client type:** Confidential
- **Client authentication:** Enabled
- **Service accounts:** Enabled
- **Grant type:** Client Credentials

The backend uses this client to communicate securely with Keycloak.

### Frontend Client
The frontend client handles user login through Keycloak.

## Application Roles
- `admin` – Full system administration
- `doctor` – Doctor access
- `lab_tech` – Laboratory report management
- `patient` – Patient access

## Realm Import
The realm export file is stored in this folder:

`healsync-realm-export.json`

Keycloak imports the realm when the Docker Compose services start with realm import enabled.

## Security Notes
- Never commit actual client secrets or passwords.
- Store credentials in the local `.env` file.
- Keep `.env` excluded from GitHub.
- Use `.env.example` with placeholder values for documentation.

## Start Keycloak

From the HealSync project root, run:

```bash
docker compose up -d keycloak
```

Open the Keycloak administration console:

`http://localhost:8080`

