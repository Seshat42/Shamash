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

## Troubleshooting

* **Server fails to start** &ndash; Ensure dependencies are installed with
  `pip install -r requirements.txt` and that configuration files exist under
  `config/`.
* **Sonarr/Radarr unreachable** &ndash; Verify `SONARR_API_KEY` and
  `RADARR_API_KEY` environment variables are set and the services are
  accessible at their configured URLs.
* **`ffplay` not found** &ndash; Install FFmpeg or use `--player` to specify an
  alternate media player when running the client.
