#!/usr/bin/env bash
# ==============================================================================
# hiSHtory Database & Configuration Backup Script
# Creates a timestamped compressed archive of /config or SQLite database
# ==============================================================================

set -euo pipefail

BACKUP_DIR="${BACKUP_DIR:-./backups}"
CONFIG_DIR="${CONFIG_DIR:-./config}"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
ARCHIVE_NAME="hishtory_backup_${TIMESTAMP}.tar.gz"

mkdir -p "${BACKUP_DIR}"

echo "[backup] Creating backup of ${CONFIG_DIR} to ${BACKUP_DIR}/${ARCHIVE_NAME}..."

if [ -d "${CONFIG_DIR}" ]; then
    tar -czf "${BACKUP_DIR}/${ARCHIVE_NAME}" -C "${CONFIG_DIR}" .
    echo "[backup] Successfully generated backup: ${BACKUP_DIR}/${ARCHIVE_NAME} ($(du -h "${BACKUP_DIR}/${ARCHIVE_NAME}" | cut -f1))"
else
    echo "[backup] Error: Configuration directory '${CONFIG_DIR}' not found!"
    exit 1
fi
