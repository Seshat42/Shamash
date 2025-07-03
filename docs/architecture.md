# Architecture Overview

Shamash is organized into four primary modules:

1. **Media Ingestion** – handles importing IPTV streams and local files. It
   accepts file paths or URLs and stores them as `MediaItem` entries. It
   communicates with the streaming module to provide content.
2. **Metadata Synchronization** – integrates with Sonarr and Radarr to keep
   information about series and movies up to date.
3. **User Management** – maintains accounts, permissions, and preferences in a
   dedicated database with CRUD endpoints for managing users.
4. **Streaming** – serves media to clients using HTTP. It coordinates with the
   caching layer for performance.

A simplified diagram of these interactions is shown below:

```text
+---------+       +---------------+       +---------------------+
| Client  | <---> | Shamash API   | <-->  | SQLite (SQLAlchemy) |
+---------+       +---------------+       +---------------------+
      ^                 ^    ^                     ^
      |                 |    |                |
      |                 |    +--> Caching ----+
      |                 +----------+         |
      |                            |         |
      |   +--------------------+   |   +-------------+
      +---| Streaming Module   |<--+-->| Media       |
          +--------------------+       | Ingestion   |
                 ^                     +-------------+
                 |
                 +--> Metadata Sync
                              |
                              +--> Sonarr
                              +--> Radarr
```

The server exposes a REST interface consumed by the client. External services
Sonarr and Radarr communicate with the metadata module using HTTP requests and
API keys supplied via environment variables. The database and cache provide
state and speed. SQLAlchemy manages the SQLite database so the API can evolve
without manual SQL changes. Each component can run independently, allowing
Shamash to scale horizontally.
