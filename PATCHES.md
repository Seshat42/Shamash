# Summary
- Added `role` column to users with migration and CRUD support.
- Enforced admin-only access on user management routes via `require_role` dependency.
- Documented roles in README and SECURITY guidelines and updated tests.

# Testing
- `pytest tests/test_ingestion_users.py::test_user_crud_endpoints -q`
