# POSTERITY Notes

These notes explain why we follow the guidelines in `AGENTS.md`.

- **Consistency** keeps the codebase approachable. Adhering to Python style
  and clear naming reduces onboarding time for new contributors.
- **Documentation** across README and change logs helps track project
  history and design decisions.
- **Architecture Overview** in `docs/architecture.md` illustrates how modules
  interact and guides scalability planning.
- **Separation of Concerns** is enforced by dividing the codebase into
  independent modules for ingestion, metadata, streaming and authentication.
  This clarity enables focused tests and limits the blast radius of
  security-sensitive code.
- **Testing** before committing avoids pushing broken code and maintains
  reliability.
- **Local Test Execution** keeps the CI pipeline minimal and fast. Developers
  run tests locally with `pytest` before pushing changes, which prevents
  workflow slowdowns while still ensuring correctness.
- **Sonarr/Radarr** are used for movie and series management because they
  are mature tools that integrate well with our workflow.
- **Metadata Synchronization** allows Shamash to reuse these managers' rich
  libraries. Keeping metadata in sync ensures the streaming catalog reflects the
  latest downloads without reinventing scraping logic.
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

- **SQLite as initial storage** keeps the project simple to set up while we
  iterate on the schema. A single file database means no external dependencies
  and easy cleanup during testing. SQLAlchemy abstracts queries so moving to a
  dedicated database later will require minimal code changes.

- **JWT Authentication** was introduced to secure the API while keeping the
  implementation lightweight. Tokens allow stateless auth so we can scale the
  service horizontally without session affinity. Storing credentials hashed in
  SQLite keeps dependencies minimal during early development. We now use
  SQLAlchemy to manage database access so models can evolve without manual SQL
  and to simplify future migrations.

- **Secrets via environment variables** avoid hard-coding sensitive values.
  Loading the JWT secret from `JWT_SECRET` or `config/default.yaml` allows each
  deployment to provide its own key while keeping development simple.

- **bcrypt password hashing** replaced SHA-256 to mitigate rainbow table
  attacks. Bcrypt provides built-in salting and configurable work factors.

- **YAML Configuration** keeps settings human-readable and easy to override.
  Loading `config/default.yaml` at startup standardizes server options such as
  port, database location and IPTV playlists. A separate `client.yaml` allows
  the CLI to connect without command line arguments. This structure avoids
  hardcoding paths in code while remaining simple to maintain.

  - **CLI Subcommands** were added to make the client extensible. Using
    `argparse` subparsers keeps the command structure clear as more features are
    introduced. Streaming support relies on external players like `ffplay` which
    allows us to avoid embedding complex media libraries while still enabling
    playback over authenticated HTTP endpoints.
  - **Containerization** ensures a consistent runtime and simplifies
    deployments. Building the server image from the official Python base allows
    contributors to run the API with identical dependencies. `docker-compose`
    orchestrates the API alongside Sonarr and Radarr for metadata sync.
  - **Documentation Overview** in `docs/README.md` guides newcomers by describing
    each module and capturing troubleshooting steps. Maintaining this file helps
    reduce onboarding questions.

These choices support long-term maintainability, scalability, and a secure
media server environment. Keep this document updated when new decisions are
made.
