"""CLI entry point for the Shamash media client."""

import argparse
import urllib.request


def parse_args():
    """Parse command line arguments for client configuration."""
    parser = argparse.ArgumentParser(description="Run the Shamash client.")
    parser.add_argument(
        "server_url",
        nargs="?",
        default="http://localhost:8000",
        help="URL of the Shamash server to connect to",
    )
    return parser.parse_args()


def ping_server(url: str) -> None:
    """Attempt to reach the server and print the result."""
    try:
        with urllib.request.urlopen(url) as response:
            print(f"Connected to {url}: {response.status}")
    except Exception as exc:  # Broad except for placeholder simplicity
        print(f"Failed to connect to {url}: {exc}")


if __name__ == "__main__":
    args = parse_args()
    ping_server(args.server_url)
