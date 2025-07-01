"""FastAPI application for the Shamash media server."""

from fastapi import FastAPI, APIRouter, Depends, HTTPException
from fastapi.responses import FileResponse, RedirectResponse
from pathlib import Path

from .integrations.radarr import refresh_movies
from .integrations.sonarr import refresh_series
from . import db

from .auth import auth_router, token_required


# Placeholder routers for future modules
media_ingestion_router = APIRouter(prefix="/ingestion", tags=["ingestion"])
metadata_sync_router = APIRouter(prefix="/metadata", tags=["metadata"])
user_management_router = APIRouter(prefix="/users", tags=["users"])
streaming_router = APIRouter(prefix="/stream", tags=["stream"])
media_router = APIRouter(prefix="/media", tags=["media"])


@media_ingestion_router.get("/ping")
async def ingestion_ping() -> dict[str, str]:
    """Check the media ingestion module."""
    return {"status": "ingestion placeholder"}


@metadata_sync_router.get("/ping")
async def metadata_ping() -> dict[str, str]:
    """Check the metadata sync module."""
    return {"status": "metadata placeholder"}


@metadata_sync_router.post("/sync")
async def metadata_sync() -> dict[str, str]:
    """Synchronize metadata with Sonarr and Radarr."""
    try:
        refresh_series()
        refresh_movies()
    except Exception as exc:  # Broad except keeps placeholder simple
        return {"status": f"failed: {exc}"}
    return {"status": "synchronized"}


@media_router.get("/")
async def list_media(_: str = Depends(token_required)) -> list[dict[str, str]]:
    """Return all available media items."""
    items = db.list_media_items()
    return [
        {"id": item.id, "title": item.title, "description": item.description}
        for item in items
    ]


@user_management_router.get("/ping")
async def users_ping() -> dict[str, str]:
    """Check the user management module."""
    return {"status": "users placeholder"}


@streaming_router.get("/ping")
async def stream_ping(_: str = Depends(token_required)) -> dict[str, str]:
    """Check the streaming module. Requires a valid token."""
    return {"status": "streaming placeholder"}


@streaming_router.get("/{item_id}")
async def stream_media(item_id: int, _: str = Depends(token_required)):
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
