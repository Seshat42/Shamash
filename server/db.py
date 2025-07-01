"""SQLite and SQLAlchemy utilities for Shamash."""

from __future__ import annotations

import hashlib
import os
from pathlib import Path
from typing import Optional

from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session, sessionmaker

from .models import Base, User, MediaItem

DEFAULT_DB_PATH = Path(__file__).with_name("shamash.db")
DB_PATH = Path(os.environ.get("SHAMASH_DB_PATH", DEFAULT_DB_PATH))
DATABASE_URL = f"sqlite:///{DB_PATH}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

Base.metadata.create_all(bind=engine)


def get_session() -> Session:
    """Return a new database session."""
    return SessionLocal()


# User management CRUD -------------------------------------------------------

def add_user(username: str, password: str) -> User:
    """Create a new user with a hashed password."""
    session = get_session()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    user = User(username=username, password_hash=password_hash)
    session.add(user)
    session.commit()
    session.refresh(user)
    session.close()
    return user


def get_user(username: str) -> Optional[User]:
    """Retrieve a user by username."""
    session = get_session()
    stmt = select(User).where(User.username == username)
    user = session.scalar(stmt)
    session.close()
    return user


def update_user_password(username: str, password: str) -> bool:
    """Update a user's password hash."""
    session = get_session()
    user = session.scalar(select(User).where(User.username == username))
    if user is None:
        session.close()
        return False
    user.password_hash = hashlib.sha256(password.encode()).hexdigest()
    session.commit()
    session.close()
    return True


def delete_user(username: str) -> bool:
    """Delete a user from the database."""
    session = get_session()
    user = session.scalar(select(User).where(User.username == username))
    if user is None:
        session.close()
        return False
    session.delete(user)
    session.commit()
    session.close()
    return True


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
    item = MediaItem(title=title, path=path, description=description)
    session.add(item)
    session.commit()
    session.refresh(item)
    session.close()
    return item


def get_media_item(item_id: int) -> Optional[MediaItem]:
    """Fetch a media item by ID."""
    session = get_session()
    item = session.get(MediaItem, item_id)
    session.close()
    return item


def update_media_item(item_id: int, **fields: str) -> bool:
    """Update fields on a media item."""
    session = get_session()
    item = session.get(MediaItem, item_id)
    if item is None:
        session.close()
        return False
    for key, value in fields.items():
        setattr(item, key, value)
    session.commit()
    session.close()
    return True


def delete_media_item(item_id: int) -> bool:
    """Remove a media item from the database."""
    session = get_session()
    item = session.get(MediaItem, item_id)
    if item is None:
        session.close()
        return False
    session.delete(item)
    session.commit()
    session.close()
    return True
