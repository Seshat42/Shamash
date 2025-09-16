# Plan

1. Refactor database CRUD helpers in `server/db.py` to use try/except/finally blocks (or helper context) so sessions roll back and close on error without changing public interfaces.
2. Introduce regression tests that monkeypatch the session factory to simulate commit/query failures and assert rollback/close behavior alongside existing CRUD coverage.
3. Document the defensive session handling approach in the appropriate documentation and summarize the change in `CHANGELOG.md`.
4. Execute `pytest` to confirm all tests pass and update project artifacts (`STATE.md`, `PATCHES.md`, `VERIFICATIONS.md`, `TODO.md`).
