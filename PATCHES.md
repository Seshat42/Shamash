# Summary
- Refactored `/metadata/sync` to await asynchronous Sonarr and Radarr refresh helpers so metadata updates no longer block the FastAPI event loop.
- Added `async_refresh_series` and `async_refresh_movies` implementations plus unit tests that validate their request payloads and error handling with `httpx.AsyncClient`.
- Introduced a concurrency regression test that proves a slow metadata sync does not prevent servicing a simultaneous ping request.

# Testing
- `pytest`
