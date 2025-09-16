import bcrypt
import pytest
from server import db


def test_add_and_get_user(temp_db):
    user = db.add_user("alice", "password")
    retrieved = db.get_user("alice")
    assert retrieved.username == user.username
    assert db.get_password_hash("alice") == user.password_hash
    assert bcrypt.checkpw(b"password", retrieved.password_hash.encode())


def test_add_user_rolls_back_and_closes_on_failure(monkeypatch):
    sessions = []

    class FaultySession:
        def __init__(self):
            self.closed = False
            self.rollback_called = False

        def add(self, _obj):
            pass

        def commit(self):
            raise RuntimeError("boom")

        def refresh(self, _obj):
            pass

        def rollback(self):
            self.rollback_called = True

        def close(self):
            self.closed = True

    def fake_get_session():
        session = FaultySession()
        sessions.append(session)
        return session

    monkeypatch.setattr(db, "get_session", fake_get_session)

    with pytest.raises(RuntimeError):
        db.add_user("bob", "password")

    session = sessions[0]
    assert session.rollback_called
    assert session.closed


def test_get_user_closes_session_on_failure(monkeypatch):
    class ExplodingSession:
        def __init__(self):
            self.closed = False

        def scalar(self, _stmt):
            raise RuntimeError("boom")

        def close(self):
            self.closed = True

    session = ExplodingSession()

    monkeypatch.setattr(db, "get_session", lambda: session)

    with pytest.raises(RuntimeError):
        db.get_user("carol")

    assert session.closed
