"""SQLite and SQLAlchemy utilities for Shamash."""

from __future__ import annotations

import bcrypt
import os
from pathlib import Path
from typing import Optional

from .config import CONFIG

from sqlalchemy import create_engine, select, text
from sqlalchemy.orm import Session, sessionmaker

from .models import Base, User, MediaItem

DEFAULT_DB_PATH = Path(
    CONFIG.get("server", {}).get("database", Path(__file__).with_name("shamash.db"))
)
DB_PATH = Path(os.environ.get("SHAMASH_DB_PATH", DEFAULT_DB_PATH))
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base.metadata.create_all(bind=engine)

# Migration: ensure the `role` column exists on the users table
with engine.begin() as conn:  # pragma: no cover - executed at import time
    existing = [row[1] for row in conn.execute(text("PRAGMA table_info(users)"))]
    if "role" not in existing:
        conn.execute(
            text("ALTER TABLE users ADD COLUMN role STRING NOT NULL DEFAULT 'user'")
        )


def get_session() -> Session:
    """Return a new database session."""
    return SessionLocal()


# User management CRUD -------------------------------------------------------


def add_user(username: str, password: str, role: str = "user") -> User:
    """Create a new user with a hashed password and role."""
    session = get_session()
    try:
        password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        user = User(username=username, password_hash=password_hash, role=role)
        session.add(user)
        session.commit()
        session.refresh(user)
        return user
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_user(username: str) -> Optional[User]:
    """Retrieve a user by username."""
    session = get_session()
    try:
        stmt = select(User).where(User.username == username)
        return session.scalar(stmt)
    finally:
        session.close()


def update_user_password(username: str, password: str) -> bool:
    """Update a user's password hash."""
    session = get_session()
    try:
        user = session.scalar(select(User).where(User.username == username))
        if user is None:
            return False
        user.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        session.commit()
        return True
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def delete_user(username: str) -> bool:
    """Delete a user from the database."""
    session = get_session()
    try:
        user = session.scalar(select(User).where(User.username == username))
        if user is None:
            return False
        session.delete(user)
        session.commit()
        return True
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_password_hash(username: str) -> Optional[str]:
    """Retrieve the stored password hash for a user."""
    user = get_user(username)
    return user.password_hash if user else None


# Media ingestion CRUD -------------------------------------------------------


def create_media_item(
    title: str, path: str, description: str | None = None
) -> MediaItem:
    """Insert a new media item."""
    session = get_session()
    try:
        item = MediaItem(title=title, path=path, description=description)
        session.add(item)
        session.commit()
        session.refresh(item)
        return item
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_media_item(item_id: int) -> Optional[MediaItem]:
    """Fetch a media item by ID."""
    session = get_session()
    try:
        return session.get(MediaItem, item_id)
    finally:
        session.close()


def list_media_items() -> list[MediaItem]:
    """Return all media items."""
    session = get_session()
    try:
        items = session.scalars(select(MediaItem)).all()
        return list(items)
    finally:
        session.close()


def update_media_item(item_id: int, **fields: str) -> bool:
    """Update fields on a media item."""
    session = get_session()
    try:
        item = session.get(MediaItem, item_id)
        if item is None:
            return False
        for key, value in fields.items():
            setattr(item, key, value)
        session.commit()
        return True
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def delete_media_item(item_id: int) -> bool:
    """Remove a media item from the database."""
    session = get_session()
    try:
        item = session.get(MediaItem, item_id)
        if item is None:
            return False
        session.delete(item)
        session.commit()
        return True
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
