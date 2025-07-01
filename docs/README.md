# Shamash Documentation

This folder contains project documentation. Future design and usage
information will be stored here. The high-level architecture diagram is
available in [architecture.md](architecture.md).

## Authentication

Use `/auth/login` to obtain a JWT token. Include the token in the
`Authorization: Bearer` header when calling protected endpoints such as
`/stream/ping`.
