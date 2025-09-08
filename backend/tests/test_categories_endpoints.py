from fastapi.testclient import TestClient
from backend.shared_enums import UserRole


def test_category_crud_flow(client: TestClient, create_user, auth_header):
    # Create admin and get token
    admin = create_user("admin1", "pass123", role=UserRole.admin)
    headers = auth_header("admin1", "pass123")

    # Create category
    payload = {"name": "Safety", "description": "Safety related"}
    r = client.post("/api/v1/categories/", json=payload, headers=headers)
    assert r.status_code == 201, r.text
    cat = r.json()
    assert cat["name"] == "Safety"

    # Duplicate should 409
    r = client.post("/api/v1/categories/", json=payload, headers=headers)
    assert r.status_code == 409

    # List categories (auth required)
    r = client.get("/api/v1/categories/", headers=headers)
    assert r.status_code == 200
    rows = r.json()
    assert any(c["name"] == "Safety" for c in rows)

    # Get category by id
    r = client.get(f"/api/v1/categories/{cat['id']}", headers=headers)
    assert r.status_code == 200
    assert r.json()["id"] == cat["id"]

    # Update category
    upd = {"name": "Safety Gear", "description": "Updated"}
    r = client.put(f"/api/v1/categories/{cat['id']}", json=upd, headers=headers)
    assert r.status_code == 200
    assert r.json()["name"] == "Safety Gear"

    # Delete category
    r = client.delete(f"/api/v1/categories/{cat['id']}", headers=headers)
    assert r.status_code == 204

    # Get after delete -> 404
    r = client.get(f"/api/v1/categories/{cat['id']}", headers=headers)
    assert r.status_code == 404
