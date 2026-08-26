#!/usr/bin/env bash
# ==============================================================================
# hiSHtory Client Pairing & Setup Helper
# Prints instructions and commands to configure client shells
# ==============================================================================

set -euo pipefail

SERVER_URL="${1:-http://localhost:8080}"
SECRET_KEY="${2:-}"

echo "================================================================================"
echo "                   hiSHtory Self-Hosted Client Setup Helper                     "
echo "================================================================================"
echo ""
echo "To connect your local terminal / shell (Bash, Zsh, Fish) to your self-hosted"
echo "hiSHtory server instance, run the following commands:"
echo ""
echo "1. Set the HISHTORY_SERVER environment variable:"
echo "   export HISHTORY_SERVER=\"${SERVER_URL}\""
echo "   (Add this line to your ~/.bashrc, ~/.zshrc, or config.fish to make it permanent)"
echo ""
if [ -n "${SECRET_KEY}" ]; then
    echo "2. Initialize your client using your existing Secret Key / Token:"
    echo "   hishtory init \"${SECRET_KEY}\""
else
    echo "2. Initialize a new client installation:"
    echo "   hishtory init"
    echo ""
    echo "   * Save the generated Secret Key printed by hishtory init! You will need it"
    echo "     to set HISHTORY_SECRET_KEY in your container .env or to link other devices."
fi
echo ""
echo "3. Verify your connection to the server:"
echo "   hishtory status"
echo ""
echo "================================================================================"
