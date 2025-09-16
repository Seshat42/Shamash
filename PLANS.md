# Plan

1. Review current JWT utilities and dependencies to determine required changes for embedding role claims and consuming them without database lookups.
2. Update `server/auth.py` to include the role in issued tokens, return structured token data from verification, and have `require_role` authorize purely via token claims.
3. Adjust authentication-dependent routes or helpers, ensuring they accept the updated token payload without unnecessary queries.
4. Expand and update tests to cover role claim issuance, validation, and authorization, including ensuring the database is not queried during role checks.
5. Update documentation (`README.md`, `CHANGELOG.md`) and repository artifacts (`STATE.md`, `PATCHES.md`, `VERIFICATIONS.md`, `TODO.md`) to reflect the new token behavior.
6. Run `pytest` to validate the suite and capture results for verification.
