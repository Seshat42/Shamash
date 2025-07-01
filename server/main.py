"""Entry point for the Shamash FastAPI server."""

import argparse

import uvicorn

from .app import app


def parse_args() -> argparse.Namespace:
    """Parse command line arguments for server configuration."""
    parser = argparse.ArgumentParser(description="Start the Shamash API server.")
    parser.add_argument(
        "--host",
        default="0.0.0.0",
        help="Host address to bind (default: 0.0.0.0)",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to listen on (default: 8000)",
    )
    return parser.parse_args()


def main() -> None:
    """Run the FastAPI application with uvicorn."""
    args = parse_args()
    uvicorn.run(app, host=args.host, port=args.port)


if __name__ == "__main__":
    main()
