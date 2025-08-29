from fastapi.testclient import TestClient
from server.app import create_app
from server import db


def test_app_includes_routes():
    app = create_app()
    client = TestClient(app)
    paths = [route.path for route in app.router.routes]
    assert "/auth/login" in paths
    assert "/stream/ping" in paths
    assert "/metadata/sync" in paths

    db.add_user("alice", "pw")
    token = client.post(
        "/auth/login", json={"username": "alice", "password": "pw"}
    ).json()["access_token"]

    ingest = client.get("/ingestion/ping")
    assert ingest.json()["status"] in {"ok", "db_unreachable"}

    meta = client.get("/metadata/ping").json()
    assert "metadata placeholder" not in meta.values()

    user_status = client.get("/users/ping").json()["status"]
    assert user_status in {"ok", "db_unreachable"}

    stream = client.get(
        "/stream/ping", headers={"Authorization": f"Bearer {token}"}
    )
    assert stream.json()["status"] in {"ok", "db_unreachable"}
