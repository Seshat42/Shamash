# Shamash Documentation

This folder contains project documentation. Future design and usage
information will be stored here. The high-level architecture diagram is
available in [architecture.md](architecture.md).

## Directory Overview

* `server/` &ndash; FastAPI backend and database models.
* `client/` &ndash; Command line client for interacting with the server.
* `config/` &ndash; YAML configuration for server and client defaults.
* `docs/` &ndash; Documentation sources including this file.
* `tests/` &ndash; pytest suite used for local verification.

## Authentication

Use `/auth/login` to obtain a JWT token. Include the token in the
`Authorization: Bearer` header when calling protected endpoints such as
`/stream/ping`.

## Health Checks

The API exposes lightweight health endpoints:

* `GET /ingestion/ping` &ndash; verifies database connectivity for media ingestion.
* `GET /metadata/ping` &ndash; checks reachability of Sonarr and Radarr and the database. The endpoint performs authenticated status
  requests and reports `auth_failed` when API keys are missing or invalid.
* `GET /users/ping` &ndash; verifies database connectivity for user management.
* `GET /stream/ping` &ndash; verifies database connectivity for streaming (requires a token).

### Environment Variables

Set the `JWT_SECRET` variable or edit `config/default.yaml` to configure the
secret used for signing JWT tokens. `SONARR_API_KEY` and `RADARR_API_KEY` must
also be provided when using metadata synchronization.

## Troubleshooting

* **Server fails to start** &ndash; Ensure dependencies are installed with
  `pip install -r requirements.txt` and that configuration files exist under
  `config/`.
* **Sonarr/Radarr unreachable** &ndash; Verify `SONARR_API_KEY` and
  `RADARR_API_KEY` environment variables are set and the services are
  accessible at their configured URLs. When `/metadata/ping` returns
  `auth_failed` for either service, double-check the API key values, reset them
  in the Sonarr or Radarr UI if necessary, and restart the Shamash server to
  reload the environment.
* **Metadata sync failed** &ndash; `/metadata/sync` returns `sonarr_error` or
  `radarr_error` when requests to these services fail. Check the server logs for
  details and retry once the external services are reachable.
* **`ffplay` not found** &ndash; Install FFmpeg or use `--player` to specify an
  alternate media player when running the client.
* **Client connection or login errors** &ndash; The CLI prints specific messages
  such as `Failed to connect to http://localhost:8000` or `Failed to login:
  invalid JSON response`. Review the message to resolve network issues,
  credentials, or file permissions.

## Media Ingestion

The `POST /ingestion/` endpoint stores media metadata. The `path` field must be
either an `http://` or `https://` URL or a local filesystem path that resolves
to an existing file. Local paths are expanded, resolved, and rejected when they
contain traversal segments such as `..` or refer to directories or missing
files. Provide fully qualified URLs for remote media to avoid validation
errors.
