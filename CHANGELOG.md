# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
- Pinned `httpx` to `<0.24` for compatibility with Starlette 0.27.
- Added `login` client subcommand with optional token storage.
- Added `jwt_secret` option in `config/default.yaml` and `JWT_SECRET` environment
  variable for token signing.
- Replaced SHA-256 password hashing with bcrypt and updated tests.
- Documented secret handling and updated AGENTS, POSTERITY and SECURITY notes.
- Added Dockerfile and `docker-compose.yaml` for containerized deployment and
  documented usage.
- Implemented Sonarr and Radarr integration modules with a new `/metadata/sync`
  endpoint and client CLI option `--sync-metadata`.
- Added `/media` and `/stream/{id}` endpoints for listing and streaming media
  items.
- Enhanced `client/main.py` with `argparse` subcommands (`ping`, `sync`, `list`,
  `play`) and streaming via external players.
- Documented new CLI usage and recorded the rationale in POSTERITY.
- Implemented POST `/ingestion/` and `/users` CRUD endpoints and added tests.
- Added error handling for Sonarr and Radarr failures with detailed
  `/metadata/sync` responses.
- Documented failure modes and updated architecture overview.
- Documented external API key setup and updated architecture overview.
- Added architecture overview in `docs/architecture.md` and updated
  documentation references.
- Migrated server to FastAPI with uvicorn and added module routers.
- Added `requirements.txt` with development dependencies.
- Updated documentation to reflect new server startup instructions.
- Implemented JWT authentication with `/auth/login` and protected routes.
- Stored hashed credentials in SQLite via `server/db.py`.
- Documented token usage and updated contributor guidelines and posterity notes.
- Introduced SQLAlchemy models with basic CRUD utilities and database setup.
- Updated architecture diagram to illustrate SQLAlchemy-backed SQLite.
- Established `pytest`-based test suite executed locally only and added
  `SHAMASH_DB_PATH` override for isolated databases.
- Introduced YAML configuration files under `config/` and loader module.
- Client now reads default server URL from `config/client.yaml`.
- Documented configuration format and rationale in README and POSTERITY.
- Expanded README with configuration, authentication and production sections.
- Documented module directory purposes and troubleshooting tips in `docs/README.md`.
- Updated AGENTS and POSTERITY to reference the new documentation files.
- Added directory structure, testing workflow and style reminder sections to
  `AGENTS.md`.
- Documented reasons for FastAPI, JWT and SQLite usage in `POSTERITY.md`.

## [0.1.0] - 2025-07-01
- Initial project structure with server, client, and documentation directories.
- Contributor guidelines in `AGENTS.md` and rationale in `POSTERITY.md`.
- Basic server and client scripts for testing connectivity.
