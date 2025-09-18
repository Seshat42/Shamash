import asyncio

import anyio
import httpx
import pytest
from fastapi.testclient import TestClient

from server import db
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


def _login(client: TestClient, username: str, password: str) -> dict[str, str]:
    response = client.post(
        "/auth/login", json={"username": username, "password": password}
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def _create_authenticated_client(
    username: str = "admin", role: str = "admin"
) -> tuple[TestClient, dict[str, str]]:
    db.add_user(username, "pw", role=role)
    app = create_app()
    client = TestClient(app)
    headers = _login(client, username, "pw")
    return client, headers


def test_metadata_sync_handles_sonarr_error(monkeypatch):
    async def fail_series():
        raise httpx.RequestError("boom")

    monkeypatch.setattr("server.app.async_refresh_series", fail_series)
    client, admin_headers = _create_authenticated_client()
    resp = client.post("/metadata/sync", headers=admin_headers)
    assert resp.json()["status"] == "sonarr_error"


def test_metadata_sync_handles_radarr_error(monkeypatch):
    async def succeed_series():
        return None

    async def fail_movies():
        raise httpx.RequestError("nope")

    monkeypatch.setattr("server.app.async_refresh_series", succeed_series)
    monkeypatch.setattr("server.app.async_refresh_movies", fail_movies)
    client, admin_headers = _create_authenticated_client()
    resp = client.post("/metadata/sync", headers=admin_headers)
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

    client, admin_headers = _create_authenticated_client()
    resp = client.get("/metadata/ping", headers=admin_headers)
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

    client, admin_headers = _create_authenticated_client()
    resp = client.get("/metadata/ping", headers=admin_headers)
    payload = resp.json()

    assert payload["sonarr"] == "ok"
    assert payload["radarr"] == "auth_failed"
    assert payload["database"] == "ok"
    assert header_log["http://sonarr.test"].get("X-Api-Key") == "valid-sonarr-key"
    assert header_log["http://radarr.test"].get("X-Api-Key") == "bad-radarr-key"


def test_metadata_sync_requires_admin_token():
    app = create_app()
    client = TestClient(app)

    missing_token = client.post("/metadata/sync")
    assert missing_token.status_code == 403

    invalid_token = client.post(
        "/metadata/sync", headers={"Authorization": "Bearer invalid"}
    )
    assert invalid_token.status_code == 401


def test_metadata_sync_rejects_non_admin_role():
    client, user_headers = _create_authenticated_client("user", role="user")

    response = client.post("/metadata/sync", headers=user_headers)
    assert response.status_code == 403


def test_metadata_ping_requires_admin_token():
    app = create_app()
    client = TestClient(app)

    missing_token = client.get("/metadata/ping")
    assert missing_token.status_code == 403

    invalid_token = client.get(
        "/metadata/ping", headers={"Authorization": "Bearer invalid"}
    )
    assert invalid_token.status_code == 401


@pytest.mark.anyio
@pytest.mark.parametrize("anyio_backend", ["asyncio"], indirect=True)
async def test_metadata_sync_allows_concurrent_ping(monkeypatch):
    start_event = anyio.Event()
    finish_event = anyio.Event()
    order: list[str] = []

    async def slow_series() -> None:
        start_event.set()
        await finish_event.wait()

    async def quick_movies() -> None:
        order.append("movies_called")

    monkeypatch.setattr("server.app.async_refresh_series", slow_series)
    monkeypatch.setattr("server.app.async_refresh_movies", quick_movies)

    db.add_user("admin", "pw", role="admin")
    app = create_app()

    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(
        transport=transport, base_url="http://testserver"
    ) as client:
        login = await client.post(
            "/auth/login", json={"username": "admin", "password": "pw"}
        )
        assert login.status_code == 200
        token = login.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        async def call_sync():
            response = await client.post("/metadata/sync", headers=headers)
            order.append("sync_complete")
            return response

        async def call_ping():
            await start_event.wait()
            response = await client.get("/users/ping")
            order.append("ping_complete")
            finish_event.set()
            return response

        with anyio.fail_after(1):
            sync_response, ping_response = await asyncio.gather(
                call_sync(), call_ping()
            )

    assert ping_response.status_code == 200
    assert sync_response.json()["status"] == "synchronized"
    assert order[0] == "ping_complete"
    assert order[-1] == "sync_complete"
