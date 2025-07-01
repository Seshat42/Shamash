# Shamash

Shamash is an experimental media server and client. It focuses on IPTV streaming while integrating well with existing library managers such as Sonarr and Radarr. The project currently provides a minimal server and command line client written in Python.

## Prerequisites

- Python 3.10 or later
- Optional: Sonarr and Radarr for automated movie and series downloads

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourorg/shamash.git
   cd shamash
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Running the Server

Run the server from the repository root. `server/main.py` launches `uvicorn` to
serve the FastAPI application:

```bash
python server/main.py --host 0.0.0.0 --port 8000
```

The server starts an HTTP API on the specified host and port.

### Authentication

Create a user in the database using `server/db.py.add_user()` or through a
future management endpoint. Obtain a token via `/auth/login` and pass it as a
`Bearer` token when accessing protected routes such as `/stream/ping`.

## Running the Client

Run the client and specify the server URL if different from the default:

```bash
python client/main.py http://localhost:8000
```

The client simply pings the server and prints the HTTP status. It will be expanded in future releases.

## Configuration Files

The `config/` directory contains YAML files used by both the server and the
client:

* `config/default.yaml` &ndash; server settings including the listening port,
  path to the SQLite database and IPTV playlist URLs.
* `config/client.yaml` &ndash; optional file that specifies the default server
  URL for `client/main.py`.

Copy these files and adjust the values to suit your environment. The server and
client will load them automatically on startup.

## Sonarr and Radarr Usage

Configure Sonarr and Radarr to download media into directories that Shamash can access. These tools handle the acquisition and organization of movies and series, while Shamash focuses on streaming them to your devices.

## IPTV Configuration

Provide your IPTV playlist URLs in `config/default.yaml`. The server will stream channels from these playlists alongside your local media library.

See the [`docs/`](docs/README.md) directory for additional design notes,
including a high-level [architecture overview](docs/architecture.md).

## Testing

Run the test suite locally before committing changes. Tests live in the
`tests/` directory and are executed with:

```bash
pytest
```

These tests are not run by any GitHub workflow, so local verification is
important.
