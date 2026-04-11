#!/bin/bash
# reinstall_deb.sh – Purge old package and install newly built .deb
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
PACKAGE_NAME="media-web-viewer"
VERSION=$(tr -d '[:space:]' < "$ROOT_DIR/VERSION")
ARCH="amd64"
DEB_NAME="${PACKAGE_NAME}_${VERSION}_${ARCH}.deb"
DEB_PATH="$ROOT_DIR/build/$DEB_NAME"

echo "==> Media Web Viewer Reinstall Script"
echo "    Version: $VERSION"
echo "    Package: $DEB_NAME"
echo ""

# Check if .deb file exists
if [ ! -f "$DEB_PATH" ]; then
    echo "❌ Error: $DEB_NAME not found!"
    echo "   Please run ./build_deb.sh first."
    exit 1
fi

# Check if package is currently installed
if dpkg -l | grep -q "^ii.*$PACKAGE_NAME"; then
    echo "📦 Package $PACKAGE_NAME is currently installed."
    echo "🗑️  Purging old package..."
    sudo apt purge -y "$PACKAGE_NAME"
    echo "✅ Old package purged successfully."
    echo ""
else
    echo "ℹ️  Package $PACKAGE_NAME is not currently installed."
    echo ""
fi

# Install new package
echo "📥 Installing new package: $DEB_NAME"
sudo dpkg -i "$DEB_PATH"

# Fix any dependency issues
echo ""
echo "🔧 Fixing dependencies (if needed)..."
sudo apt install -f -y

echo ""
echo "✅ Installation complete!"
echo ""
echo "🚀 You can now run: $PACKAGE_NAME"
echo ""
