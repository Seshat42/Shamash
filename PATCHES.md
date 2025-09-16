# Summary
- Added Radarr integration pytest coverage that monkeypatches `httpx` to assert request URLs, headers, payloads, and RequestError propagation.
- Added matching Sonarr integration tests validating the `/api/v3` calls, headers, and error handling without external requests.
- Documented the mocked integration testing approach in `docs/README.md` and recorded the change in the changelog.

# Testing
- `pytest`
