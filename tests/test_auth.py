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
    token = create_token("carol")
    assert verify_token(token) == "carol"


def test_verify_token_rejects_expired(monkeypatch):
    monkeypatch.setattr(auth, "TOKEN_EXPIRE_SECONDS", -1)
    token = auth.create_token("dan")
    with pytest.raises(HTTPException) as exc_info:
        auth.verify_token(token)
    assert exc_info.value.status_code == status.HTTP_401_UNAUTHORIZED
