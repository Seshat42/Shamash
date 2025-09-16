# Project Invariants
- R1: Use four spaces for indentation and provide docstrings for modules and functions.
- R2: Run pytest before committing changes.
- R3: Update documentation and changelog alongside code modifications.

# Task Requirements
- T7: Replace `datetime.utcnow` in token creation with timezone-aware `datetime.now(datetime.UTC)`.
- T8: Add unit coverage ensuring expired tokens are rejected to validate token expiry logic.
- T9: Run `pytest` to confirm the suite passes with the timezone-aware change.
- T10: Update `CHANGELOG.md` with the authentication timestamp adjustment.

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
- Cycle 11: Planned role-based access control and updated planning artifacts.
- Cycle 12: Implemented role column, migration, and admin enforcement on user routes.
- Cycle 13: Updated tests and documentation, then executed role-based CRUD tests.
- Cycle 14: Reviewed timezone-aware JWT requirements and repository instructions for the new task.
- Cycle 15: Refreshed planning artifacts to outline the timezone-aware authentication update.
- Cycle 16: Replaced naive token expiration timestamps with `datetime.now(datetime.UTC)`.
- Cycle 17: Added an expiry regression test ensuring `verify_token` rejects expired tokens.
- Cycle 18: Updated changelog and backlog to capture the timezone-aware authentication change.
- Cycle 19: Executed the full pytest suite to validate the update.

# Decision Log
- D1: Chose database `SELECT 1` query to verify connectivity for ingestion, users, and streaming health.
- D2: Implemented HTTP HEAD requests to Sonarr and Radarr for metadata health without requiring sync commands.
- D3: Expanded existing test rather than adding new functions to match execution command.
- D4: Utilized `urllib.error` exceptions and logging for clearer client error reporting.
- D5: Kept user-facing prints for actionable messages while logging full error details.
- D6: Opted to verify roles against the database per request instead of encoding them into tokens for immediate revocation.
- D7: Simulated expired tokens by monkeypatching `TOKEN_EXPIRE_SECONDS` to a negative value for deterministic testing.
