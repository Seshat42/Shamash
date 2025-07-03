"""HTTP helpers for interacting with the Sonarr API."""

from __future__ import annotations

import logging
import os

import httpx
from httpx import RequestError

SONARR_URL = os.environ.get("SONARR_URL", "http://localhost:8989")
SONARR_API_KEY = os.environ.get("SONARR_API_KEY", "")


def _headers() -> dict[str, str]:
    """Return headers required for Sonarr requests."""
    if SONARR_API_KEY:
        return {"X-Api-Key": SONARR_API_KEY}
    return {}


def get_series() -> list[dict]:
    """Retrieve all series from Sonarr."""
    url = f"{SONARR_URL}/api/v3/series"
    try:
        response = httpx.get(url, headers=_headers(), timeout=10)
        response.raise_for_status()
    except RequestError as exc:
        logging.getLogger(__name__).error("Sonarr request failed: %s", exc)
        raise
    return response.json()


def refresh_series() -> None:
    """Trigger a Sonarr refresh command."""
    url = f"{SONARR_URL}/api/v3/command"
    payload = {"name": "RefreshSeries"}
    try:
        response = httpx.post(url, json=payload, headers=_headers(), timeout=10)
        response.raise_for_status()
    except RequestError as exc:
        logging.getLogger(__name__).error("Sonarr request failed: %s", exc)
        raise
