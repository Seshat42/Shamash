# Summary
- Embedded user roles in JWT payloads, returning structured claims and enforcing authorization directly from signed tokens.
- Refactored the login flow and FastAPI dependencies to rely on token claims instead of database lookups, and refreshed media route annotations.
- Expanded authentication tests for role-aware tokens and documented the behavior changes in the README and changelog.

# Testing
- `pytest`
