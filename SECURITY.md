# Security Guidelines

This document outlines the planned approach to security for the Shamash project.

## Authentication and Roles

- **Admin vs. User Roles**: The server will distinguish between administrative users and regular users. Administrators manage media libraries and server settings, while regular users stream content.
- **Token Handling**: Authentication will rely on JSON Web Tokens (JWTs). Tokens will be issued upon login and included in each API request's `Authorization` header. Tokens will be time-limited and refreshed periodically to reduce risk of compromise.
- **Storage of Credentials**: Credentials will be stored using secure hashing algorithms (e.g., bcrypt) and never in plain text.

## Dependency Management

- **requirements.txt**: Python dependencies for server and client will be listed in a `requirements.txt` file. The file will be updated using `pip freeze` or `pip-tools`.
- **Keeping Dependencies Updated**: We plan to use Dependabot or a similar tool to automatically open pull requests when dependencies have updates. Dependency updates will be tested before merging.

## Best Practices for Media Servers

- **Least Privilege**: Run server processes with the minimal privileges required.
- **Secure Defaults**: Bind the server only to necessary network interfaces and use HTTPS when deployed in production.
- **Regular Updates**: Keep the operating system and dependencies patched against vulnerabilities.
- **Logging and Monitoring**: Implement logging of authentication attempts and system activity to help detect malicious behavior.

For additional design documentation, see `docs/`.
