# Summary
- Adopted `pre-commit` with `black` and `flake8`, added the required dependencies, and reformatted the repository to satisfy the hooks.
- Created a GitHub Actions workflow that installs dependencies, runs the pre-commit lint checks, and executes `pytest` on pushes and pull requests.
- Updated the changelog to summarize the new tooling and automation.

# Testing
- `pre-commit run --all-files`
- `pytest`
