from fastapi.testclient import TestClient
import httpx
from server.app import create_app


def test_metadata_sync_handles_sonarr_error(monkeypatch):
    def fail_series():
        raise httpx.RequestError("boom")
    monkeypatch.setattr("server.app.refresh_series", fail_series)
    app = create_app()
    client = TestClient(app)
    resp = client.post("/metadata/sync")
    assert resp.json()["status"] == "sonarr_error"


def test_metadata_sync_handles_radarr_error(monkeypatch):
    def fail_series():
        pass
    def fail_movies():
        raise httpx.RequestError("nope")
    monkeypatch.setattr("server.app.refresh_series", fail_series)
    monkeypatch.setattr("server.app.refresh_movies", fail_movies)
    app = create_app()
    client = TestClient(app)
    resp = client.post("/metadata/sync")
    assert resp.json()["status"] == "radarr_error"
