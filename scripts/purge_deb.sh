#!/bin/bash
# purge_deb.sh – Completely remove media-web-viewer package and config.
set -e

PACKAGE_NAME="media-web-viewer"

echo "==> Media Web Viewer: Purge Script"

if dpkg -l | grep -q "^ii.*$PACKAGE_NAME"; then
    echo "🗑️  Purging package $PACKAGE_NAME..."
    sudo apt purge -y "$PACKAGE_NAME"
    echo "🚮 Removing remaining artifacts..."
    sudo rm -rf /opt/media-web-viewer
    echo "✅ Purge complete."
else
    echo "ℹ️  Package $PACKAGE_NAME is not installed. Nothing to do."
fi
