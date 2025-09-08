from fastapi.testclient import TestClient
from backend.shared_enums import UserRole


def test_create_user_and_login_flow(client: TestClient):
    # Create user
    payload = {
        "username": "testuser",
        "full_name": "Test User",
        "email": "test@example.com",
        "role": "admin",
        "is_active": True,
        "password": "secret123",
    }
    r = client.post("/api/v1/users/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["username"] == "testuser"
    assert data["role"] == "admin"

    # Login
    form = {
        "grant_type": "password",
        "username": "testuser",
        "password": "secret123",
        "scope": "",
    }
    r = client.post("/api/v1/auth/token", data=form)
    assert r.status_code == 200, r.text
    token = r.json()["access_token"]

    # /me should work
    r = client.get("/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert r.status_code == 200, r.text
    me = r.json()
    assert me["username"] == "testuser"
