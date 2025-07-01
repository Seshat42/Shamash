"""HTTP helpers for interacting with the Radarr API."""

from __future__ import annotations

import os

import httpx

RADARR_URL = os.environ.get("RADARR_URL", "http://localhost:7878")
RADARR_API_KEY = os.environ.get("RADARR_API_KEY", "")


def _headers() -> dict[str, str]:
    """Return headers required for Radarr requests."""
    if RADARR_API_KEY:
        return {"X-Api-Key": RADARR_API_KEY}
    return {}


def get_movies() -> list[dict]:
    """Retrieve all movies from Radarr."""
    url = f"{RADARR_URL}/api/v3/movie"
    response = httpx.get(url, headers=_headers(), timeout=10)
    response.raise_for_status()
    return response.json()


def refresh_movies() -> None:
    """Trigger a Radarr refresh command."""
    url = f"{RADARR_URL}/api/v3/command"
    payload = {"name": "RefreshMovie"}
    response = httpx.post(url, json=payload, headers=_headers(), timeout=10)
    response.raise_for_status()
