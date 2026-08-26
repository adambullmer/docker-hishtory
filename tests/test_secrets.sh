#!/usr/bin/env bash
# ==============================================================================
# Docker Secrets & Hashed Auth Integration Test
# ==============================================================================

set -euo pipefail

SECRETS_DIR="./tests/scratch_secrets"
CONTAINER_NAME="hishtory-secret-test"
TEST_PORT="18081"
IMAGE_TAG="hishtory-server:test"

mkdir -p "${SECRETS_DIR}"

# 1. Create temporary secret files
echo "secret_user_token_12345" > "${SECRETS_DIR}/hishtory_token.txt"
echo "secret_admin" > "${SECRETS_DIR}/web_user.txt"
# Pre-computed bcrypt hash for 'secretpassword99' ($2b$12$...) or htpasswd format
htpasswd -b -B -c "${SECRETS_DIR}/htpasswd_test" secret_admin secretpassword99
HASH_VAL=$(cut -d: -f2 < "${SECRETS_DIR}/htpasswd_test")
echo "${HASH_VAL}" > "${SECRETS_DIR}/web_pass_hash.txt"

echo "[test-secrets] Starting container with mounted secret files..."
docker run -d \
    --name "${CONTAINER_NAME}" \
    -p "${TEST_PORT}:8080" \
    -v "$(pwd)/${SECRETS_DIR}:/run/secrets:ro" \
    -e HISHTORY_SECRET_KEY_FILE=/run/secrets/hishtory_token.txt \
    -e WEB_USER_FILE=/run/secrets/web_user.txt \
    -e WEB_PASSWORD_HASH_FILE=/run/secrets/web_pass_hash.txt \
    "${IMAGE_TAG}"

echo "[test-secrets] Waiting for container initialization..."
for i in $(seq 1 30); do
    if curl -s -f "http://127.0.0.1:${TEST_PORT}/healthcheck" >/dev/null 2>&1; then
        break
    fi
    sleep 1
done

echo "[test-secrets] Testing authentication against secret-loaded hashed password..."
STATUS_OK=$(curl -s -u secret_admin:secretpassword99 -o /dev/null -w "%{http_code}" "http://127.0.0.1:${TEST_PORT}/")

echo "[test-secrets] Auth with secret password returned HTTP: ${STATUS_OK}"
if [ "${STATUS_OK}" -ne 200 ] && [ "${STATUS_OK}" -ne 302 ] && [ "${STATUS_OK}" -ne 304 ]; then
    echo "[test-secrets] FAILED: Secret authentication test failed!"
    docker logs "${CONTAINER_NAME}"
    docker rm -f "${CONTAINER_NAME}"
    rm -rf "${SECRETS_DIR}"
    exit 1
fi

echo "[test-secrets] Cleaning up..."
docker rm -f "${CONTAINER_NAME}"
rm -rf "${SECRETS_DIR}"

echo "[test-secrets] SUCCESS: Docker secret resolution and hashed auth verified!"
