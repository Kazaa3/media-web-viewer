#!/bin/bash
# fast_build_exe.sh - Rapid PyInstaller build using the root spec file.
# Usage: ./scripts/fast_build_exe.sh
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VERSION=$(tr -d '[:space:]' < "$ROOT_DIR/VERSION")

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🚀 [Fast Build] Media Web Viewer v${VERSION} Executable"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Activate build environment
if [ -d "$ROOT_DIR/.venv_build" ]; then
    echo "📦 Activating .venv_build..."
    source "$ROOT_DIR/.venv_build/bin/activate"
fi

# Ensure requirements for build
echo "⚙️ Checking build dependencies..."
pip install --upgrade pyinstaller eel bottle-websocket > /dev/null

# Build using the spec file
cd "$ROOT_DIR"
echo "🛠️  Running PyInstaller with MediaWebViewer.spec..."
pyinstaller --clean MediaWebViewer.spec

echo ""
echo "✅ Build Process Complete!"
echo "📍 Artifacts in: $ROOT_DIR/dist/"
ls -lh "$ROOT_DIR/dist/MediaWebViewer-${VERSION}"* 2>/dev/null || echo "⚠️  No output found in dist/ (check PyInstaller logs)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
