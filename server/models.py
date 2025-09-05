"""SQLAlchemy models for Shamash."""

from __future__ import annotations

from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    """User account with hashed password."""

    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="user", nullable=False)


class MediaItem(Base):
    """Local or remote media item."""

    __tablename__ = "media_items"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    path = Column(Text, nullable=False)
    description = Column(Text, nullable=True)
