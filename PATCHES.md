# Summary
- Hardened `server/db.py` CRUD helpers with try/except/finally blocks to roll back and close sessions on failure without changing their interfaces.
- Added pytest regressions that monkeypatch the session factory to simulate commit/query errors and assert rollback plus closure semantics.
- Documented the defensive session pattern in `docs/README.md` and noted the change in `CHANGELOG.md`.

# Testing
- `pytest`
