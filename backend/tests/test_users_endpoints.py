from fastapi.testclient import TestClient
from backend.shared_enums import UserRole


def test_users_list_and_update_role(client: TestClient, create_user, auth_header):
    # Create a superadmin and two admin users
    superadmin = create_user("super1", "pass123", role=UserRole.superadmin)
    user = create_user("user1", "pass123", role=UserRole.admin)
    admin_other = create_user("admin2", "pass123", role=UserRole.admin)

    # Auth as superadmin
    headers = auth_header("super1", "pass123")

    # List users (superadmin only)
    r = client.get("/api/v1/users/", headers=headers)
    assert r.status_code == 200, r.text
    users = r.json()
    assert any(u["username"] == "user1" for u in users)

    # Update user1 role to superadmin
    r = client.put(
        f"/api/v1/users/{user.id}/role",
        json={"role": "superadmin"},
        headers=headers,
    )
    assert r.status_code == 200, r.text
    data = r.json()
    assert data["role"] == "superadmin"

    # Non-superadmin should be forbidden for listing (use a different admin)
    headers_admin = auth_header("admin2", "pass123")
    r = client.get("/api/v1/users/", headers=headers_admin)
    assert r.status_code == 403
