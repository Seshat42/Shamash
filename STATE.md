# Project Invariants
- R1: Use four spaces for indentation and provide docstrings for modules and functions.
- R2: Run pytest before committing changes.
- R3: Update documentation and changelog alongside code modifications.

# Task Requirements
- T21: Validate ingestion paths as either HTTP(S) URLs or existing local files without traversal segments.
- T22: Expand tests to cover valid and invalid ingestion paths for both remote URLs and local files.
- T23: Document supported ingestion path formats in `docs/README.md`.
- T24: Record the validation update in `CHANGELOG.md` and ensure `pytest` passes.

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
- Cycle 20: Reviewed authentication modules and existing tests to scope the role claim updates.
- Cycle 21: Embedded role claims into token creation and verification while refactoring dependencies to consume structured claims.
- Cycle 22: Updated media and auth tests to exercise role-aware tokens and added coverage for authorization decisions.
- Cycle 23: Documented the role claim workflow in README and CHANGELOG and pruned the backlog item.
- Cycle 24: Ran the full pytest suite to validate the role-embedded token flow.
- Cycle 25: Reviewed metadata health checks and integration modules, then refreshed planning artifacts for the authenticated ping update.
- Cycle 26: Reworked `_check_service` to call the authenticated system status endpoints and parallelized the Sonarr/Radarr probes in `/metadata/ping`.
- Cycle 27: Stubbed `httpx.AsyncClient` in tests to simulate invalid Sonarr and Radarr API keys and verified the reported statuses.
- Cycle 28: Updated documentation and the changelog with API key troubleshooting guidance.
- Cycle 29: Executed the full pytest suite to confirm the authenticated checks pass across the test suite.
- Cycle 30: Reviewed ingestion path validation requirements and inspected server ingestion code and tests to scope the update.
- Cycle 31: Refreshed the planning artifact for the ingestion path validation effort.
- Cycle 32: Added a Pydantic validator ensuring ingestion paths are constrained to HTTP(S) URLs or existing local files.
- Cycle 33: Expanded ingestion tests with valid local files and invalid URL and traversal scenarios.
- Cycle 34: Documented ingestion path requirements and updated the changelog entry.
- Cycle 35: Ran the pytest suite to verify the ingestion validation and tests.

# Decision Log
- D1: Chose database `SELECT 1` query to verify connectivity for ingestion, users, and streaming health.
- D2: Implemented HTTP HEAD requests to Sonarr and Radarr for metadata health without requiring sync commands.
- D3: Expanded existing test rather than adding new functions to match execution command.
- D4: Utilized `urllib.error` exceptions and logging for clearer client error reporting.
- D5: Kept user-facing prints for actionable messages while logging full error details.
- D6: Opted to verify roles against the database per request instead of encoding them into tokens for immediate revocation (superseded by D8).
- D7: Simulated expired tokens by monkeypatching `TOKEN_EXPIRE_SECONDS` to a negative value for deterministic testing.
- D8: Moved role enforcement to rely on signed JWT claims to eliminate authorization-time database queries while preserving expiry-based revocation.
- D9: Queried the Sonarr and Radarr system status endpoints asynchronously and interpreted 401/403 responses as `auth_failed` to detect invalid API keys without blocking the event loop.
- D10: Normalized accepted local ingestion paths to resolved filesystem locations to prevent traversal and ensure consistency.
