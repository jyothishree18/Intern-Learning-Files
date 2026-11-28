
import os
import logging
from functools import lru_cache

import jwt
from jwt import PyJWKClient

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials


# Logger configuration
logger = logging.getLogger(__name__)


# Keycloak configuration
KEYCLOAK_URL = os.getenv(
    "KEYCLOAK_URL",
    "http://localhost:8080"
)

KEYCLOAK_REALM = os.getenv(
    "KEYCLOAK_REALM",
    "healsync"
)

# Public issuer URL present in the access token
ISSUER = os.getenv(
    "KEYCLOAK_ISSUER",
    f"http://localhost:8080/realms/{KEYCLOAK_REALM}"
)

# Internal Docker URL for retrieving public signing keys
JWKS_URL = (
    f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}"
    "/protocol/openid-connect/certs"
)

security = HTTPBearer()


@lru_cache(maxsize=1)
def get_jwks_client():
    return PyJWKClient(JWKS_URL)


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    token = credentials.credentials

    try:
        signing_key = (
            get_jwks_client()
            .get_signing_key_from_jwt(token)
        )

        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            issuer=ISSUER,
            options={
                "require": ["exp", "iss", "sub"],
                "verify_aud": False,
            },
        )

        return payload

    except jwt.PyJWTError as exc:
        logger.warning("JWT validation error: %s", exc)

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired access token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    except Exception:
        logger.exception("Authentication error")

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Unable to validate access token",
            headers={"WWW-Authenticate": "Bearer"},
        )


def require_roles(*allowed_roles):

    def role_checker(
        user=Depends(get_current_user)
    ):

        user_roles = (
            user.get("realm_access", {})
            .get("roles", [])
        )

        if not any(
            role in user_roles
            for role in allowed_roles
        ):

            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to perform this action",
            )

        return user

    return role_checker
