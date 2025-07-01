"""Configuration loader for Shamash server."""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

import yaml

DEFAULT_CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "default.yaml"


def load_config(path: Path = DEFAULT_CONFIG_PATH) -> Dict[str, Any]:
    """Load the YAML configuration file."""
    with path.open("r", encoding="utf-8") as cfg:
        return yaml.safe_load(cfg)


CONFIG: Dict[str, Any] = load_config()
