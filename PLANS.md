# Plan

1. Add `role` column to `User` model and database with migration logic.
2. Update CRUD utilities and tests to handle user roles.
3. Implement `require_role` FastAPI dependency and secure user management endpoints.
4. Document role-based access in `README.md` and `SECURITY.md`, and note in `CHANGELOG.md`.
5. Run `pytest tests/test_ingestion_users.py::test_user_crud_endpoints -q`.
6. Commit changes and open a pull request.
