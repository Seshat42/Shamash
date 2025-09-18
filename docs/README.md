# Shamash Documentation

This handbook centralizes architecture, operational, and contributor notes for the Shamash media server and CLI. Start with the high-level [architecture overview](architecture.md) to understand the system boundaries before diving into deployment or development tasks.

## Directory Overview

* `server/` &ndash; FastAPI backend and database models.
* `client/` &ndash; Command line client for interacting with the server.
* `config/` &ndash; YAML configuration for server and client defaults.
* `docs/` &ndash; Documentation sources including this file.
* `tests/` &ndash; pytest suite used for local verification.
* `packaging/pyinstaller/` &ndash; Reproducible build specifications used by the release pipeline to generate standalone executables.

## Deployment Guide

### Local Development

1. Install dependencies with `pip install -r requirements.txt`.
2. Launch the API via `python server/main.py --host 0.0.0.0 --port 8000`.
3. Use the CLI in `client/main.py` to exercise endpoints (`ping`, `login`, `list`, `play`, `sync`).
4. Populate configuration files under `config/` or rely on the shipped defaults for iterative testing.

### Production Rollout

Production deployments should follow a hardened, repeatable process:

1. **Secure configuration** &ndash; Replace the placeholder JWT signing key, set `SHAMASH_DB_PATH` to a persistent volume, and configure Sonarr/Radarr URLs plus API keys. Secrets can be injected through environment variables or overrides in `config/default.yaml`.
2. **Provision accounts** &ndash; Use `server/db.py` helpers or an admin CLI flow to create an administrator before exposing the API to the network.
3. **Select the runtime** &ndash; Run `uvicorn server.app:app --host 0.0.0.0 --port 8000` under `systemd`, `supervisord`, or another supervisor; alternatively deploy the packaged executables or containers described below.
4. **Enforce network boundaries** &ndash; Terminate TLS and perform request logging behind Nginx, Traefik, or Caddy. Restrict inbound traffic to the reverse proxy.
5. **Monitor and maintain** &ndash; Ship logs to your observability stack, review authentication warnings, rotate API keys when staff changes occur, and back up the SQLite database on a regular cadence.

