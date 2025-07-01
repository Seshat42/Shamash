# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]
- Implemented Sonarr and Radarr integration modules with a new `/metadata/sync`
  endpoint and client CLI option `--sync-metadata`.
- Added `/media` and `/stream/{id}` endpoints for listing and streaming media
  items.
- Enhanced `client/main.py` with `argparse` subcommands (`ping`, `sync`, `list`,
  `play`) and streaming via external players.
- Documented new CLI usage and recorded the rationale in POSTERITY.
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

## [0.1.0] - 2025-07-01
- Initial project structure with server, client, and documentation directories.
- Contributor guidelines in `AGENTS.md` and rationale in `POSTERITY.md`.
- Basic server and client scripts for testing connectivity.
