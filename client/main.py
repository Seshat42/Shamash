"""CLI entry point for the Shamash media client."""

import argparse
import json
import logging
import shutil
import subprocess
import urllib.request
from pathlib import Path

from urllib.error import HTTPError, URLError

import yaml


CONFIG_FILE = Path(__file__).resolve().parent.parent / "config" / "client.yaml"


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


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
        "--server-url",
        default=get_default_url(),
        help="URL of the Shamash server to connect to",
    )
    parser.add_argument(
        "--token",
        help="JWT token for authenticated endpoints",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("ping", help="Check server availability")
    subparsers.add_parser("sync", help="Synchronize metadata")
    subparsers.add_parser("list", help="List available media items")
    login_parser = subparsers.add_parser("login", help="Obtain and optionally save a JWT token")
    login_parser.add_argument("username", help="Account username")
    login_parser.add_argument("password", help="Account password")
    login_parser.add_argument(
        "--save-token",
        action="store_true",
        help="Persist token to $HOME/.shamash_token",
    )
    play_parser = subparsers.add_parser("play", help="Stream a media item")
    play_parser.add_argument("item_id", type=int, help="ID of media item")
    play_parser.add_argument(
        "--player",
        choices=["ffplay", "vlc"],
        default="ffplay",
        help="External player to launch",
    )

    return parser.parse_args()


def ping_server(url: str) -> None:
    """Attempt to reach the server and print the result."""
    try:
        with urllib.request.urlopen(url) as response:
            print(f"Connected to {url}: {response.status}")
    except HTTPError as exc:
        logger.error("Ping HTTP error", exc_info=exc)
        print(f"Failed to connect to {url}: HTTP {exc.code}")
    except URLError as exc:
        logger.error("Ping failed", exc_info=exc)
        print(f"Failed to connect to {url}: {exc.reason}")


def sync_metadata(url: str) -> None:
    """Send a request to synchronize metadata via the server."""
    endpoint = f"{url.rstrip('/')}/metadata/sync"
    req = urllib.request.Request(endpoint, method="POST")
    try:
        with urllib.request.urlopen(req) as response:
            print(f"Metadata sync: {response.status}")
    except HTTPError as exc:
        logger.error("Metadata sync HTTP error", exc_info=exc)
        print(f"Failed to sync metadata: HTTP {exc.code}")
    except URLError as exc:
        logger.error("Metadata sync failed", exc_info=exc)
        print(f"Failed to sync metadata: {exc.reason}")


def list_media(url: str, token: str | None) -> None:
    """Fetch and display media items from the server."""
    endpoint = f"{url.rstrip('/')}/media/"
    headers: dict[str, str] = {}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    req = urllib.request.Request(endpoint, headers=headers)
    try:
        with urllib.request.urlopen(req) as response:
            items = json.load(response)
        for item in items:
            print(f"{item['id']}: {item['title']}")
    except HTTPError as exc:
        logger.error("List media HTTP error", exc_info=exc)
        print(f"Failed to list media: HTTP {exc.code}")
    except URLError as exc:
        logger.error("List media failed", exc_info=exc)
        print(f"Failed to list media: {exc.reason}")
    except json.JSONDecodeError as exc:
        logger.error("List media JSON error", exc_info=exc)
        print("Failed to list media: invalid JSON response")


def login_user(url: str, username: str, password: str, save_token: bool) -> None:
    """Request a JWT token and optionally persist it."""
    endpoint = f"{url.rstrip('/')}/auth/login"
    payload = json.dumps({"username": username, "password": password}).encode()
    req = urllib.request.Request(
        endpoint,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req) as response:
            data = json.load(response)
        token = data.get("access_token")
        if not token:
            raise ValueError("No token returned")
        print(token)
        if save_token:
            token_path = Path.home() / ".shamash_token"
            try:
                token_path.write_text(token, encoding="utf-8")
            except OSError as exc:
                logger.error("Token save failed", exc_info=exc)
                print(f"Could not save token to {token_path}: {exc}")
    except HTTPError as exc:
        logger.error("Login HTTP error", exc_info=exc)
        print(f"Failed to login: HTTP {exc.code}")
    except URLError as exc:
        logger.error("Login request failed", exc_info=exc)
        print(f"Failed to login: {exc.reason}")
    except json.JSONDecodeError as exc:
        logger.error("Login JSON error", exc_info=exc)
        print("Failed to login: invalid JSON response")
    except ValueError as exc:
        logger.error("Login token error", exc_info=exc)
        print(f"Failed to login: {exc}")


def play_media(url: str, item_id: int, token: str | None, player: str) -> None:
    """Stream a media item using an external player."""
    endpoint = f"{url.rstrip('/')}/stream/{item_id}"
    player_path = shutil.which(player)
    if player_path is None:
        print(f"Player '{player}' not found")
        return
    cmd = [player_path]
    if player == "ffplay" and token:
        cmd.extend(["-headers", f"Authorization: Bearer {token}\r\n"])
    cmd.append(endpoint)
    try:
        subprocess.run(cmd, check=False)
    except OSError as exc:
        logger.error("Player launch failed", exc_info=exc)
        print(f"Failed to launch player: {exc}")


if __name__ == "__main__":
    args = parse_args()

    if args.command == "ping":
        ping_server(args.server_url)
    elif args.command == "sync":
        sync_metadata(args.server_url)
    elif args.command == "list":
        list_media(args.server_url, args.token)
    elif args.command == "play":
        play_media(args.server_url, args.item_id, args.token, args.player)
    elif args.command == "login":
        login_user(
            args.server_url,
            args.username,
            args.password,
            args.save_token,
        )
