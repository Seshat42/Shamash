# Plan

1. Add a configuration helper that resolves the effective JWT secret, warns when it remains the insecure default, and integrate the check into server startup and auth secret selection.
2. Extend the pytest suite to capture the warning for the default secret and confirm silence when a custom secret is provided.
3. Document the secret requirements in the READMEs, summarize the change in the changelog, and refresh project artifacts before running pytest.
4. Execute `pytest` to validate the behavior and update `STATE.md`, `PATCHES.md`, `VERIFICATIONS.md`, and related artifacts.