Refer to the production checklist in the root [README](../README.md#production-deployment) for an end-to-end summary.

### Containers and Executables

* **Docker Compose** &ndash; `docker-compose up` builds the server image and optionally launches Sonarr and Radarr helpers. Bind persistent volumes for `server/shamash.db` and media directories before relying on the stack in production.
* **PyInstaller bundles** &ndash; The specs in `packaging/pyinstaller/` mirror the GitHub Actions release workflow. Running `pyinstaller packaging/pyinstaller/shamash_server.spec` (and the client equivalent) yields standalone binaries that embed the configuration directory for easy distribution.

## Security and Compliance

Follow the practices documented in [SECURITY.md](../SECURITY.md) to enforce least privilege, protect credentials, and keep dependencies current. Key expectations include:

* Generate a unique JWT secret for every environment; the server logs a critical warning when the default placeholder is detected.
* Store credentials with bcrypt hashing and restrict administrative routes to users with the `admin` role.
* Run the services with unprivileged accounts, limit exposed network surfaces, and maintain regular operating-system and dependency patching.
* Log authentication events and monitor for anomalies or repeated failures.

## Release Management

Shamash publishes reproducible artifacts for every semantic version tag:

1. Update `CHANGELOG.md` and documentation to describe the release.
2. Run `pytest` locally and, when needed, build the PyInstaller bundles to validate the specs:

   ```bash
   pyinstaller packaging/pyinstaller/shamash_client.spec --noconfirm --distpath dist/pyinstaller --workpath build/pyinstaller
   pyinstaller packaging/pyinstaller/shamash_server.spec --noconfirm --distpath dist/pyinstaller --workpath build/pyinstaller
   ```

3. Create and push a tag such as `git tag v0.2.0` followed by `git push origin v0.2.0`.
4. GitHub Actions runs on Linux, macOS, and Windows to execute tests, build the executables, and attach archives (Linux `.tar.gz`, macOS `.tar.gz`, Windows `.zip`) to the release.

The automation consumes the specs in `packaging/pyinstaller/` to guarantee parity between local builds and the published binaries.

## Authentication

Use `/auth/login` to obtain a JWT token. Include the token in the `Authorization: Bearer` header when calling protected endpoints such as `/ingestion`, `/metadata`, `/stream/ping`, or `/users`.

## Health Checks

The API exposes lightweight health endpoints:

* `GET /ingestion/ping` &ndash; verifies database connectivity for media ingestion (requires an admin token).
* `GET /metadata/ping` &ndash; checks reachability of Sonarr and Radarr and the database (requires an admin token). The endpoint performs authenticated status requests and reports `auth_failed` when API keys are missing or invalid.
* `GET /users/ping` &ndash; verifies database connectivity for user management.
* `GET /stream/ping` &ndash; verifies database connectivity for streaming (requires a token).

### Environment Variables

Set the `JWT_SECRET` variable or edit `config/default.yaml` to configure the secret used for signing JWT tokens. When the server starts with the placeholder `change_this_secret`, it logs a **critical** warning so production deployments do not proceed with the insecure default. `SONARR_API_KEY` and `RADARR_API_KEY` must also be provided when using metadata synchronization.

## Troubleshooting

* **Server fails to start** &ndash; Ensure dependencies are installed with `pip install -r requirements.txt` and that configuration files exist under `config/`.
* **Sonarr/Radarr unreachable** &ndash; Verify `SONARR_API_KEY` and `RADARR_API_KEY` environment variables are set and the services are accessible at their configured URLs. When `/metadata/ping` returns `auth_failed` for either service, double-check the API key values, reset them in the Sonarr or Radarr UI if necessary, and restart the Shamash server to reload the environment.
* **Metadata sync failed** &ndash; `/metadata/sync` returns `sonarr_error` or `radarr_error` when requests to these services fail. Ensure an admin token is supplied, check the server logs for details, and retry once the external services are reachable.
* **`ffplay` not found** &ndash; Install FFmpeg or use `--player` to specify an alternate media player when running the client.
* **Client connection or login errors** &ndash; The CLI prints specific messages such as `Failed to connect to http://localhost:8000` or `Failed to login: invalid JSON response`. Review the message to resolve network issues, credentials, or file permissions.

## Testing

`tests/test_sonarr.py` and `tests/test_radarr.py` monkeypatch `httpx` so the Sonarr and Radarr integrations stay deterministic. The tests assert that each helper targets the `/api/v3` endpoints, includes `X-Api-Key` headers when set, and re-raises `httpx.RequestError` for failures. Follow this pattern for new service clients to avoid contacting real servers during the suite.

## Database Sessions

`server/db.py` wraps every CRUD helper in `try/except/finally` blocks so that each session rolls back and closes when an operation fails. This guarantees that failed transactions do not leak connections or leave partial writes. When adding new queries, follow the same pattern by retrieving a session with `db.get_session()` and closing it in a `finally` clause or via a context manager that performs the cleanup.

## Media Ingestion

The `POST /ingestion/` endpoint stores media metadata. All `/ingestion` operations require administrator credentials so only trusted operators ingest media. The `path` field must be either an `http://` or `https://` URL or a local filesystem path that resolves to an existing file. Local paths are expanded, resolved, and rejected when they contain traversal segments such as `..` or refer to directories or missing files. Provide fully qualified URLs for remote media to avoid validation errors.
Metadata endpoints require the same administrator credentials as ingestion. Authenticate first and include the admin token when checking health or triggering a sync:

```bash
curl -H "Authorization: Bearer $ADMIN_TOKEN" \
  http://localhost:8000/metadata/ping
curl -X POST -H "Authorization: Bearer $ADMIN_TOKEN" \
  http://localhost:8000/metadata/sync
```

Requests without the header return `403` and invalid tokens return `401` before the server contacts Sonarr or Radarr.
