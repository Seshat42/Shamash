# AGENTS Guidelines

This repository contains the Shamash media server and client.
Follow these guidelines when contributing:

- **Coding Style**: Use 4 spaces per indentation level. Write clear module
  docstrings and inline comments. Name variables and functions using
  `snake_case`, classes with `PascalCase`, and files in `lowercase_with_underscores`.
- **Directories**:
  - `server/` contains server-side code.
  - `client/` contains client-side code.
  - `docs/` holds documentation.
  - `docs/architecture.md` contains the high-level architecture diagram. Update
    it when major components or external integrations change.
- **Branching**: Work from short-lived feature branches off `main`. Open a
  pull request when ready for review.
- **Documentation**: Keep `README.md`, `AGENTS.md`, `POSTERITY.md`, and
  `CHANGELOG.md` up to date with your changes.
- **Commits**: Commit logical units of work with descriptive messages. Update
  the changelog with a brief summary of each change.
- **Testing**: Run `pytest` on the `tests/` directory before committing.
  Tests are executed locally only and are intentionally omitted from any GitHub
  workflow. Always create new tests when adding features. If no tests exist,
  run `python -m py_compile */*.py` and execute the scripts to ensure they start
  without errors.
- **Configuration**: YAML files in `config/` provide default settings for the
  server and client. Update `config/default.yaml` and `config/client.yaml` when
  introducing new options.
- **Client CLI**: Use subcommands (`ping`, `sync`, `list`, `play`) implemented
  with `argparse` in `client/main.py`. Pass `--token` when calling endpoints
  that require authentication.
- **Server Framework**: The API uses FastAPI served by uvicorn. Add new
  endpoints via routers in `server/app.py` to keep the application modular.
- **Authentication**: JWT utilities live in `server/auth.py`. Use
  `token_required` as a dependency on protected endpoints. Credentials are
 stored hashed in the SQLite database managed by `server/db.py`.
- **Database**: A SQLite file `server/shamash.db` stores all data. Import
  `server.db` to create tables automatically using SQLAlchemy models defined in
  `server/models.py`. Set the `SHAMASH_DB_PATH` environment variable to point to
  an alternate database when running tests.

- **External API Keys**: Integrations with Sonarr and Radarr require API keys.
  Set the `SONARR_API_KEY` and `RADARR_API_KEY` environment variables so the
  server can authenticate to these services. Optionally adjust `SONARR_URL` and
  `RADARR_URL` if the services run on non-default ports.

General workflow:
1. Create a feature branch.
2. Implement changes with proper style and comments.
3. Run tests or script checks.
4. Update documentation and changelog.
5. Push the branch and open a pull request.

For the reasoning behind these conventions see `POSTERITY.md`.
