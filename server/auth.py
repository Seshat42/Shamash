"""JWT authentication utilities and route definitions."""

from __future__ import annotations

import datetime
import os

from dataclasses import dataclass

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


@dataclass(frozen=True)
class TokenClaims:
    """Structured representation of token claims used for authorization."""

    username: str
    role: str


class LoginRequest(BaseModel):
    """Schema for login requests."""

    username: str
    password: str


def create_token(username: str, role: str) -> str:
    """Generate a JWT token for the specified user and role."""
    payload = {
        "sub": username,
        "role": role,
        "exp": datetime.datetime.now(datetime.UTC)
        + datetime.timedelta(seconds=TOKEN_EXPIRE_SECONDS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str) -> TokenClaims:
    """Verify a JWT token and return the embedded claims."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except jwt.PyJWTError as exc:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token") from exc
    username = payload.get("sub")
    role = payload.get("role")
    if username is None or role is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    return TokenClaims(username=username, role=role)


def token_required(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenClaims:
    """FastAPI dependency that validates a bearer token."""
    return verify_token(credentials.credentials)


def require_role(role: str):
    """Return a dependency that ensures the authenticated user has ``role``."""

    def checker(claims: TokenClaims = Depends(token_required)) -> str:
        if claims.role != role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return claims.username

    return checker


@auth_router.post("/login")
async def login(credentials: LoginRequest) -> dict[str, str]:
    """Authenticate user credentials and return a JWT token."""
    username = credentials.username
    password = credentials.password
    user = db.get_user(username)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    if not bcrypt.checkpw(password.encode(), user.password_hash.encode()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    token = create_token(user.username, user.role)
    return {"access_token": token}
