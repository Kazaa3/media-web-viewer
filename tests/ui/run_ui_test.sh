#!/bin/bash
# --- [MWV-UI-TEST-RUNNER] ---
# Runs the playback verification test using the correct venv.

set -e
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../" && pwd)"
VENV_PATH="$PROJECT_ROOT/.venv_selenium"
TEST_SCRIPT="$PROJECT_ROOT/tests/ui/playback_verify.py"

if [ ! -d "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at $VENV_PATH"
    exit 1
fi

echo "[System] Activating $VENV_PATH..."
source "$VENV_PATH/bin/activate"

echo "[System] Running $TEST_SCRIPT..."
python "$TEST_SCRIPT"
