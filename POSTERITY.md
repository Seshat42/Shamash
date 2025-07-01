# POSTERITY Notes

These notes explain why we follow the guidelines in `AGENTS.md`.

- **Consistency** keeps the codebase approachable. Adhering to Python style
  and clear naming reduces onboarding time for new contributors.
- **Documentation** across README and change logs helps track project
  history and design decisions.
- **Testing** before committing avoids pushing broken code and maintains
  reliability.
- **Sonarr/Radarr** are used for movie and series management because they
  are mature tools that integrate well with our workflow.
- **IPTV Focus** allows Shamash to fill a gap in open source streaming
  solutions while still supporting personal libraries.
- **Security** is prioritized by running services with minimal privileges and
  limiting network exposure.

These choices support long-term maintainability, scalability, and a secure
media server environment. Keep this document updated when new decisions are
made.
