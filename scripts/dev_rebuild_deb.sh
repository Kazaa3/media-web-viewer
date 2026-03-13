#!/bin/bash
# dev_rebuild_deb.sh – Build, Purge, and Install for fast iteration.
# Usage: ./scripts/dev_rebuild_deb.sh [--fast]
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

FAST_MODE=false
if [[ "$1" == "--fast" ]]; then
    FAST_MODE=true
fi

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🛠️  [Dev Rebuild] Starting full cycle for Media Web Viewer"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# 1. Build
if [ "$FAST_MODE" = true ]; then
    echo "🏃 Using Fast Build (skipping test gate)..."
    bash "$SCRIPT_DIR/fast_build_deb.sh"
else
    echo "🏗️  Using Standard Build (running test gate)..."
    bash "$ROOT_DIR/infra/build_deb.sh"
fi

# 2. Reinstall (handles purge and install)
echo ""
echo "🔄 Reinstalling..."
bash "$SCRIPT_DIR/reinstall_deb.sh"

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "✅ Dev Rebuild Cycle Complete!"
echo "🚀 Target: media-web-viewer"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
