#!/bin/bash
# build_exe.sh – Baut eine standalone Windows/Linux EXE für Media Web Viewer
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VERSION=$(tr -d '[:space:]' < "$ROOT_DIR/VERSION")
BUILD_DIR="$ROOT_DIR/build"
DIST_DIR="$ROOT_DIR/dist"

echo "==> Building Media Web Viewer v${VERSION} Executable..."
mkdir -p "$BUILD_DIR"

# Activate virtual environment if it exists
if [ -d "$ROOT_DIR/.venv_build" ]; then
    source "$ROOT_DIR/.venv_build/bin/activate"
fi

# Install/upgrade PyInstaller
pip install --upgrade pyinstaller

# Clean previous builds in local dir to avoid PyInstaller confusion
rm -rf "$SCRIPT_DIR/build" "$SCRIPT_DIR/dist"

# Build using PyInstaller
echo "==> Creating executable with PyInstaller (Zero-Leak)..."
cd "$ROOT_DIR"

# We use the build_system's preferred way or manual eel command
# to ensure web assets are included correctly.
python -m eel src/core/main.py web \
    --onefile \
    --noconsole \
    --name "MediaWebViewer-${VERSION}" \
    --clean \
    --workpath "$BUILD_DIR/pyinstaller_work" \
    --distpath "$BUILD_DIR"

# Verify build
if [ -f "$BUILD_DIR/MediaWebViewer-${VERSION}" ] || [ -f "$BUILD_DIR/MediaWebViewer-${VERSION}.exe" ]; then
    echo "==> ✅ Build successful!"
    echo "Artifact in: $BUILD_DIR"
    ls -lh "$BUILD_DIR/MediaWebViewer-${VERSION}"*
else
    echo "==> ❌ Build failed!"
    exit 1
fi
