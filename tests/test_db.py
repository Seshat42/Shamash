import bcrypt
from server import db


def test_add_and_get_user(temp_db):
    user = db.add_user("alice", "password")
    retrieved = db.get_user("alice")
    assert retrieved.username == user.username
    assert db.get_password_hash("alice") == user.password_hash
    assert bcrypt.checkpw(b"password", retrieved.password_hash.encode())
