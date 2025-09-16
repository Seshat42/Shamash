import pytest
from fastapi import HTTPException, status
from fastapi.testclient import TestClient

from server import auth, db
from server.app import create_app


def test_login_success(temp_db):
    db.add_user("bob", "secret")
    app = create_app()
    client = TestClient(app)
    response = client.post("/auth/login", json={"username": "bob", "password": "secret"})
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_token_functions():
    from server.auth import create_token, verify_token
    token = create_token("carol", "admin")
    claims = verify_token(token)
    assert claims.username == "carol"
    assert claims.role == "admin"


def test_verify_token_rejects_expired(monkeypatch):
    monkeypatch.setattr(auth, "TOKEN_EXPIRE_SECONDS", -1)
    token = auth.create_token("dan", "user")
    with pytest.raises(HTTPException) as exc_info:
        auth.verify_token(token)
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED


def test_require_role_uses_token_claim(monkeypatch):
    token = auth.create_token("erin", "admin")

    def _fail_get_user(_: str):  # pragma: no cover - ensures database is not queried
        raise AssertionError("require_role should not query the database")

    monkeypatch.setattr(auth.db, "get_user", _fail_get_user)
    checker = auth.require_role("admin")
    claims = auth.verify_token(token)
    assert checker(claims) == "erin"


def test_require_role_rejects_mismatched_role():
    token = auth.create_token("frank", "user")
    checker = auth.require_role("admin")
    with pytest.raises(HTTPException) as exc_info:
        checker(auth.verify_token(token))
    assert exc_info.value.status_code == status.HTTP_403_FORBIDDEN
