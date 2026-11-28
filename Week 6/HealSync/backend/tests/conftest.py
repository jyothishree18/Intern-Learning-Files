import os

# Set this before importing the application, because database.py reads DATABASE_URL
# while it is imported.
os.environ.setdefault("DATABASE_URL", "sqlite:///./healsync_test_bootstrap.db")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.db.database import Base, get_db
from app.core.auth import get_current_user


@pytest.fixture()
def db_session():
    test_engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(
        bind=test_engine,
        autoflush=False,
        autocommit=False,
    )

    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=test_engine)
        test_engine.dispose()


@pytest.fixture()
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = lambda: {
        "sub": "test-user-id",
        "preferred_username": "test-user",
        "realm_access": {"roles": ["admin"]},
    }

    # Do not enter TestClient as a context manager: that would run the app
    # lifespan, which creates tables on the configured DB and contacts MinIO.
    test_client = TestClient(app)
    try:
        yield test_client
    finally:
        test_client.close()
        app.dependency_overrides.clear()


@pytest.fixture()
def set_user():
    """Set the JWT payload returned by get_current_user for a test."""
    def _set_user(user_payload):
        app.dependency_overrides[get_current_user] = lambda: user_payload
    return _set_user
