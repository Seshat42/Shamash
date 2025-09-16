from fastapi.testclient import TestClient
import httpx

from server.app import create_app


def _stub_metadata_client(monkeypatch, status_by_host, header_log):
    class DummyAsyncClient:
        def __init__(self, *args, **kwargs):
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def get(self, url, headers=None):
            for host, status in status_by_host.items():
                if host in url:
                    header_log[host] = dict(headers or {})
                    return httpx.Response(
                        status_code=status,
                        request=httpx.Request("GET", url),
                    )
            raise AssertionError(f"Unexpected metadata URL: {url}")

    monkeypatch.setattr("server.app.httpx.AsyncClient", DummyAsyncClient)


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


def test_metadata_ping_reports_invalid_sonarr_key(monkeypatch):
    monkeypatch.setattr("server.app.SONARR_URL", "http://sonarr.test")
    monkeypatch.setattr("server.app.RADARR_URL", "http://radarr.test")
    monkeypatch.setattr("server.app.SONARR_API_KEY", "bad-sonarr-key")
    monkeypatch.setattr("server.app.RADARR_API_KEY", "valid-radarr-key")
    monkeypatch.setattr("server.app._check_database", lambda: "ok")

    header_log: dict[str, dict[str, str]] = {}
    _stub_metadata_client(
        monkeypatch,
        {"http://sonarr.test": 401, "http://radarr.test": 200},
        header_log,
    )

    app = create_app()
    client = TestClient(app)
    resp = client.get("/metadata/ping")
    payload = resp.json()

    assert payload["sonarr"] == "auth_failed"
    assert payload["radarr"] == "ok"
    assert payload["database"] == "ok"
    assert header_log["http://sonarr.test"].get("X-Api-Key") == "bad-sonarr-key"
    assert header_log["http://radarr.test"].get("X-Api-Key") == "valid-radarr-key"


def test_metadata_ping_reports_invalid_radarr_key(monkeypatch):
    monkeypatch.setattr("server.app.SONARR_URL", "http://sonarr.test")
    monkeypatch.setattr("server.app.RADARR_URL", "http://radarr.test")
    monkeypatch.setattr("server.app.SONARR_API_KEY", "valid-sonarr-key")
    monkeypatch.setattr("server.app.RADARR_API_KEY", "bad-radarr-key")
    monkeypatch.setattr("server.app._check_database", lambda: "ok")

    header_log: dict[str, dict[str, str]] = {}
    _stub_metadata_client(
        monkeypatch,
        {"http://sonarr.test": 200, "http://radarr.test": 403},
        header_log,
    )

    app = create_app()
    client = TestClient(app)
    resp = client.get("/metadata/ping")
    payload = resp.json()

    assert payload["sonarr"] == "ok"
    assert payload["radarr"] == "auth_failed"
    assert payload["database"] == "ok"
    assert header_log["http://sonarr.test"].get("X-Api-Key") == "valid-sonarr-key"
    assert header_log["http://radarr.test"].get("X-Api-Key") == "bad-radarr-key"
