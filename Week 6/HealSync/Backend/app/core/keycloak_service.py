
import json
import os
import urllib.request 
import urllib.error
from urllib.parse import quote


KEYCLOAK_URL = os.getenv(
    "KEYCLOAK_URL", "http://localhost:8080"
).rstrip("/")

KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "healsync")
ADMIN_REALM = os.getenv("KEYCLOAK_ADMIN_REALM", "master")
ADMIN_USERNAME = os.getenv("KEYCLOAK_ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("KEYCLOAK_ADMIN_PASSWORD")


def request_keycloak(method, url, token=None, data=None):
    headers = {"Content-Type": "application/json"}

    if token:
        headers["Authorization"] = f"Bearer {token}"

    body = json.dumps(data).encode() if data is not None else None

    request = urllib.request.Request(
        url,
        data=body,
        headers=headers,
        method=method,
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            response_body = response.read().decode()

            return (
                response.status,
                response.headers,
                json.loads(response_body) if response_body else None,
            )

    except urllib.error.HTTPError as error:
        detail = error.read().decode()
        raise RuntimeError(
            f"Keycloak returned {error.code}: {detail}"
        ) from error


def get_admin_token():
    if not ADMIN_USERNAME or not ADMIN_PASSWORD:
        raise RuntimeError(
            "Keycloak admin credentials are missing from .env"
        )

    url = (
        f"{KEYCLOAK_URL}/realms/{ADMIN_REALM}"
        "/protocol/openid-connect/token"
    )

    data = (
        "client_id=admin-cli"
        "&grant_type=password"
        f"&username={quote(ADMIN_USERNAME)}"
        f"&password={quote(ADMIN_PASSWORD)}"
    ).encode()

    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Content-Type": "application/x-www-form-urlencoded"
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return json.loads(
                response.read().decode()
            )["access_token"]

    except urllib.error.HTTPError as error:
        raise RuntimeError(
            "Unable to authenticate with Keycloak admin. "
            "Check admin credentials and admin-cli configuration."
        ) from error


def create_user_account(email, password, full_name, role):
    allowed_roles = {"patient", "doctor", "lab_tech"}

    if role not in allowed_roles:
        raise ValueError("Invalid user role.")

    token = get_admin_token()

    users_url = (
        f"{KEYCLOAK_URL}/admin/realms/{KEYCLOAK_REALM}/users"
    )

    # Check for an existing account.
    search_url = f"{users_url}?email={quote(email)}&exact=true"

    _, _, existing_users = request_keycloak(
        "GET", search_url, token
    )

    if existing_users:
        raise ValueError(
            "An account with this email already exists."
        )

    names = full_name.strip().split(maxsplit=1)

    user_data = {
        "username": email,
        "email": email,
        "firstName": names[0],
        "lastName": names[1] if len(names) > 1 else "",
        "enabled": True,
        "emailVerified": False,
        "credentials": [
            {
                "type": "password",
                "value": password,
                "temporary": True,
            }
        ],
    }

    _, headers, _ = request_keycloak(
        "POST", users_url, token, user_data
    )

    location = headers.get("Location")

    if not location:
        raise RuntimeError(
            "Keycloak created the user but returned no user ID."
        )

    user_id = location.rstrip("/").split("/")[-1]

    try:
        # Find the requested realm role.
        role_url = (
            f"{KEYCLOAK_URL}/admin/realms/{KEYCLOAK_REALM}"
            f"/roles/{role}"
        )

        _, _, realm_role = request_keycloak(
            "GET", role_url, token
        )

        # Assign the role.
        mapping_url = (
            f"{users_url}/{user_id}/role-mappings/realm"
        )

        request_keycloak(
            "POST", mapping_url, token, [realm_role]
        )

        return user_id

    except Exception:
        try:
            request_keycloak(
                "DELETE",
                f"{users_url}/{user_id}",
                token,
            )
        except Exception:
            pass

        raise


def create_patient_account(email, password, full_name):
    return create_user_account(
        email, password, full_name, "patient"
    )


def delete_patient_account(user_id):
    token = get_admin_token()

    users_url = (
        f"{KEYCLOAK_URL}/admin/realms/{KEYCLOAK_REALM}/users"
    )

    request_keycloak(
        "DELETE",
        f"{users_url}/{user_id}",
        token,
    )
