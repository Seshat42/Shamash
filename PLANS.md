# Plan

1. Capture the release packaging requirements in the state log and confirm client and server entry points for PyInstaller specs.
2. Add deterministic PyInstaller spec files that bundle the configuration directory, then exercise a Linux build to validate the layouts.
3. Update GitHub Actions to run pytest across Linux, macOS, and Windows and add a tag-driven release workflow that packages binaries after tests and uploads them to the GitHub Release.
4. Document the release process in `README.md` and `docs/README.md`, create the 0.2.0 changelog entry, and refresh the verification artifacts.
