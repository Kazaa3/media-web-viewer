#!/bin/bash
# install_latest_deb.sh – Robustly find and install the newest .deb package.
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PACKAGE_NAME="media-web-viewer"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📥 [Installer] Media Web Viewer Latest Package"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. Find latest .deb
echo "🔍 Searching for packages in build/ and dist/..."
LATEST_DEB=$(ls -t "$ROOT_DIR"/build/${PACKAGE_NAME}_*.deb "$ROOT_DIR"/dist/${PACKAGE_NAME}_*.deb 2>/dev/null | head -n 1)

if [ -z "$LATEST_DEB" ]; then
    echo "❌ Error: No .deb packages found!"
    echo "   Run ./scripts/fast_build_deb.sh first."
    exit 1
fi

DEB_BASENAME=$(basename "$LATEST_DEB")
echo "📦 Found latest: $DEB_BASENAME"

# 2. Installation logic
echo "⚙️  Installing package..."
# We use sudo for installation
sudo dpkg -i "$LATEST_DEB"

# 3. Dependency fix
echo "🔧 Resolving dependencies..."
sudo apt-get install -f -y

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Installation Success!"
echo "🚀 Run with: media-web-viewer"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
