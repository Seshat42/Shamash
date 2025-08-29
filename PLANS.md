# Plan

1. Replace placeholder ping endpoints in `server/app.py` with health checks:
   - Add helper functions to verify database connectivity and external service reachability.
   - Update `/ingestion/ping`, `/metadata/ping`, `/users/ping`, and `/stream/ping` to return real statuses.
2. Update tests to assert new health responses and ensure no placeholder strings remain.
3. Revise documentation (`README.md`, `docs/README.md`) describing the health endpoints.
4. Record changes in `CHANGELOG.md`.
5. Run `pytest tests/test_app.py::test_app_includes_routes -q` and full test suite for verification.
6. Commit changes and open a pull request.
