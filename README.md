# Shamash

Shamash is a self-hosted media server and command-line client focused on IPTV streaming while integrating with existing library managers such as Sonarr and Radarr. The repository ships a FastAPI backend, a Python CLI, and reproducible PyInstaller executables that are published for every tagged release.

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
future management endpoint. Users have a `role` of either `user` or `admin`.
Administrative actions, such as managing other accounts or ingesting media,
require an `admin` token. Obtain a token via `/auth/login` and pass it as a
`Bearer` token when accessing protected routes such as `/ingestion`,
`/stream/ping`, or `/users`.

Issued tokens embed the user's role claim so FastAPI dependencies can authorize
requests without repeating a database lookup. The role claim is signed with the
rest of the JWT payload, ensuring tampering is rejected during verification.

## Health Endpoints

Shamash exposes several lightweight health checks:

* `GET /ingestion/ping` &ndash; database connectivity for media ingestion (requires
  an admin token).
* `GET /metadata/ping` &ndash; reachability of Sonarr and Radarr plus database status.
* `GET /users/ping` &ndash; database connectivity for user management.
* `GET /stream/ping` &ndash; database connectivity for streaming (requires a token).

All `/ingestion` endpoints require administrator credentials so that only trusted
operators can add new media entries.

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

The bundled configuration ships with a placeholder `jwt_secret` value of `change_this_secret`. The server logs a **critical** warning on startup when the effective secret matches this default to highlight insecure deployments. Update `config/default.yaml` or set `JWT_SECRET` in production environments to silence the warning while leaving local development unaffected.

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

## Production Deployment

Production environments should prioritize hardened configuration, monitored processes, and repeatable packaging. A typical deployment flow is:

1. **Harden credentials and configuration** – Generate a unique JWT signing secret, point `SHAMASH_DB_PATH` at a persistent volume, and set the Sonarr/Radarr API keys via environment variables or overrides in `config/default.yaml`.
2. **Provision the database** – Use `server/db.py` helpers or the CLI to create at least one administrator account before exposing the API.
3. **Choose the runtime**:
   - Run `uvicorn server.app:app --host 0.0.0.0 --port 8000` under a supervisor such as `systemd`, `supervisord`, or a process manager like `pm2`.
   - Deploy the published PyInstaller executables from `packaging/pyinstaller/` (also available on GitHub Releases) to simplify dependency management and pin dependencies.
   - Or build and run the included container images via `docker-compose up` or your preferred orchestrator, mounting persistent volumes for the database and media libraries.
4. **Terminate TLS at the edge** – Place Shamash behind a reverse proxy such as Nginx, Traefik, or Caddy to enforce HTTPS, rate limiting, and request logging.
5. **Monitor and rotate secrets** – Forward logs to your observability stack, review failed authentication attempts, and rotate tokens or API keys when staff changes occur.

Review the [security guidelines](SECURITY.md) for hardening recommendations and the [`docs/`](docs/README.md) handbook for operational details, including the [architecture overview](docs/architecture.md).

## Docker Setup

Build the server image using the included `Dockerfile`:

```bash
docker build -t shamash .
```

Start the API along with optional Sonarr and Radarr containers via `docker-compose`:

```bash
docker-compose up
```

This configuration mounts the repository into the container so code changes are reflected immediately during development. Adjust volume mounts and environment variables before promoting the stack to production so the database and media files persist outside the container lifecycle.

## Release Process

Follow these steps to cut a tagged release:

1. Update `CHANGELOG.md` with the new version entry and commit the changes.
2. Run `pytest` and optionally build local executables with PyInstaller to verify the specs:

   ```bash
   pyinstaller packaging/pyinstaller/shamash_client.spec --noconfirm --distpath dist/pyinstaller --workpath build/pyinstaller
   pyinstaller packaging/pyinstaller/shamash_server.spec --noconfirm --distpath dist/pyinstaller --workpath build/pyinstaller
   ```
3. Create and push a semantic version tag, for example `git tag v0.2.0` followed by `git push origin v0.2.0`.

Pushing a tag that matches `v*.*.*` triggers the release workflow. GitHub Actions runs `pytest` on Linux, macOS, and Windows, builds the PyInstaller executables, and uploads platform archives (e.g. `shamash-v0.2.0-linux.tar.gz`, `shamash-v0.2.0-windows.zip`) to the GitHub Release alongside the tag.

## Testing

Run the test suite locally before committing changes. Tests live in the
`tests/` directory and are executed with:

```bash
pytest
```

These tests are not run by any GitHub workflow, so local verification is
important.
