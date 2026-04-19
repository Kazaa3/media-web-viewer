#!/bin/bash
# reboot_mwv.sh - Atomic Clear and Reboot
# (v1.35.55)

# Dynamic Path Discovery (v1.46.132)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
SCRIPTS_DIR="$PROJECT_ROOT/scripts"
PYTHON_BIN=$(which python3.14 || which python3 || which python)
MAIN_PY="$PROJECT_ROOT/src/core/main.py"

cd "$PROJECT_ROOT" || exit

echo "[Reboot] Executing Cleanup..."
bash "$SCRIPTS_DIR/cleanup_mwv.sh"

echo "[Reboot] Starting MWV Frontend..."
# Detach with nohup to ensure it survives the parent's exit
nohup "$PYTHON_BIN" "$MAIN_PY" > /dev/null 2>&1 &

echo "[Reboot] Launch sequence complete. PID: $!"
exit 0
