from fastapi.testclient import TestClient
from server.app import create_app
from server import db


def _login(client: TestClient, username: str, password: str) -> dict[str, str]:
    response = client.post(
        "/auth/login", json={"username": username, "password": password}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _create_admin_client() -> tuple[TestClient, dict[str, str]]:
    db.add_user("admin", "pw", role="admin")
    app = create_app()
    client = TestClient(app)
    admin_headers = _login(client, "admin", "pw")
    return client, admin_headers


def test_ingest_creates_item(temp_db):
    client, admin_headers = _create_admin_client()
    response = client.post(
        "/ingestion/",
        json={"title": "new", "path": "http://example.com/video.mp4"},
        headers=admin_headers,
    )
    assert response.status_code == 200
    items = db.list_media_items()
    assert len(items) == 1
    assert items[0].title == "new"
    assert items[0].path == "http://example.com/video.mp4"


def test_ingest_accepts_local_file_path(temp_db, tmp_path):
    media_file = tmp_path / "movie.mp4"
    media_file.write_bytes(b"binary")

    client, admin_headers = _create_admin_client()
    response = client.post(
        "/ingestion/",
        json={"title": "local", "path": str(media_file)},
        headers=admin_headers,
    )

    assert response.status_code == 200
    items = db.list_media_items()
    assert len(items) == 1
    assert items[0].path == str(media_file.resolve())


def test_ingest_rejects_missing_local_file(temp_db, tmp_path):
    missing = tmp_path / "missing.mp4"

    client, admin_headers = _create_admin_client()
    response = client.post(
        "/ingestion/",
        json={"title": "bad", "path": str(missing)},
        headers=admin_headers,
    )

    assert response.status_code == 422
    detail = response.json()["detail"][0]
    assert detail["loc"][-1] == "path"
    assert "existing file" in detail["msg"]


def test_ingest_rejects_directory_traversal(temp_db):
    client, admin_headers = _create_admin_client()
    response = client.post(
        "/ingestion/",
        json={"title": "bad", "path": "../etc/passwd"},
        headers=admin_headers,
    )

    assert response.status_code == 422
    detail = response.json()["detail"][0]
    assert detail["loc"][-1] == "path"
    assert "directory traversal" in detail["msg"]


def test_ingest_rejects_invalid_url(temp_db):
    client, admin_headers = _create_admin_client()
    response = client.post(
        "/ingestion/",
        json={"title": "bad", "path": "ftp://example.com/video.mp4"},
        headers=admin_headers,
    )

    assert response.status_code == 422
    detail = response.json()["detail"][0]
    assert detail["loc"][-1] == "path"
    assert "http or https" in detail["msg"]


def test_ingest_rejects_missing_token(temp_db):
    db.add_user("admin", "pw", role="admin")
    app = create_app()
    client = TestClient(app)

    response = client.post(
        "/ingestion/",
        json={"title": "new", "path": "http://example.com/video.mp4"},
    )

    assert response.status_code == 403
    assert db.list_media_items() == []


def test_ingest_rejects_non_admin_role(temp_db):
    db.add_user("user", "pw", role="user")
    app = create_app()
    client = TestClient(app)
    user_headers = _login(client, "user", "pw")

    response = client.post(
        "/ingestion/",
        json={"title": "new", "path": "http://example.com/video.mp4"},
        headers=user_headers,
    )

    assert response.status_code == 403
    assert db.list_media_items() == []


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

    resp = client.put("/users/dave", json={"password": "new"}, headers=admin_headers)
    assert resp.status_code == 200

    resp = client.delete("/users/dave", headers=admin_headers)
    assert resp.status_code == 200
    assert db.get_user("dave") is None
