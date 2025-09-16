# Summary
- Replaced JWT expiration timestamp generation with timezone-aware `datetime.now(datetime.UTC)`.
- Added an authentication test asserting expired tokens raise a 401 via `verify_token`.
- Documented the timezone-aware authentication update in the changelog and backlog artifacts.

# Testing
- `pytest`
