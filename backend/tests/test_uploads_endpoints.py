from fastapi.testclient import TestClient
import io


def test_upload_image_success(client: TestClient):
    # Create an in-memory PNG file
    file_content = b"\x89PNG\r\n\x1a\n" + b"0" * 100
    files = {
        "file": ("test.png", io.BytesIO(file_content), "image/png"),
    }
    r = client.post("/api/v1/uploads/upload", files=files)
    assert r.status_code == 201, r.text
    data = r.json()
    assert "image_url" in data
    assert data["image_url"].startswith("/uploads/")


def test_upload_non_image_rejected(client: TestClient):
    files = {
        "file": ("not_image.txt", io.BytesIO(b"hello"), "text/plain"),
    }
    r = client.post("/api/v1/uploads/upload", files=files)
    assert r.status_code == 400
