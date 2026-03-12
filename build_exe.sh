#!/bin/bash
# build_exe.sh – Baut eine standalone Windows/Linux EXE für Media Web Viewer
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
VERSION=$(tr -d '[:space:]' < "$SCRIPT_DIR/VERSION")

echo "==> Building Media Web Viewer v${VERSION} Executable..."

# Activate virtual environment if it exists
if [ -d "$SCRIPT_DIR/.venv_build" ]; then
    source "$SCRIPT_DIR/.venv_build/bin/activate"
fi

# Install/upgrade PyInstaller
pip install --upgrade pyinstaller

# Clean previous builds
rm -rf "$SCRIPT_DIR/build" "$SCRIPT_DIR/dist"

# Build using PyInstaller with the spec file
if [ -f "$SCRIPT_DIR/MediaWebViewer.spec" ]; then
    echo "==> Using existing MediaWebViewer.spec..."
    python -m PyInstaller MediaWebViewer.spec --clean
else
    echo "==> Creating executable with PyInstaller..."
    EEL_PATH=$(python -c "import eel; import os; print(os.path.dirname(eel.__file__))")
    python -m PyInstaller \
        --onefile \
        --noconsole \
        --name "MediaWebViewer-${VERSION}" \
        --add-data "${EEL_PATH}/eel.js:eel" \
        --add-data "web:web" \
        --hidden-import bottle_websocket \
        --hidden-import gevent \
        --hidden-import gevent.monkey \
        main.py
fi

# Verify build
if [ -f "$SCRIPT_DIR/dist/MediaWebViewer" ] || [ -f "$SCRIPT_DIR/dist/MediaWebViewer.exe" ]; then
    echo "==> ✅ Build successful!"
    ls -lh "$SCRIPT_DIR/dist/"
else
    echo "==> ❌ Build failed!"
    exit 1
fi
