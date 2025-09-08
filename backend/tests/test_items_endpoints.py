from fastapi.testclient import TestClient
from backend.shared_enums import UserRole


def test_items_crud_flow_minimal(client: TestClient, create_user, auth_header):
    # Auth as admin
    admin = create_user("admin_items", "pass123", role=UserRole.admin)
    headers = auth_header("admin_items", "pass123")

    # Create item (no category)
    payload = {
        "unique_id": "SKU-001",
        "name": "Harness",
        "description": "Safety harness",
        "state": "good",
    }
    r = client.post("/api/v1/items/", json=payload, headers=headers)
    assert r.status_code == 200, r.text
    item = r.json()
    assert item["unique_id"] == "SKU-001"
    item_id = item["id"]

    # List items
    r = client.get("/api/v1/items/")
    assert r.status_code == 200
    assert any(row["id"] == item_id for row in r.json())

    # Delete item
    r = client.delete(f"/api/v1/items/{item_id}", headers=headers)
    assert r.status_code == 200
    assert r.json()["id"] == item_id
