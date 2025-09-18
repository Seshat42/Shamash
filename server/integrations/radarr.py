"""HTTP helpers for interacting with the Radarr API."""

from __future__ import annotations

import logging
import os

import httpx
from httpx import RequestError

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
    try:
        response = httpx.get(url, headers=_headers(), timeout=10)
        response.raise_for_status()
    except RequestError as exc:
        logging.getLogger(__name__).error("Radarr request failed: %s", exc)
        raise
    return response.json()


def refresh_movies() -> None:
    """Trigger a Radarr refresh command."""
    url = f"{RADARR_URL}/api/v3/command"
    payload = {"name": "RefreshMovie"}
    try:
        response = httpx.post(url, json=payload, headers=_headers(), timeout=10)
        response.raise_for_status()
    except RequestError as exc:
        logging.getLogger(__name__).error("Radarr request failed: %s", exc)
        raise


async def async_refresh_movies(
    client: httpx.AsyncClient | None = None,
) -> None:
    """Trigger a Radarr refresh command without blocking the event loop."""

    url = f"{RADARR_URL}/api/v3/command"
    payload = {"name": "RefreshMovie"}
    headers = _headers()

    try:
        if client is None:
            async with httpx.AsyncClient() as async_client:
                response = await async_client.post(
                    url, json=payload, headers=headers, timeout=10
                )
        else:
            response = await client.post(
                url, json=payload, headers=headers, timeout=10
            )
        response.raise_for_status()
    except RequestError as exc:
        logging.getLogger(__name__).error("Radarr request failed: %s", exc)
        raise
