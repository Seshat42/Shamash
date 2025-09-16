# Summary
- Added a Pydantic field validator on `IngestionRequest.path` to accept only HTTP(S) URLs or resolved existing local files while rejecting traversal attempts.
- Expanded ingestion tests to cover valid local files and invalid URL or traversal submissions, and ensured remote URLs remain accepted.
- Documented supported ingestion path formats and recorded the validation update in the changelog.

# Testing
- `pytest`
