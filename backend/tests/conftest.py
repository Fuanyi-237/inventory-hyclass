import os
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient
from datetime import datetime

from backend.main import app
from backend import models
from backend.base import Base
from backend.dependencies import get_db
from backend.shared_enums import UserRole
from backend.password_utils import get_password_hash

# Create an in-memory SQLite database shared across threads
TEST_ENGINE = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=TEST_ENGINE)

# Create all tables once per test session
@pytest.fixture(scope="session", autouse=True)
def create_test_db():
    Base.metadata.create_all(bind=TEST_ENGINE)
    yield
    Base.metadata.drop_all(bind=TEST_ENGINE)

# Override get_db dependency to use the in-memory DB
@pytest.fixture(scope="function")
def db_session():
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture(scope="function", autouse=True)
def override_dependencies(db_session):
    def _get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = _get_db
    yield
    app.dependency_overrides.clear()

@pytest.fixture()
def client():
    return TestClient(app)

@pytest.fixture()
def create_user(db_session):
    def _create_user(username: str, password: str, role: UserRole = UserRole.admin, email: str | None = None):
        user = models.User(
            username=username,
            full_name=username.title(),
            email=email,
            hashed_password=get_password_hash(password),
            role=role,
            is_active=True,
        )
        db_session.add(user)
        db_session.commit()
        db_session.refresh(user)
        return user
    return _create_user

@pytest.fixture()
def auth_header(client, create_user):
    def _auth_header(username: str, password: str):
        # Ensure user exists (no-op if already exists due to unique constraint handling in tests)
        # Attempt to get a token
        data = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "scope": "",
        }
        response = client.post("/api/v1/auth/token", data=data)
        assert response.status_code == 200, response.text
        token = response.json()["access_token"]
        return {"Authorization": f"Bearer {token}"}
    return _auth_header
