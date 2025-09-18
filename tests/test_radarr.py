import httpx
import pytest

from server.integrations import radarr


def test_headers_include_api_key(monkeypatch):
    monkeypatch.setattr(radarr, "RADARR_API_KEY", "radarr-key")
    assert radarr._headers() == {"X-Api-Key": "radarr-key"}


def test_headers_omit_empty_key(monkeypatch):
    monkeypatch.setattr(radarr, "RADARR_API_KEY", "")
    assert radarr._headers() == {}


def test_get_movies_requests_expected_url_and_headers(monkeypatch):
    monkeypatch.setattr(radarr, "RADARR_URL", "http://radarr.test")
    monkeypatch.setattr(radarr, "RADARR_API_KEY", "test-key")

    call_log = {}

    class DummyResponse:
        def raise_for_status(self):
            call_log["raised"] = True

        def json(self):
            return [
                {"id": 42, "title": "Example"},
            ]

    def fake_get(url, *, headers=None, timeout=None):
        call_log["url"] = url
        call_log["headers"] = dict(headers or {})
        call_log["timeout"] = timeout
        return DummyResponse()

    monkeypatch.setattr(radarr.httpx, "get", fake_get)

    payload = radarr.get_movies()

    assert payload == [{"id": 42, "title": "Example"}]
    assert call_log["url"] == "http://radarr.test/api/v3/movie"
    assert call_log["headers"] == {"X-Api-Key": "test-key"}
    assert call_log["timeout"] == 10
    assert call_log["raised"] is True


def test_get_movies_propagates_request_error(monkeypatch):
    monkeypatch.setattr(radarr, "RADARR_URL", "http://radarr.test")
    monkeypatch.setattr(radarr, "RADARR_API_KEY", "")

    def fake_get(url, *, headers=None, timeout=None):
        assert url == "http://radarr.test/api/v3/movie"
        assert headers == {}
        assert timeout == 10
        raise httpx.RequestError("boom", request=httpx.Request("GET", url))

    monkeypatch.setattr(radarr.httpx, "get", fake_get)

    with pytest.raises(httpx.RequestError):
        radarr.get_movies()


def test_refresh_movies_posts_expected_payload(monkeypatch):
    monkeypatch.setattr(radarr, "RADARR_URL", "http://radarr.test")
    monkeypatch.setattr(radarr, "RADARR_API_KEY", "refresh-key")

    call_log = {}

    class DummyResponse:
        def raise_for_status(self):
            call_log["raised"] = True

    def fake_post(url, *, json=None, headers=None, timeout=None):
        call_log["url"] = url
        call_log["json"] = dict(json or {})
        call_log["headers"] = dict(headers or {})
        call_log["timeout"] = timeout
        return DummyResponse()

    monkeypatch.setattr(radarr.httpx, "post", fake_post)

    radarr.refresh_movies()

    assert call_log["url"] == "http://radarr.test/api/v3/command"
    assert call_log["json"] == {"name": "RefreshMovie"}
    assert call_log["headers"] == {"X-Api-Key": "refresh-key"}
    assert call_log["timeout"] == 10
    assert call_log["raised"] is True


def test_refresh_movies_propagates_request_error(monkeypatch):
    monkeypatch.setattr(radarr, "RADARR_URL", "http://radarr.test")
    monkeypatch.setattr(radarr, "RADARR_API_KEY", "")

    def fake_post(url, *, json=None, headers=None, timeout=None):
        assert url == "http://radarr.test/api/v3/command"
        assert json == {"name": "RefreshMovie"}
        assert headers == {}
        assert timeout == 10
        raise httpx.RequestError("nope", request=httpx.Request("POST", url))

    monkeypatch.setattr(radarr.httpx, "post", fake_post)

    with pytest.raises(httpx.RequestError):
        radarr.refresh_movies()


@pytest.mark.anyio
@pytest.mark.parametrize("anyio_backend", ["asyncio"], indirect=True)
async def test_async_refresh_movies_uses_async_client(monkeypatch):
    monkeypatch.setattr(radarr, "RADARR_URL", "http://radarr.test")
    monkeypatch.setattr(radarr, "RADARR_API_KEY", "async-key")

    call_log: dict[str, object] = {}

    class DummyAsyncClient:
        def __init__(self, *args, **kwargs):
            call_log["client_args"] = args
            call_log["client_kwargs"] = kwargs

        async def __aenter__(self):
            call_log["entered"] = True
            return self

        async def __aexit__(self, exc_type, exc, tb):
            call_log["exited"] = True
            return False

        async def post(self, url, *, json=None, headers=None, timeout=None):
            call_log["url"] = url
            call_log["json"] = dict(json or {})
            call_log["headers"] = dict(headers or {})
            call_log["timeout"] = timeout

            class DummyResponse:
                def raise_for_status(self):
                    call_log["raised"] = True

            return DummyResponse()

    monkeypatch.setattr(radarr.httpx, "AsyncClient", DummyAsyncClient)

    await radarr.async_refresh_movies()

    assert call_log["url"] == "http://radarr.test/api/v3/command"
    assert call_log["json"] == {"name": "RefreshMovie"}
    assert call_log["headers"] == {"X-Api-Key": "async-key"}
    assert call_log["timeout"] == 10
    assert call_log["entered"] is True
    assert call_log["exited"] is True
    assert call_log["raised"] is True


@pytest.mark.anyio
@pytest.mark.parametrize("anyio_backend", ["asyncio"], indirect=True)
async def test_async_refresh_movies_propagates_request_error(monkeypatch):
    monkeypatch.setattr(radarr, "RADARR_URL", "http://radarr.test")
    monkeypatch.setattr(radarr, "RADARR_API_KEY", "")

    class DummyAsyncClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def post(self, url, *, json=None, headers=None, timeout=None):
            assert url == "http://radarr.test/api/v3/command"
            assert json == {"name": "RefreshMovie"}
            assert headers == {}
            assert timeout == 10
            raise httpx.RequestError("boom", request=httpx.Request("POST", url))

    monkeypatch.setattr(radarr.httpx, "AsyncClient", DummyAsyncClient)

    with pytest.raises(httpx.RequestError):
        await radarr.async_refresh_movies()
