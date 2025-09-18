# Plan

1. Protect `/ingestion` endpoints by requiring admin credentials while preserving the existing path validation behavior.
2. Update ingestion tests to authenticate as admin for positive cases and verify non-admin or unauthenticated calls receive 403 responses.
3. Document the administrative requirement for ingestion workflows in README.md and docs/README.md so operators adjust credentials accordingly.
4. Rebuild supporting artifacts (STATE.md, PATCHES.md, VERIFICATIONS.md, TODO.md) after implementing code and documentation changes.
