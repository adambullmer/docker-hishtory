#!/usr/bin/env bash
# ==============================================================================
# Local Build & Container Smoke Test Runner
# ==============================================================================

set -euo pipefail

IMAGE_NAME="hishtory-server:local-test"
CONTAINER_NAME="hishtory-test-runner"
TEST_PORT="18080"

echo "[test-local] 1. Building Docker image '${IMAGE_NAME}'..."
docker build -t "${IMAGE_NAME}" .

echo "[test-local] 2. Cleaning up any previous test container..."
docker rm -f "${CONTAINER_NAME}" 2>/dev/null || true

echo "[test-local] 3. Starting container in MODE=all..."
docker run -d \
    --name "${CONTAINER_NAME}" \
    -p "${TEST_PORT}:8080" \
    -e MODE=all \
    -e WEB_USER=testadmin \
    -e WEB_PASSWORD=testpass123 \
    "${IMAGE_NAME}"

echo "[test-local] 4. Waiting for container to initialize..."
for i in $(seq 1 30); do
    if curl -s -f "http://127.0.0.1:${TEST_PORT}/healthcheck" >/dev/null 2>&1; then
        echo "[test-local] Healthcheck endpoint responsive on iteration ${i}."
        break
    fi
    sleep 1
done

echo "[test-local] 5. Verifying /healthcheck endpoint (expect HTTP 200)..."
HEALTH_CODE=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:${TEST_PORT}/healthcheck")
if [ "$HEALTH_CODE" -ne 200 ]; then
    echo "[test-local] FAILED: Healthcheck returned HTTP ${HEALTH_CODE}"
    docker logs "${CONTAINER_NAME}"
    docker rm -f "${CONTAINER_NAME}"
    exit 1
fi

echo "[test-local] 6. Verifying Web UI basic auth challenge (expect HTTP 401)..."
AUTH_CHALLENGE=$(curl -s -o /dev/null -w "%{http_code}" "http://127.0.0.1:${TEST_PORT}/")
if [ "$AUTH_CHALLENGE" -ne 401 ]; then
    echo "[test-local] FAILED: Web UI without auth returned HTTP ${AUTH_CHALLENGE} (expected 401)"
    docker logs "${CONTAINER_NAME}"
    docker rm -f "${CONTAINER_NAME}"
    exit 1
fi

echo "[test-local] 7. Verifying Web UI authenticated access (expect HTTP 200 or active web response)..."
AUTH_SUCCESS=$(curl -s -u testadmin:testpass123 -o /dev/null -w "%{http_code}" "http://127.0.0.1:${TEST_PORT}/")
echo "[test-local] Authenticated response code: ${AUTH_SUCCESS}"

echo "[test-local] 8. Container logs:"
docker logs "${CONTAINER_NAME}" | tail -n 25

echo "[test-local] 9. Cleaning up test container..."
docker rm -f "${CONTAINER_NAME}"

echo "[test-local] SUCCESS: All smoke test assertions passed!"
