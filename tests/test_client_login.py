import json
from pathlib import Path
import urllib.request

from client import main


class FakeResponse:
    def __init__(self, data: bytes):
        self._data = data
        self.status = 200

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False

    def read(self, *args, **kwargs):
        return self._data

    def readline(self, *args, **kwargs):
        return self._data


def test_login_saves_token(tmp_path, monkeypatch):
    responses = []

    def fake_urlopen(req, *args, **kwargs):
        body = json.loads(req.data.decode())
        assert body == {"username": "bob", "password": "secret"}
        responses.append(req.full_url)
        return FakeResponse(b'{"access_token": "testtoken"}')

    monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)
    monkeypatch.setattr(Path, "home", lambda: tmp_path)

    main.login_user("http://localhost:8000", "bob", "secret", save_token=True)

    token_file = tmp_path / ".shamash_token"
    assert token_file.exists()
    assert token_file.read_text(encoding="utf-8") == "testtoken"
    assert responses == ["http://localhost:8000/auth/login"]
