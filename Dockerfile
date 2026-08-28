# syntax=docker/dockerfile:1
# ------------------------------------------------------------------------------
# Build Stage: Compile hishtory-server and hishtory client from upstream Go source
# ------------------------------------------------------------------------------
FROM golang:1.24-alpine AS builder

# Install build dependencies required for CGO (SQLite support)
RUN apk add --no-cache \
    git \
    make \
    gcc \
    musl-dev \
    ca-certificates

# Specify hishtory version tag, commit, or branch (defaults to master)
ARG HISHTORY_VERSION=master

WORKDIR /src

# Clone the official hishtory repository
RUN git clone --depth 1 --branch ${HISHTORY_VERSION} https://github.com/ddworken/hishtory.git . || \
    git clone https://github.com/ddworken/hishtory.git . && git checkout ${HISHTORY_VERSION}

# Download Go modules
RUN go mod download

# Build hishtory backend ingress server binary (located in ./backend/server)
RUN CGO_ENABLED=1 GOOS=linux go build \
    -ldflags="-s -w" \
    -o /out/hishtory-server \
    ./backend/server

# Build hishtory CLI client binary (located at repository root .)
RUN CGO_ENABLED=1 GOOS=linux go build \
    -ldflags="-s -w" \
    -o /out/hishtory \
    .

# ------------------------------------------------------------------------------
# Runtime Stage: LinuxServer.io Alpine base image with S6-Overlay v3
# ------------------------------------------------------------------------------
FROM ghcr.io/linuxserver/baseimage-alpine:3.21

# Container metadata and labels following OCI specification
LABEL maintainer="hishtory-selfhost"
LABEL org.opencontainers.image.title="hishtory-server"
LABEL org.opencontainers.image.description="Unified self-hosted hiSHtory Ingress API & Web Server with Nginx reverse proxy and s6-overlay"
LABEL org.opencontainers.image.licenses="Apache-2.0"
LABEL org.opencontainers.image.source="https://github.com/ddworken/hishtory"

# Install runtime packages (Nginx reverse proxy, htpasswd utility, SQLite, curl)
RUN apk add --no-cache \
    nginx \
    apache2-utils \
    sqlite \
    curl \
    bash \
    ca-certificates \
    tzdata && \
    rm -rf /var/cache/apk/* /tmp/*

# Copy compiled binaries from builder stage
COPY --from=builder /out/hishtory-server /usr/local/bin/hishtory-server
COPY --from=builder /out/hishtory /usr/local/bin/hishtory

# Ensure binaries have executable permissions
RUN chmod +x /usr/local/bin/hishtory-server /usr/local/bin/hishtory

# Copy LinuxServer.io root filesystem overlay (S6-Overlay services, Nginx configs, healthcheck)
COPY root/ /

# Make scripts executable
RUN chmod +x /healthcheck.sh \
    /etc/s6-overlay/s6-rc.d/01-init/up \
    /etc/s6-overlay/s6-rc.d/01-init/run \
    /etc/s6-overlay/s6-rc.d/svc-ingress/run \
    /etc/s6-overlay/s6-rc.d/svc-web/run \
    /etc/s6-overlay/s6-rc.d/svc-nginx/run

# Persistent volume for database, credentials, and client configuration
VOLUME ["/config"]

# Single public port exposed by Nginx reverse proxy
EXPOSE 8080

# Container healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD ["/healthcheck.sh"]
