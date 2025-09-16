# Plan

1. Review current JWT timestamp handling in `server/auth.py` and identify replacements for `datetime.utcnow`.
2. Update token generation to use `datetime.now(datetime.UTC)` ensuring timezone awareness.
3. Extend `tests/test_auth.py` with coverage that asserts expired tokens are rejected.
4. Run `pytest` to verify the suite passes with the timezone-aware change.
5. Update documentation artifacts including `CHANGELOG.md`, `STATE.md`, `PATCHES.md`, and `VERIFICATIONS.md`.
6. Commit the changes and prepare the pull request message.
