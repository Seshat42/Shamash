# Shamash

Shamash is an experimental media server and client. It focuses on IPTV streaming while integrating well with existing library managers such as Sonarr and Radarr. The project currently provides a minimal server and command line client written in Python.

THIS IS NOT COMPLETE IN ITS CURRENT STATE

## Prerequisites

- Python 3.10 or later
- Optional: Sonarr and Radarr for automated movie and series downloads

## Running the Server

Run the server from the repository root. `server/main.py` launches `uvicorn` to
serve the FastAPI application:

```bash
python server/main.py --host 0.0.0.0 --port 8000
```

The server starts an HTTP API on the specified host and port.

## Authentication

Create a user in the database using `server/db.py.add_user()` or through a
future management endpoint. Obtain a token via `/auth/login` and pass it as a
`Bearer` token when accessing protected routes such as `/stream/ping`.

## Health Endpoints

Shamash exposes several lightweight health checks:

* `GET /ingestion/ping` &ndash; database connectivity for media ingestion.
* `GET /metadata/ping` &ndash; reachability of Sonarr and Radarr plus database status.
* `GET /users/ping` &ndash; database connectivity for user management.
* `GET /stream/ping` &ndash; database connectivity for streaming (requires a token).

## Running the Client

Use the client subcommands to interact with the server:

```bash
# Ping the API
python client/main.py ping --server-url http://localhost:8000

# Obtain a token and save it for later
python client/main.py login bob secret --save-token

# List available media (requires a token)
python client/main.py list --token YOUR_TOKEN

# Play an item with ffplay
python client/main.py play 1 --token YOUR_TOKEN --player ffplay
```

The `--save-token` flag writes the returned token to `$HOME/.shamash_token` so
subsequent commands can pass it via `--token` without retyping.

## Configuration

Shamash loads settings from `config/default.yaml`. Edit this file to change
the listening port, database path or playlist URLs. The CLI reads the default
server URL from `config/client.yaml`. Environment variables override certain
settings:

* `SHAMASH_DB_PATH` – path to the SQLite database.
* `JWT_SECRET` – overrides the secret used to sign JWT tokens.
* `SONARR_API_KEY` and `RADARR_API_KEY` – credentials for Sonarr and Radarr.
* `SONARR_URL` and `RADARR_URL` – set custom service URLs.

## Configuration Files

The `config/` directory contains YAML files used by both the server and the
client:

* `config/default.yaml` &ndash; server settings including the listening port,
  path to the SQLite database, a `jwt_secret` placeholder and IPTV playlist URLs.
* `config/client.yaml` &ndash; optional file that specifies the default server
  URL for `client/main.py`.

Copy these files and adjust the values to suit your environment. The server and
client will load them automatically on startup.

## Sonarr and Radarr Usage

Configure Sonarr and Radarr to download media into directories that Shamash can access. These tools handle the acquisition and organization of movies and series, while Shamash focuses on streaming them to your devices.

## IPTV Configuration

Provide your IPTV playlist URLs in `config/default.yaml`. The server will stream channels from these playlists alongside your local media library.

## Running in Production

Run Shamash behind a reverse proxy such as Nginx for HTTPS termination.
Start the API using uvicorn directly or under a process manager:

```bash
uvicorn server.app:app --host 0.0.0.0 --port 8000
```

Use `systemd` or a similar tool to manage the service and enable restarts.

See the [`docs/`](docs/README.md) directory for additional design notes,
including a high-level [architecture overview](docs/architecture.md).

## Docker Setup

Build the server image using the included `Dockerfile`:

```bash
docker build -t shamash .
```

Start the API along with optional Sonarr and Radarr containers via
`docker-compose`:

```bash
docker-compose up
```

This configuration mounts the repository into the container so code changes are
reflected immediately during development.

## Testing

Run the test suite locally before committing changes. Tests live in the
`tests/` directory and are executed with:

```bash
pytest
```

These tests are not run by any GitHub workflow, so local verification is
important.
