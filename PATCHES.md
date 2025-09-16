# Summary
- Added configuration helpers that resolve the JWT secret, emit a critical warning when it matches the insecure default, and wired the check into auth and app startup.
- Extended the application tests to assert the default secret triggers the warning while a custom secret remains silent.
- Documented the secret configuration expectations in the READMEs and noted the change in the changelog.

# Testing
- `pytest`
