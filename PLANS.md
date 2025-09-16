# Plan

1. Review the metadata health check implementation and integration helpers to determine the appropriate authenticated endpoints and headers for Sonarr and Radarr status probes.
2. Update `server/app.py` so `_check_service` performs authenticated requests that distinguish unreachable services from authentication failures, and ensure `/metadata/ping` surfaces the new status codes.
3. Extend `tests/test_metadata_failure.py` with mocks for `httpx.AsyncClient` to exercise invalid API key responses from Sonarr and Radarr without performing real network calls.
4. Refresh documentation in `docs/README.md` with troubleshooting guidance for API key authentication issues and note the change in `CHANGELOG.md`.
5. Execute `pytest` to confirm the suite passes, then update repository artifacts (`STATE.md`, `PATCHES.md`, `VERIFICATIONS.md`, `TODO.md`) accordingly.
