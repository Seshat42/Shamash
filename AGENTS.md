# AGENTS Guidelines

This repository contains the Shamash media server and client.
Follow these guidelines when contributing:

- **Coding Style**: Use 4 spaces per indentation level. Write clear module
  docstrings and inline comments. Name variables and functions using
  `snake_case`, classes with `PascalCase`, and files in `lowercase_with_underscores`.
- **Directories**:
  - `server/` contains server-side code.
  - `client/` contains client-side code.
  - `docs/` holds documentation.
- **Branching**: Work from short-lived feature branches off `main`. Open a
  pull request when ready for review.
- **Documentation**: Keep `README.md`, `AGENTS.md`, `POSTERITY.md`, and
  `CHANGELOG.md` up to date with your changes.
- **Commits**: Commit logical units of work with descriptive messages. Update
  the changelog with a brief summary of each change.
- **Testing**: Run available tests before committing. If no tests exist,
  run `python -m py_compile */*.py` and execute the scripts to ensure they
  start without errors.

General workflow:
1. Create a feature branch.
2. Implement changes with proper style and comments.
3. Run tests or script checks.
4. Update documentation and changelog.
5. Push the branch and open a pull request.

For the reasoning behind these conventions see `POSTERITY.md`.
