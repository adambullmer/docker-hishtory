# hiSHtory Unified Self-Hosted Server (Ingress + Web UI)

[![CI/CD Status](https://github.com/ddworken/hishtory/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/ddworken/hishtory/actions)
[![GitHub Container Registry](https://img.shields.io/badge/ghcr.io-hishtory--server-blue?logo=docker)](https://ghcr.io)
[![Base Image](https://img.shields.io/badge/base-linuxserver%2Falpine%3A3.21-009688?logo=alpine-linux)](https://github.com/linuxserver/docker-baseimage-alpine)
[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)

A production-grade, hardened container image for self-hosting both the **hiSHtory Ingress Server** (encrypted shell history sync backend) and the **hiSHtory Web UI** (browser-based history explorer) through a single unified public port.

---

## Features

- **Single Public Port (`8080`)**: Embedded Nginx reverse proxy segments incoming traffic seamlessly:
  - `/api/*` & `/healthcheck` &rarr; Ingress Sync API (`127.0.0.1:8081`)
  - `/*` &rarr; Web UI Dashboard (`127.0.0.1:8000`) protected with HTTP Basic Auth.
- **LinuxServer.io Standards**: Built on `baseimage-alpine:3.21` with **S6-Overlay v3** and `PUID`/`PGID` permission management.
- **Docker Secrets & Encrypted Auth**:
  - Full support for Docker Secrets and `_FILE` environment variables (`WEB_PASSWORD_FILE`, `HISHTORY_SECRET_KEY_FILE`, etc.).
  - Accepts pre-computed password hashes (`WEB_PASSWORD_HASH` / `WEB_AUTH_HASH`) so plaintext credentials are never stored.
- **Single-User / Token Isolation**: Direct support for binding the container and Web UI to your personal `HISHTORY_SECRET_KEY`.
- **Database Flexibility**: Out-of-the-box SQLite with persistent volume (`/config/hishtory.db`) or high-performance PostgreSQL.
- **Multi-Architecture**: Native builds for `linux/amd64` and `linux/arm64` (Raspberry Pi, Apple Silicon, AWS Graviton).
- **Automated CI/CD**: GitHub Actions pipeline building and publishing directly to the GitHub Container Registry (`ghcr.io`).

---

## Architecture Overview

```
                          ┌─────────────────────────────┐
                          │ External Traffic (Port 8080)│
                          └──────────────┬──────────────┘
                                         │
                         ┌───────────────▼──────────────┐
                         │     Nginx Reverse Proxy      │
                         └───────┬──────────────┬───────┘
          /api/* & /healthcheck  │              │  /* (Protected by Basic Auth)
                                 │              │
                    ┌────────────▼─────┐  ┌─────▼────────────┐
                    │  Ingress Server  │  │   Web UI Server  │
                    │  127.0.0.1:8081  │  │   127.0.0.1:8000 │
                    └────────────┬─────┘  └─────┬────────────┘
                                 │              │
                                 └───────┬──────┘
                                         │
                             ┌───────────▼───────────┐
                             │  Volume Mount /config │
                             │  (SQLite DB & Keys)   │
                             └───────────────────────┘
```

---

## Quick Start

### 1. Docker Run (SQLite Default)

```bash
docker run -d \
  --name hishtory-server \
  -p 8080:8080 \
  -v $(pwd)/config:/config \
  -e PUID=1000 \
  -e PGID=1000 \
  -e TZ=UTC \
  -e MODE=all \
  -e HISHTORY_SECRET_KEY="your_hishtory_secret_key" \
  -e WEB_USER=admin \
  -e WEB_PASSWORD="your_secure_web_password" \
  --restart unless-stopped \
  ghcr.io/your-org/hishtory-server:latest
```

### 2. Docker Compose (Recommended)

Save the following as `docker-compose.yml`:

```yaml
services:
  hishtory:
    image: ghcr.io/your-org/hishtory-server:latest
    container_name: hishtory-server
    restart: unless-stopped
    ports:
      - "8080:8080"
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=UTC
      - MODE=all
      - HISHTORY_SECRET_KEY=${HISHTORY_SECRET_KEY:-}
      - WEB_USER=${WEB_USER:-admin}
      - WEB_PASSWORD=${WEB_PASSWORD:-}
      - WEB_PASSWORD_HASH=${WEB_PASSWORD_HASH:-}
    volumes:
      - ./config:/config
    healthcheck:
      test: ["CMD", "/healthcheck.sh"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 15s
```

Run:
```bash
docker compose up -d
```

---

## Connecting Your Shells & Clients

Once the container is running and accessible (e.g. at `http://your-server-ip:8080` or `https://history.example.com`):

### 1. Configure the Server URL
Add this line to your `~/.bashrc`, `~/.zshrc`, or `~/.config/fish/config.fish`:
```bash
export HISHTORY_SERVER="https://history.example.com"
```

### 2. Initialize the Client
- **If linking an existing secret key / account:**
  ```bash
  hishtory init "your_secret_key_here"
  ```
- **If starting fresh:**
  ```bash
  hishtory init
  ```
  *Copy the secret key printed in the terminal and add it to your container `.env` as `HISHTORY_SECRET_KEY` so the Web UI can explore your history.*

### 3. Verify Connection
```bash
hishtory status
```

---

## Docker Secrets & Pre-Hashed Passwords

### Using Docker Secrets / `_FILE` Variables

The container automatically reads any secret file when given `<VAR>_FILE` or mounted to `/run/secrets/`:

```yaml
services:
  hishtory:
    image: ghcr.io/your-org/hishtory-server:latest
    environment:
      - HISHTORY_SECRET_KEY_FILE=/run/secrets/hishtory_key
      - WEB_USER=admin
      - WEB_PASSWORD_FILE=/run/secrets/web_pass
    secrets:
      - hishtory_key
      - web_pass

secrets:
  hishtory_key:
    file: ./secrets/hishtory_key.txt
  web_pass:
    file: ./secrets/web_pass.txt
```

### Using Pre-Hashed Passwords (`WEB_PASSWORD_HASH`)

To avoid passing plaintext passwords in environment variables, supply an Apache/Nginx bcrypt hash:

```bash
# Generate a bcrypt hash using htpasswd or openssl
htpasswd -bnBC 12 "" "YourSecretPassword" | tr -d ':\n'
# Example output: $2y$12$e8d...
```

Set the generated hash in `.env`:
```ini
WEB_USER=admin
WEB_PASSWORD_HASH=$2y$12$e8d...
```

---

## Environment Variables Reference

| Variable | Default | Description |
| :--- | :--- | :--- |
| `PORT` | `8080` | External public listening port for Nginx |
| `PUID` / `PGID` | `1000` / `1000` | User and Group ID for file permission management |
| `TZ` | `UTC` | Timezone (e.g. `America/New_York`) |
| `MODE` | `all` | Operating mode: `all` (Ingress + Web), `ingress` (API only), or `web` (UI only) |
| `HISHTORY_SECRET_KEY` | *(empty)* | Secret key for history encryption and Web UI linking (supports `_FILE`) |
| `WEB_USER` | `admin` | Username for Web UI Basic Auth |
| `WEB_PASSWORD` | *(auto-generated)* | Plaintext password for Web UI (automatically hashed to bcrypt) |
| `WEB_PASSWORD_HASH` | *(empty)* | Pre-computed bcrypt/SHA hash for Web UI (bypasses plaintext) |
| `HISHTORY_SQLITE_DB` | `/config/hishtory.db` | Path to SQLite database file |
| `HISHTORY_POSTGRES_DB` | *(empty)* | PostgreSQL connection URI (`postgresql://user:pass@host:5432/db`) |

---

## Reverse Proxy Setup (HTTPS / SSL)

When exposing your container to the internet, terminate SSL using Caddy, Nginx, or Traefik:

### Caddy Example
```caddy
history.example.com {
    reverse_proxy localhost:8080
}
```

### Nginx Reverse Proxy
```nginx
server {
    listen 443 ssl http2;
    server_name history.example.com;

    ssl_certificate /etc/letsencrypt/live/history.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/history.example.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## Database Backup & Maintenance

To create a timestamped backup archive of your SQLite database and configuration:

```bash
bash scripts/backup-db.sh
```
Backups are saved to `./backups/hishtory_backup_YYYYMMDD_HHMMSS.tar.gz`.

---

## Building Locally

```bash
# Build container image
docker build -t hishtory-server:local .

# Run local smoke tests
bash scripts/test-local.sh
```

---

## License

This project is licensed under the **Apache-2.0 License**. See [LICENSE](LICENSE) for details.
Upstream hiSHtory is developed by [David Dworken](https://github.com/ddworken/hishtory).
