# Plan

1. Assess concurrency strategies for metadata sync (thread off blocking helpers versus introducing async HTTP clients) and select the approach that best preserves clarity and testability.
2. Refactor the Sonarr and Radarr integration helpers to provide async refresh functions while retaining logging and error propagation guarantees.
3. Update `server/app.py` to run metadata refreshes without blocking the event loop by awaiting the new async helpers in parallel and maintaining existing error handling semantics.
4. Revise integration and metadata tests to exercise the async helpers and ensure sync failures are reported consistently.
5. Add regression coverage that simulates a slow metadata refresh while serving another request, demonstrating FastAPI remains responsive.
6. Regenerate supporting artifacts (`STATE.md`, `PATCHES.md`, `VERIFICATIONS.md`, `TODO.md`) and run the full pytest suite.
