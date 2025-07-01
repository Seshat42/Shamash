# POSTERITY Notes

These notes explain why we follow the guidelines in `AGENTS.md`.

- **Consistency** keeps the codebase approachable. Adhering to Python style
  and clear naming reduces onboarding time for new contributors.
- **Documentation** across README and change logs helps track project
  history and design decisions.
- **Architecture Overview** in `docs/architecture.md` illustrates how modules
  interact and guides scalability planning.
- **Testing** before committing avoids pushing broken code and maintains
  reliability.
- **Local Test Execution** keeps the CI pipeline minimal and fast. Developers
  run tests locally with `pytest` before pushing changes, which prevents
  workflow slowdowns while still ensuring correctness.
- **Sonarr/Radarr** are used for movie and series management because they
  are mature tools that integrate well with our workflow.
- **IPTV Focus** allows Shamash to fill a gap in open source streaming
  solutions while still supporting personal libraries.
- **Security** is prioritized by running services with minimal privileges and
  limiting network exposure.
- **FastAPI and uvicorn** were selected for the server implementation due to
  their lightweight footprint and strong async support. Running uvicorn through
  our entry script keeps configuration simple while allowing production
  deployments to front the service with a reverse proxy for HTTPS termination.
Running the API in this manner ensures we can restrict open ports and apply
additional security layers such as rate limiting.

- **JWT Authentication** was introduced to secure the API while keeping the
  implementation lightweight. Tokens allow stateless auth so we can scale the
  service horizontally without session affinity. Storing credentials hashed in
 SQLite keeps dependencies minimal during early development. We now use
  SQLAlchemy to manage database access so models can evolve without manual SQL
  and to simplify future migrations.

- **YAML Configuration** keeps settings human-readable and easy to override.
  Loading `config/default.yaml` at startup standardizes server options such as
  port, database location and IPTV playlists. A separate `client.yaml` allows
  the CLI to connect without command line arguments. This structure avoids
  hardcoding paths in code while remaining simple to maintain.

These choices support long-term maintainability, scalability, and a secure
media server environment. Keep this document updated when new decisions are
made.
