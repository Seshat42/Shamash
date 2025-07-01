"""CLI entry point for the Shamash media client."""

import argparse
import urllib.request
from pathlib import Path

import yaml


CONFIG_FILE = Path(__file__).resolve().parent.parent / "config" / "client.yaml"


def get_default_url() -> str:
    """Return the server URL from configuration or a built-in default."""
    if CONFIG_FILE.exists():
        with CONFIG_FILE.open("r", encoding="utf-8") as cfg:
            data = yaml.safe_load(cfg) or {}
        return data.get("server_url", "http://localhost:8000")
    return "http://localhost:8000"


def parse_args() -> argparse.Namespace:
    """Parse command line arguments for client configuration."""
    parser = argparse.ArgumentParser(description="Run the Shamash client.")
    parser.add_argument(
        "server_url",
        nargs="?",
        default=get_default_url(),
        help="URL of the Shamash server to connect to",
    )
    parser.add_argument(
        "--sync-metadata",
        action="store_true",
        help="Trigger metadata synchronization instead of pinging",
    )
    return parser.parse_args()


def ping_server(url: str) -> None:
    """Attempt to reach the server and print the result."""
    try:
        with urllib.request.urlopen(url) as response:
            print(f"Connected to {url}: {response.status}")
    except Exception as exc:  # Broad except for placeholder simplicity
        print(f"Failed to connect to {url}: {exc}")


def sync_metadata(url: str) -> None:
    """Send a request to synchronize metadata via the server."""
    endpoint = f"{url.rstrip('/')}/metadata/sync"
    req = urllib.request.Request(endpoint, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Metadata sync: {response.status}")
    except Exception as exc:  # Broad except for placeholder simplicity
        print(f"Failed to sync metadata: {exc}")


if __name__ == "__main__":
    args = parse_args()
    if args.sync_metadata:
        sync_metadata(args.server_url)
    else:
        ping_server(args.server_url)
