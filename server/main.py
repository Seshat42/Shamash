"""Simple placeholder web server for Shamash media server."""

import argparse
from http.server import HTTPServer, SimpleHTTPRequestHandler


def parse_args():
    """Parse command line arguments for server configuration."""
    parser = argparse.ArgumentParser(description="Start the Shamash server.")
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="Port to listen on (default: 8000)",
    )
    return parser.parse_args()


def run_server(port: int) -> None:
    """Run a basic HTTP server on the specified port."""
    server_address = ("", port)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print(f"Shamash server running on http://localhost:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    args = parse_args()
    run_server(args.port)
