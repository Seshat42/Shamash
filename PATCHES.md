# Summary
- Restricted `/metadata` endpoints in `server/app.py` by applying the existing admin-only dependency at the router level.
- Updated metadata tests to authenticate with admin tokens and assert 401/403 responses for missing, invalid, or non-admin credentials.
- Documented the admin requirement for metadata health and sync operations in `README.md` and `docs/README.md` with example commands for operators.

# Testing
- `pytest`
