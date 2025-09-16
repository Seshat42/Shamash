# Plan

1. Review repository tooling expectations and inventory formatting or linting gaps that `black`, `flake8`, and `pre-commit` must cover.
2. Add lightweight dependencies plus a `.pre-commit-config.yaml` that wires `black` and `flake8`, then run the hooks to format and fix violations.
3. Introduce a GitHub Actions workflow that installs dependencies, runs `pre-commit` checks, and executes `pytest` for regression coverage.
4. Update documentation artifacts (`CHANGELOG.md`, `STATE.md`, `PATCHES.md`, `VERIFICATIONS.md`) to reflect the new tooling and verification steps.
