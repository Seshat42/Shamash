import logging

from fastapi.testclient import TestClient

from server import db
from server.app import create_app


def test_app_includes_routes():
    app = create_app()
    client = TestClient(app)
    paths = [route.path for route in app.router.routes]
    assert "/auth/login" in paths
    assert "/stream/ping" in paths
    assert "/metadata/sync" in paths

    db.add_user("alice", "pw", role="admin")
    token = client.post(
        "/auth/login", json={"username": "alice", "password": "pw"}
    ).json()["access_token"]

    ingest = client.get(
        "/ingestion/ping", headers={"Authorization": f"Bearer {token}"}
    )
    assert ingest.json()["status"] in {"ok", "db_unreachable"}

    meta = client.get("/metadata/ping").json()
    assert "metadata placeholder" not in meta.values()

    user_status = client.get("/users/ping").json()["status"]
    assert user_status in {"ok", "db_unreachable"}

    stream = client.get("/stream/ping", headers={"Authorization": f"Bearer {token}"})
    assert stream.json()["status"] in {"ok", "db_unreachable"}


def test_create_app_warns_on_default_jwt_secret(caplog, monkeypatch):
    monkeypatch.delenv("JWT_SECRET", raising=False)
    caplog.set_level(logging.CRITICAL, logger="server.config")

    create_app()

    messages = [record.getMessage() for record in caplog.records]
    assert any("default insecure value" in message for message in messages)


def test_create_app_skips_warning_with_custom_secret(caplog, monkeypatch):
    monkeypatch.setenv("JWT_SECRET", "super_secret_value")
    caplog.set_level(logging.CRITICAL, logger="server.config")

    create_app()

    messages = [record.getMessage() for record in caplog.records]
    assert all("default insecure value" not in message for message in messages)
