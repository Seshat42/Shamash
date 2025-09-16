from fastapi.testclient import TestClient
from server.app import create_app
from server import db


def test_ingest_creates_item(temp_db):
    app = create_app()
    client = TestClient(app)
    response = client.post(
        "/ingestion/",
        json={"title": "new", "path": "http://example.com/video.mp4"},
    )
    assert response.status_code == 200
    items = db.list_media_items()
    assert len(items) == 1
    assert items[0].title == "new"
    assert items[0].path == "http://example.com/video.mp4"


def test_ingest_accepts_local_file_path(temp_db, tmp_path):
    media_file = tmp_path / "movie.mp4"
    media_file.write_bytes(b"binary")

    app = create_app()
    client = TestClient(app)
    response = client.post(
        "/ingestion/",
        json={"title": "local", "path": str(media_file)},
    )

    assert response.status_code == 200
    items = db.list_media_items()
    assert len(items) == 1
    assert items[0].path == str(media_file.resolve())


def test_ingest_rejects_missing_local_file(temp_db, tmp_path):
    missing = tmp_path / "missing.mp4"

    app = create_app()
    client = TestClient(app)
    response = client.post(
        "/ingestion/",
        json={"title": "bad", "path": str(missing)},
    )

    assert response.status_code == 422
    detail = response.json()["detail"][0]
    assert detail["loc"][-1] == "path"
    assert "existing file" in detail["msg"]


def test_ingest_rejects_directory_traversal(temp_db):
    app = create_app()
    client = TestClient(app)
    response = client.post(
        "/ingestion/",
        json={"title": "bad", "path": "../etc/passwd"},
    )

    assert response.status_code == 422
    detail = response.json()["detail"][0]
    assert detail["loc"][-1] == "path"
    assert "directory traversal" in detail["msg"]


def test_ingest_rejects_invalid_url(temp_db):
    app = create_app()
    client = TestClient(app)
    response = client.post(
        "/ingestion/",
        json={"title": "bad", "path": "ftp://example.com/video.mp4"},
    )

    assert response.status_code == 422
    detail = response.json()["detail"][0]
    assert detail["loc"][-1] == "path"
    assert "http or https" in detail["msg"]


def test_user_crud_endpoints(temp_db):
    db.add_user("admin", "pw", role="admin")
    app = create_app()
    client = TestClient(app)

    admin_token = client.post(
        "/auth/login", json={"username": "admin", "password": "pw"}
    ).json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}

    resp = client.post(
        "/users/", json={"username": "dave", "password": "pw"}, headers=admin_headers
    )
    assert resp.status_code == 200

    dave_token = client.post(
        "/auth/login", json={"username": "dave", "password": "pw"}
    ).json()["access_token"]
    user_headers = {"Authorization": f"Bearer {dave_token}"}

    resp = client.post(
        "/users/", json={"username": "eve", "password": "pw"}, headers=user_headers
    )
    assert resp.status_code == 403

    resp = client.get("/users/dave", headers=admin_headers)
    assert resp.status_code == 200
    assert resp.json()["username"] == "dave"
    assert resp.json()["role"] == "user"

    resp = client.put(
        "/users/dave", json={"password": "new"}, headers=admin_headers
    )
    assert resp.status_code == 200

    resp = client.delete("/users/dave", headers=admin_headers)
    assert resp.status_code == 200
    assert db.get_user("dave") is None
