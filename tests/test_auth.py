from fastapi.testclient import TestClient
from server.app import create_app
from server import db


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
