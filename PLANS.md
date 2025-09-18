# Plan

1. Require administrator authorization for `/metadata` routes by adding the existing `require_role("admin")` dependency in `server/app.py` without impacting other routers.
2. Update metadata-focused tests to login before accessing the endpoints and add assertions that unauthenticated and non-admin requests return 401/403 responses. Adjust related suites such as `tests/test_app.py` accordingly.
3. Document the admin token requirement for metadata health and sync operations in `README.md` and `docs/README.md`, including guidance for operators on authenticating requests.
4. Regenerate supporting artifacts (STATE.md, PATCHES.md, VERIFICATIONS.md, TODO.md) after implementing code and documentation changes, then run the full pytest suite.
