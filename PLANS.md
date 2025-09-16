# Plan

1. Inspect the Sonarr and Radarr integration helpers to catalog expected URLs, headers, and error propagation behavior.
2. Add pytest modules that monkeypatch `httpx` calls to assert the integrations send the correct requests and raise `RequestError` on failures for both success and error paths.
3. Document the mocked integration test strategy in `docs/README.md` and summarize the additions in `CHANGELOG.md`.
4. Execute `pytest` to verify the new tests and update `STATE.md`, `PATCHES.md`, `VERIFICATIONS.md`, and related artifacts.
