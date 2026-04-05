#!/bin/bash
# reboot_mwv.sh - Atomic Clear and Reboot
# (v1.35.55)

PROJECT_ROOT="/home/xc/#Coding/gui_media_web_viewer"
SCRIPTS_DIR="$PROJECT_ROOT/scripts"
PYTHON_BIN="/home/xc/.local/bin/python3.14"
MAIN_PY="$PROJECT_ROOT/src/core/main.py"

cd "$PROJECT_ROOT" || exit

echo "[Reboot] Executing Cleanup..."
bash "$SCRIPTS_DIR/cleanup_mwv.sh"

echo "[Reboot] Starting MWV Frontend..."
# Detach with nohup to ensure it survives the parent's exit
nohup "$PYTHON_BIN" "$MAIN_PY" > /dev/null 2>&1 &

echo "[Reboot] Launch sequence complete. PID: $!"
exit 0
