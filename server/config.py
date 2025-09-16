"""Configuration loader for Shamash server."""

from __future__ import annotations

import logging
import os
from pathlib import Path
from typing import Any, Dict

import yaml

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "default.yaml"
DEFAULT_JWT_SECRET = "change_this_secret"
JWT_SECRET_ENV_VAR = "JWT_SECRET"

LOGGER = logging.getLogger(__name__)


def load_config(path: Path = DEFAULT_CONFIG_PATH) -> Dict[str, Any]:
    """Load the YAML configuration file."""
    with path.open("r", encoding="utf-8") as cfg:
        return yaml.safe_load(cfg)


CONFIG: Dict[str, Any] = load_config()


def resolve_jwt_secret() -> str:
    """Return the effective JWT secret considering environment overrides."""

    env_secret = os.environ.get(JWT_SECRET_ENV_VAR)
    if env_secret:
        return env_secret
    server_config = CONFIG.get("server", {})
    return server_config.get("jwt_secret", DEFAULT_JWT_SECRET)


def warn_if_default_jwt_secret(secret: str) -> None:
    """Emit a critical warning when the secret matches the shipped default."""

    if secret == DEFAULT_JWT_SECRET:
        LOGGER.critical(
            "JWT secret is using the default insecure value. Set the %s environment "
            "variable or update config/default.yaml to protect production deployments.",
            JWT_SECRET_ENV_VAR,
        )
