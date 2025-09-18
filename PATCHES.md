# Summary
- Restricted `/ingestion` endpoints in `server/app.py` by adding an admin-only dependency.
- Updated `tests/test_ingestion_users.py` to authenticate ingestion calls with admin tokens and to assert 403 responses for unauthorized users.
- Documented the admin ingestion requirement in `README.md` and `docs/README.md` for operators.

# Testing
- `pytest`
