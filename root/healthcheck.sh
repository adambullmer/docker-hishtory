#!/bin/bash
# ==============================================================================
# Container Healthcheck Script
# Validates Nginx proxy, Ingress backend, and Web UI availability
# ==============================================================================

set -eo pipefail

PORT="${PORT:-8080}"
MODE="${MODE:-all}"

# 1. Check Ingress Healthcheck via Nginx Proxy (expect 200 OK)
if [ "$MODE" = "all" ] || [ "$MODE" = "ingress" ]; then
    HEALTH_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:${PORT}/healthcheck" || echo "000")
    if [ "$HEALTH_STATUS" -ne 200 ]; then
        echo "[healthcheck] Ingress healthcheck failed with HTTP status: $HEALTH_STATUS"
        exit 1
    fi
fi

# 2. Check Web UI Root via Nginx Proxy (expect 200 OK or 401 Unauthorized due to Basic Auth)
if [ "$MODE" = "all" ] || [ "$MODE" = "web" ]; then
    WEB_STATUS=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:${PORT}/" || echo "000")
    if [ "$WEB_STATUS" -ne 200 ] && [ "$WEB_STATUS" -ne 401 ]; then
        echo "[healthcheck] Web UI healthcheck failed with HTTP status: $WEB_STATUS"
        exit 1
    fi
fi

echo "[healthcheck] Container is healthy (Mode: $MODE, Port: $PORT)."
exit 0
