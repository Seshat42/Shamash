# Project Invariants
- R1: Use four spaces for indentation and provide docstrings for modules and functions.
- R2: Run pytest before committing changes.
- R3: Update documentation and changelog alongside code modifications.

# Task Requirements
- T1: Replace placeholder ping endpoints with real health checks.
- T2: Ensure no placeholder strings remain in responses.
- T3: Update tests, documentation, and changelog accordingly.

# Cognitive Ledger
- Cycle 1: Inspected repository structure and existing placeholder endpoints.
- Cycle 2: Added database and external service health check helpers; replaced placeholder responses.
- Cycle 3: Expanded tests to verify health endpoints and token-protected stream check.
- Cycle 4: Updated documentation and changelog with new health endpoints.
- Cycle 5: Executed targeted and full test suites to confirm functionality.

# Decision Log
- D1: Chose database `SELECT 1` query to verify connectivity for ingestion, users, and streaming health.
- D2: Implemented HTTP HEAD requests to Sonarr and Radarr for metadata health without requiring sync commands.
- D3: Expanded existing test rather than adding new functions to match execution command.
