import httpx
import pytest

from server.integrations import sonarr


def test_headers_include_api_key(monkeypatch):
    monkeypatch.setattr(sonarr, "SONARR_API_KEY", "sonarr-key")
    assert sonarr._headers() == {"X-Api-Key": "sonarr-key"}


def test_headers_omit_empty_key(monkeypatch):
    monkeypatch.setattr(sonarr, "SONARR_API_KEY", "")
    assert sonarr._headers() == {}


def test_get_series_requests_expected_url_and_headers(monkeypatch):
    monkeypatch.setattr(sonarr, "SONARR_URL", "http://sonarr.test")
    monkeypatch.setattr(sonarr, "SONARR_API_KEY", "test-key")

    call_log = {}

    class DummyResponse:
        def raise_for_status(self):
            call_log["raised"] = True

        def json(self):
            return [
                {"id": 7, "title": "Example Series"},
            ]

    def fake_get(url, *, headers=None, timeout=None):
        call_log["url"] = url
        call_log["headers"] = dict(headers or {})
        call_log["timeout"] = timeout
        return DummyResponse()

    monkeypatch.setattr(sonarr.httpx, "get", fake_get)

    payload = sonarr.get_series()

    assert payload == [{"id": 7, "title": "Example Series"}]
    assert call_log["url"] == "http://sonarr.test/api/v3/series"
    assert call_log["headers"] == {"X-Api-Key": "test-key"}
    assert call_log["timeout"] == 10
    assert call_log["raised"] is True


def test_get_series_propagates_request_error(monkeypatch):
    monkeypatch.setattr(sonarr, "SONARR_URL", "http://sonarr.test")
    monkeypatch.setattr(sonarr, "SONARR_API_KEY", "")

    def fake_get(url, *, headers=None, timeout=None):
        assert url == "http://sonarr.test/api/v3/series"
        assert headers == {}
        assert timeout == 10
        raise httpx.RequestError("boom", request=httpx.Request("GET", url))

    monkeypatch.setattr(sonarr.httpx, "get", fake_get)

    with pytest.raises(httpx.RequestError):
        sonarr.get_series()


def test_refresh_series_posts_expected_payload(monkeypatch):
    monkeypatch.setattr(sonarr, "SONARR_URL", "http://sonarr.test")
    monkeypatch.setattr(sonarr, "SONARR_API_KEY", "refresh-key")

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

    monkeypatch.setattr(sonarr.httpx, "post", fake_post)

    sonarr.refresh_series()

    assert call_log["url"] == "http://sonarr.test/api/v3/command"
    assert call_log["json"] == {"name": "RefreshSeries"}
    assert call_log["headers"] == {"X-Api-Key": "refresh-key"}
    assert call_log["timeout"] == 10
    assert call_log["raised"] is True


def test_refresh_series_propagates_request_error(monkeypatch):
    monkeypatch.setattr(sonarr, "SONARR_URL", "http://sonarr.test")
    monkeypatch.setattr(sonarr, "SONARR_API_KEY", "")

    def fake_post(url, *, json=None, headers=None, timeout=None):
        assert url == "http://sonarr.test/api/v3/command"
        assert json == {"name": "RefreshSeries"}
        assert headers == {}
        assert timeout == 10
        raise httpx.RequestError("nope", request=httpx.Request("POST", url))

    monkeypatch.setattr(sonarr.httpx, "post", fake_post)

    with pytest.raises(httpx.RequestError):
        sonarr.refresh_series()


@pytest.mark.anyio
@pytest.mark.parametrize("anyio_backend", ["asyncio"], indirect=True)
async def test_async_refresh_series_uses_async_client(monkeypatch):
    monkeypatch.setattr(sonarr, "SONARR_URL", "http://sonarr.test")
    monkeypatch.setattr(sonarr, "SONARR_API_KEY", "async-key")

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

    monkeypatch.setattr(sonarr.httpx, "AsyncClient", DummyAsyncClient)

    await sonarr.async_refresh_series()

    assert call_log["url"] == "http://sonarr.test/api/v3/command"
    assert call_log["json"] == {"name": "RefreshSeries"}
    assert call_log["headers"] == {"X-Api-Key": "async-key"}
    assert call_log["timeout"] == 10
    assert call_log["entered"] is True
    assert call_log["exited"] is True
    assert call_log["raised"] is True


@pytest.mark.anyio
@pytest.mark.parametrize("anyio_backend", ["asyncio"], indirect=True)
async def test_async_refresh_series_propagates_request_error(monkeypatch):
    monkeypatch.setattr(sonarr, "SONARR_URL", "http://sonarr.test")
    monkeypatch.setattr(sonarr, "SONARR_API_KEY", "")

    class DummyAsyncClient:
        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type, exc, tb):
            return False

        async def post(self, url, *, json=None, headers=None, timeout=None):
            assert url == "http://sonarr.test/api/v3/command"
            assert json == {"name": "RefreshSeries"}
            assert headers == {}
            assert timeout == 10
            raise httpx.RequestError("boom", request=httpx.Request("POST", url))

    monkeypatch.setattr(sonarr.httpx, "AsyncClient", DummyAsyncClient)

    with pytest.raises(httpx.RequestError):
        await sonarr.async_refresh_series()
