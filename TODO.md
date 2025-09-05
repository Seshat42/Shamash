# Backlog
- Replace `datetime.utcnow` usage in `server/auth.py` with timezone-aware `datetime.now(datetime.UTC)`.
- Expand metadata health check to validate API keys and authenticate with external services.
- Include user role in JWT claims to avoid database lookup for authorization.
