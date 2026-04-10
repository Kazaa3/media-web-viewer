#!/bin/bash
# fast_build_deb.sh - Rapid Debian package build skipping test gates.
# Usage: ./scripts/fast_build_deb.sh
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
VERSION=$(tr -d '[:space:]' < "$ROOT_DIR/VERSION")

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "📦 [Fast Build] Media Web Viewer v${VERSION} Debian Package"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. Synchronize Version Metadata (v1.41.00)
echo "🔄 Synchronizing project version metadata..."
VERSION=$(tr -d '[:space:]' < "$ROOT_DIR/VERSION")
python3 "$ROOT_DIR/scripts/update_version.py" --new-version "$VERSION"

# Set environment for build_deb.sh
export SKIP_BUILD_TESTS=1

# Run the central build script
echo "⚙️ Running infra/build_deb.sh (skipping test gate)..."
bash "$ROOT_DIR/infra/build_deb.sh"

echo ""
echo "✅ Fast Debian Build Complete!"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
