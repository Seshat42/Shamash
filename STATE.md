# Project Invariants
- R1: Use four spaces for indentation and provide docstrings for modules and functions.
- R2: Run pytest before committing changes.
- R3: Update documentation and changelog alongside code modifications.

# Task Requirements
- T1: Replace generic exception handlers in the client with targeted errors and logging.
- T2: Document new client error messages in `docs/README.md` and `CHANGELOG.md`.
- T3: Run `pytest tests/test_client_login.py::test_login_saves_token -q`.

# Cognitive Ledger
- Cycle 1: Inspected repository structure and existing placeholder endpoints.
- Cycle 2: Added database and external service health check helpers; replaced placeholder responses.
- Cycle 3: Expanded tests to verify health endpoints and token-protected stream check.
- Cycle 4: Updated documentation and changelog with new health endpoints.
- Cycle 5: Executed targeted and full test suites to confirm functionality.
- Cycle 6: Reviewed client CLI for broad `Exception` handlers.
- Cycle 7: Introduced specific exception handling with logging in `client/main.py`.
- Cycle 8: Documented error messages in `docs/README.md` and updated `CHANGELOG.md`.
- Cycle 9: Ran `pytest tests/test_client_login.py::test_login_saves_token -q`.
- Cycle 10: Committed changes and prepared pull request.

# Decision Log
- D1: Chose database `SELECT 1` query to verify connectivity for ingestion, users, and streaming health.
- D2: Implemented HTTP HEAD requests to Sonarr and Radarr for metadata health without requiring sync commands.
- D3: Expanded existing test rather than adding new functions to match execution command.
- D4: Utilized `urllib.error` exceptions and logging for clearer client error reporting.
- D5: Kept user-facing prints for actionable messages while logging full error details.
