# Plan

1. Review the existing ingestion payload validation and identify edge cases for URLs, missing files, and traversal attempts.
2. Implement a Pydantic validator on `IngestionRequest.path` to accept only HTTP(S) URLs or existing local files without traversal segments.
3. Expand `tests/test_ingestion_users.py` with cases covering valid URLs, valid files, and representative invalid inputs.
4. Document supported ingestion path formats in `docs/README.md` and note the update in `CHANGELOG.md`.
5. Run `pytest` and refresh project artifacts (`STATE.md`, `PATCHES.md`, `VERIFICATIONS.md`, `TODO.md`).
