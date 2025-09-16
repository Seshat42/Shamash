"""FastAPI application for the Shamash media server."""

from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from pathlib import Path
from pydantic import BaseModel
import httpx
from sqlalchemy import text

from .integrations.radarr import refresh_movies, RADARR_URL
from .integrations.sonarr import refresh_series, SONARR_URL
from . import db

from .auth import auth_router, token_required, require_role, TokenClaims


# Placeholder routers for future modules
media_ingestion_router = APIRouter(prefix="/ingestion", tags=["ingestion"])
metadata_sync_router = APIRouter(prefix="/metadata", tags=["metadata"])
user_management_router = APIRouter(prefix="/users", tags=["users"])
streaming_router = APIRouter(prefix="/stream", tags=["stream"])
media_router = APIRouter(prefix="/media", tags=["media"])


async def _check_service(url: str) -> str:
    """Return ``"ok"`` if an HTTP HEAD succeeds, otherwise ``"unreachable"``."""
    try:
        async with httpx.AsyncClient(timeout=2) as client:
            await client.head(url)
        return "ok"
    except httpx.RequestError:
        return "unreachable"


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
    """Check connectivity with Sonarr, Radarr and the database."""
    sonarr_status = await _check_service(SONARR_URL)
    radarr_status = await _check_service(RADARR_URL)
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
    app = FastAPI(title="Shamash Media Server")

    app.include_router(media_ingestion_router)
    app.include_router(metadata_sync_router)
    app.include_router(user_management_router)
    app.include_router(media_router)
    app.include_router(streaming_router)
    app.include_router(auth_router)

    return app


app = create_app()
