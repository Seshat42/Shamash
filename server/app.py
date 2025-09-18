"""FastAPI application for the Shamash media server."""

import asyncio
from pathlib import Path
from urllib.parse import urlparse

import httpx
from fastapi import APIRouter, Depends, FastAPI, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from pydantic import BaseModel, field_validator
from sqlalchemy import text

from . import db
from .auth import TokenClaims, auth_router, require_role, token_required
from .config import resolve_jwt_secret, warn_if_default_jwt_secret
from .integrations.radarr import RADARR_API_KEY, RADARR_URL, refresh_movies
from .integrations.sonarr import SONARR_API_KEY, SONARR_URL, refresh_series


# Placeholder routers for future modules
media_ingestion_router = APIRouter(
    prefix="/ingestion",
    tags=["ingestion"],
    dependencies=[Depends(require_role("admin"))],
)
metadata_sync_router = APIRouter(prefix="/metadata", tags=["metadata"])
user_management_router = APIRouter(prefix="/users", tags=["users"])
streaming_router = APIRouter(prefix="/stream", tags=["stream"])
media_router = APIRouter(prefix="/media", tags=["media"])


async def _check_service(base_url: str, api_key: str | None) -> str:
    """Probe an external service and return its health status string.

    A service is considered ``"ok"`` when the authenticated status endpoint
    responds successfully. If the request fails due to missing or invalid API
    credentials the function returns ``"auth_failed"``. Network errors and
    timeouts are reported as ``"unreachable"`` and any other HTTP response code
    is mapped to ``"error"``.
    """

    status_url = f"{base_url.rstrip('/')}/api/v3/system/status"
    headers = {"X-Api-Key": api_key} if api_key else {}
    try:
        async with httpx.AsyncClient(timeout=2) as client:
            response = await client.get(status_url, headers=headers)
    except httpx.RequestError:
        return "unreachable"

    if response.status_code in {401, 403}:
        return "auth_failed"
    if response.is_success:
        return "ok"
    return "error"


def _check_database() -> str:
    """Return ``"ok"`` if the database responds to a simple query."""
    try:
        session = db.get_session()
        session.execute(text("SELECT 1"))
        session.close()
        return "ok"
    except Exception:
        return "db_unreachable"


@media_ingestion_router.get("/ping")
async def ingestion_ping() -> dict[str, str]:
    """Check database connectivity for media ingestion."""
    return {"status": _check_database()}


class IngestionRequest(BaseModel):
    """Payload for creating a media item."""

    title: str
    path: str
    description: str | None = None

    @field_validator("path")
    def validate_path(cls, value: str) -> str:
        """Ensure the path is an HTTP(S) URL or an existing local file."""

        cleaned = value.strip()
        if not cleaned:
            raise ValueError("path must not be empty")

        parsed = urlparse(cleaned)
        scheme = parsed.scheme.lower()
        if scheme in {"http", "https"}:
            if parsed.netloc:
                return cleaned
            raise ValueError(
                "path must include a network location when using http or https URLs"
            )
        if scheme:
            raise ValueError(
                "path must be an http or https URL or an existing local file"
            )

        candidate = Path(cleaned)
        if ".." in candidate.parts:
            raise ValueError("local paths may not contain directory traversal segments")

        try:
            resolved = candidate.expanduser().resolve(strict=True)
        except FileNotFoundError as exc:
            raise ValueError("local path must reference an existing file") from exc
        except OSError as exc:  # pragma: no cover - unexpected resolution failure
            raise ValueError("local path could not be resolved") from exc

        if not resolved.is_file():
            raise ValueError("local path must reference a file")

        return str(resolved)


@media_ingestion_router.post("/")
async def ingest_media(item: IngestionRequest) -> dict[str, int | str | None]:
    """Create a new media item entry."""
    created = db.create_media_item(item.title, item.path, item.description)
    return {
        "id": created.id,
        "title": created.title,
        "description": created.description,
    }


@metadata_sync_router.get("/ping")
async def metadata_ping() -> dict[str, str]:
    """Check connectivity and authentication with Sonarr, Radarr, and the database."""

    sonarr_status, radarr_status = await asyncio.gather(
        _check_service(SONARR_URL, SONARR_API_KEY),
        _check_service(RADARR_URL, RADARR_API_KEY),
    )
    return {
        "sonarr": sonarr_status,
        "radarr": radarr_status,
        "database": _check_database(),
    }


@metadata_sync_router.post("/sync")
async def metadata_sync() -> dict[str, str]:
    """Synchronize metadata with Sonarr and Radarr."""
    try:
        refresh_series()
    except httpx.RequestError as exc:
        return {"status": "sonarr_error", "detail": str(exc)}
    try:
        refresh_movies()
    except httpx.RequestError as exc:
        return {"status": "radarr_error", "detail": str(exc)}
    except Exception as exc:  # pragma: no cover - catch unexpected errors
        return {"status": f"failed: {exc}"}
    return {"status": "synchronized"}


@media_router.get("/")
async def list_media(_: TokenClaims = Depends(token_required)) -> list[dict]:
    """Return all available media items."""
    items = db.list_media_items()
    return [
        {"id": item.id, "title": item.title, "description": item.description}
        for item in items
    ]


@user_management_router.get("/ping")
async def users_ping() -> dict[str, str]:
    """Check database connectivity for user management."""
    return {"status": _check_database()}


class UserCreateRequest(BaseModel):
    """Payload for creating a user."""

    username: str
    password: str
    role: str = "user"


class PasswordUpdateRequest(BaseModel):
    """Payload for updating a user's password."""

    password: str


@user_management_router.post("/")
async def create_user(
    request: UserCreateRequest, _: str = Depends(require_role("admin"))
) -> dict[str, str | int]:
    """Create a new user account."""
    user = db.add_user(request.username, request.password, request.role)
    return {"id": user.id, "username": user.username, "role": user.role}


@user_management_router.get("/{username}")
async def get_user(
    username: str, _: str = Depends(require_role("admin"))
) -> dict[str, str | int]:
    """Retrieve information about a user."""
    user = db.get_user(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return {"id": user.id, "username": user.username, "role": user.role}


@user_management_router.put("/{username}")
async def update_user(
    username: str,
    request: PasswordUpdateRequest,
    _: str = Depends(require_role("admin")),
) -> dict[str, str]:
    """Update a user's password."""
    success = db.update_user_password(username, request.password)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "updated"}


@user_management_router.delete("/{username}")
async def delete_user(
    username: str, _: str = Depends(require_role("admin"))
) -> dict[str, str]:
    """Remove a user account."""
    success = db.delete_user(username)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"status": "deleted"}


@streaming_router.get("/ping")
async def stream_ping(_: TokenClaims = Depends(token_required)) -> dict[str, str]:
    """Check database connectivity for streaming. Requires a valid token."""
    return {"status": _check_database()}


@streaming_router.get("/{item_id}")
async def stream_media(item_id: int, _: TokenClaims = Depends(token_required)):
    """Stream a media file or redirect to a remote URL."""
    item = db.get_media_item(item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Media not found")
    if item.path.startswith("http://") or item.path.startswith("https://"):
        return RedirectResponse(item.path)
    file_path = Path(item.path)
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(file_path, media_type="application/octet-stream")


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    warn_if_default_jwt_secret(resolve_jwt_secret())

    app = FastAPI(title="Shamash Media Server")

    app.include_router(media_ingestion_router)
    app.include_router(metadata_sync_router)
    app.include_router(user_management_router)
    app.include_router(media_router)
    app.include_router(streaming_router)
    app.include_router(auth_router)

    return app


app = create_app()
