from fastapi.testclient import TestClient
from server.app import create_app
from server import db
from server.auth import create_token


def test_media_list_endpoint(temp_db, tmp_path):
    db.create_media_item("demo", str(tmp_path / "demo.mp4"))
    db.add_user("alice", "pw")
    app = create_app()
    client = TestClient(app)
    token = create_token("alice", "user")
    response = client.get("/media/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["title"] == "demo"


def test_stream_endpoint_serves_file(temp_db, tmp_path):
    media_file = tmp_path / "sample.txt"
    media_file.write_text("hello")
    item = db.create_media_item("sample", str(media_file))
    db.add_user("bob", "pw")
    app = create_app()
    client = TestClient(app)
    token = create_token("bob", "user")
    response = client.get(
        f"/stream/{item.id}", headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    assert response.content == b"hello"
