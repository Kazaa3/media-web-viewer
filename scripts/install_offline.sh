#!/bin/bash
# Offline Package Installer for MWV
# Usage: ./scripts/install_offline.sh [.venv_path]

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PATH="${1:-$PROJECT_ROOT/.venv_core}"
PACKAGES_DIR="$PROJECT_ROOT/packages"

echo "STDOUT: MWV Offline Installer starting..."
echo "STDOUT: Target Venv: $VENV_PATH"

if [ ! -d "$VENV_PATH" ]; then
    echo "ERROR: Virtual environment not found at $VENV_PATH"
    exit 1
fi

if [ ! -d "$PACKAGES_DIR" ]; then
    echo "ERROR: Offline packages directory not found at $PACKAGES_DIR"
    exit 1
fi

# Activate venv
source "$VENV_PATH/bin/activate"

# Install from local wheel cache
echo "STDOUT: Installing dependencies from local cache..."
pip install --no-index --find-links="$PACKAGES_DIR" -r "$PROJECT_ROOT/requirements.txt"

if [ $? -eq 0 ]; then
    echo "STDOUT: Offline installation completed successfully."
else
    echo "ERROR: Offline installation failed."
    exit 1
fi
