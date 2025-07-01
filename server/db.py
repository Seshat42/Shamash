"""Simple SQLite utilities for user authentication."""

from __future__ import annotations

import hashlib
import sqlite3
from pathlib import Path
from typing import Optional


DB_PATH = Path(__file__).with_name("shamash.db")


def get_connection() -> sqlite3.Connection:
    """Return a connection to the SQLite database."""
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password_hash TEXT)"
    )
    return conn


def add_user(username: str, password: str) -> None:
    """Insert a new user with a hashed password."""
    conn = get_connection()
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    with conn:
        conn.execute(
            "INSERT OR REPLACE INTO users (username, password_hash) VALUES (?, ?)",
            (username, password_hash),
        )


def get_password_hash(username: str) -> Optional[str]:
    """Retrieve the password hash for a username if it exists."""
    conn = get_connection()
    cur = conn.execute(
        "SELECT password_hash FROM users WHERE username = ?", (username,)
    )
    row = cur.fetchone()
    return row[0] if row else None
