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


def test_user_crud_endpoints(temp_db):
    app = create_app()
    client = TestClient(app)

    resp = client.post("/users/", json={"username": "dave", "password": "pw"})
    assert resp.status_code == 200

    resp = client.get("/users/dave")
    assert resp.status_code == 200
    assert resp.json()["username"] == "dave"

    resp = client.put("/users/dave", json={"password": "new"})
    assert resp.status_code == 200

    resp = client.delete("/users/dave")
    assert resp.status_code == 200
    assert db.get_user("dave") is None
