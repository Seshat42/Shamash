# Shamash

Shamash is an experimental media server and client. It focuses on IPTV streaming while integrating well with existing library managers such as Sonarr and Radarr. The project currently provides a minimal server and command line client written in Python.

## Prerequisites

- Python 3.10 or later
- Optional: Sonarr and Radarr for automated movie and series downloads

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourorg/shamash.git
   cd shamash
   ```
2. Install dependencies. The server and client currently rely only on the Python standard library, so there is no `requirements.txt` yet. Future versions will document additional dependencies here.

## Running the Server

Run the server from the repository root:

```bash
python server/main.py --port 8000
```

The server starts an HTTP service on the given port and serves files from the current directory.

## Running the Client

Run the client and specify the server URL if different from the default:

```bash
python client/main.py http://localhost:8000
```

The client simply pings the server and prints the HTTP status. It will be expanded in future releases.

## Sonarr and Radarr Usage

Configure Sonarr and Radarr to download media into directories that Shamash can access. These tools handle the acquisition and organization of movies and series, while Shamash focuses on streaming them to your devices.

## IPTV Configuration

Provide your IPTV playlist URL and any required credentials through the Shamash configuration file (to be implemented). The server will stream channels from this playlist alongside your local media library.

See the [`docs/`](docs/README.md) directory for additional design notes.
