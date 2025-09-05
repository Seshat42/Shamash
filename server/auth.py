"""JWT authentication utilities and route definitions."""

from __future__ import annotations

import datetime
import os

import bcrypt
import jwt
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

from . import db
from .config import CONFIG


SECRET_KEY = os.environ.get(
    "JWT_SECRET", CONFIG.get("server", {}).get("jwt_secret", "change_this_secret")
)
ALGORITHM = "HS256"
TOKEN_EXPIRE_SECONDS = 3600


security = HTTPBearer()

auth_router = APIRouter(prefix="/auth", tags=["auth"])


class LoginRequest(BaseModel):
    """Schema for login requests."""

    username: str
    password: str


def create_token(username: str) -> str:
    """Generate a JWT token for the specified user."""
    payload = {
        "sub": username,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=TOKEN_EXPIRE_SECONDS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> str:
    """Verify a JWT token and return the username."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc
    username = payload.get("sub")
    if username is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    return username


def token_required(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    """FastAPI dependency that validates a bearer token."""
    return verify_token(credentials.credentials)


def require_role(role: str):
    """Return a dependency that ensures the authenticated user has ``role``."""

    def checker(username: str = Depends(token_required)) -> str:
        user = db.get_user(username)
        if user is None or user.role != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return username

    return checker


@auth_router.post("/login")
async def login(credentials: LoginRequest) -> dict[str, str]:
    """Authenticate user credentials and return a JWT token."""
    username = credentials.username
    password = credentials.password
    stored_hash = db.get_password_hash(username)
    if stored_hash is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not bcrypt.checkpw(password.encode(), stored_hash.encode()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_token(username)
    return {"access_token": token}
