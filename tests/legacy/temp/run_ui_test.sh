#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../../.." && pwd)"
VENV_DIR="$REPO_ROOT/venv_selenium"
PYTHON_BIN="$VENV_DIR/bin/python"

if [[ ! -x "$PYTHON_BIN" ]]; then
  echo "FAILURE"
  echo "Reason: Python executable not found in venv_selenium: $PYTHON_BIN"
  exit 2
fi

export APP_URL="${APP_URL:-http://localhost:8345}"
export PLAYBACK_VERIFY_HEADLESS="${PLAYBACK_VERIFY_HEADLESS:-0}"
export PLAYBACK_VERIFY_KEEP_OPEN_MS="${PLAYBACK_VERIFY_KEEP_OPEN_MS:-3500}"

exec "$PYTHON_BIN" "$SCRIPT_DIR/playback_verify.py" "$@"
