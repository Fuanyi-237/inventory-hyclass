from fastapi.testclient import TestClient
from datetime import datetime, timezone
from backend.shared_enums import UserRole


def test_transaction_create_and_list(client: TestClient, create_user, auth_header):
    # Create admin and auth
    admin = create_user("admin_tx", "pass123", role=UserRole.admin)
    headers = auth_header("admin_tx", "pass123")

    # Create an item first
    item_payload = {
        "unique_id": "SKU-TX-1",
        "name": "Helmet",
        "description": "Safety helmet",
        "state": "good",
    }
    r = client.post("/api/v1/items/", json=item_payload, headers=headers)
    assert r.status_code == 200, r.text
    item_id = r.json()["id"]

    # Create a transaction for that item
    tx_payload = {
        "item_id": item_id,
        "user_id": admin.id,
        "action": "add",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "notes": "Initial stock",
        "state": "good",
    }
    r = client.post("/api/v1/transactions/", json=tx_payload, headers=headers)
    assert r.status_code == 201, r.text
    tx = r.json()
    assert tx["item_id"] == item_id

    # List transactions
    r = client.get("/api/v1/transactions/")
    assert r.status_code == 200
    rows = r.json()
    assert any(t["id"] == tx["id"] for t in rows)
