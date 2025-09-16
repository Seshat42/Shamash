# Summary
- Updated the metadata health check to call the Sonarr and Radarr system status endpoints with API keys, reporting `auth_failed` on authentication errors while keeping the requests asynchronous.
- Added tests that stub `httpx.AsyncClient` to simulate invalid Sonarr and Radarr API keys and verify the `/metadata/ping` responses.
- Documented API key troubleshooting guidance and recorded the change in the changelog.

# Testing
- `pytest`
