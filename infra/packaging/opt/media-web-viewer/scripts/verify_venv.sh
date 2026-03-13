#!/bin/bash
# Verify the application in a clean virtual environment

set -e

PROJECT_ROOT=$(pwd)
VENV_DIR="/tmp/test_media_viewer_venv"

echo "=== Creating clean venv in $VENV_DIR ==="
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

echo "=== Installing dependencies ==="
pip install --upgrade pip
pip install -r requirements.txt

echo "=== Running Environment Tests ==="
PYTHONPATH="$PROJECT_ROOT" pytest tests/test_environment_dependencies.py -v

echo "=== Running Media Category Tests ==="
PYTHONPATH="$PROJECT_ROOT" pytest tests/test_media_categories.py -v

echo "=== Cleanup ==="
# Deactivate and optionally remove
# deactivate
# rm -rf "$VENV_DIR"

echo "=== Verification Complete! ==="
