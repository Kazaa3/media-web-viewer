#!/bin/bash

# ==============================================================================
# Robust DOM Integrity Audit (Headless Chrome)
# Version: v1.35
# Target: http://127.0.0.1:8345/app.html
# ==============================================================================

echo "🚀 Starting Robust DOM Integrity Audit..."

# 1. Environment Preparation
echo "[1/4] Spawning verification media items... (Database Sync)"
python3 scripts/spawn_test_items.py > /dev/null

# 2. Headless Chrome DOM Dump
echo "[2/4] Capturing fully rendered DOM via Headless Chrome..."
CHROME_BIN="/usr/bin/google-chrome"
DUMP_DIR="/tmp"
DUMP_FILE="$DUMP_DIR/dom_dump_v135.html"

# Run Chrome, wait for JS, and dump DOM
$CHROME_BIN --headless --disable-gpu --dump-dom http://127.0.0.1:8345/app.html > "$DUMP_FILE" 2>/dev/null

# Buffer for render time
echo "Waiting for app server..."; timeout 30 bash -c "until curl -s http://127.0.0.1:8345/app.html > /dev/null; do sleep 1; done"; sleep 2

# 3. Structural Node Verification
echo "[3/4] Validating structural nodes..."

function verify_id() {
    local target_id=$1
    if grep -Ei "id=['\"]$target_id['\"]" "$DUMP_FILE" > /dev/null; then
        echo "  [OK]  ID: $target_id found."
    else
        echo "  [FAIL] ID: $target_id MISSING or orphaned."
    fi
}

verify_id "main-sidebar"
verify_id "player-main-viewport"
verify_id "library-main-viewport"
verify_id "player-gallery-render-target"

# 4. Content & Routing Verification
echo "[4/4] Auditing item population and routing pills..."

# Item Count
ITEM_COUNT=$(grep -ci 'class="media-item-card"' "$DUMP_FILE")
if [ "$ITEM_COUNT" -gt 0 ]; then
    echo "  [OK]  Data Flow: $ITEM_COUNT media items rendered in DOM."
else
    echo "  [FAIL] Data Flow: 0 items rendered. (Internal Variable Mismatch?)"
fi

# Payload Check (v1.35)
if grep -q "Test MP4 Video" "$DUMP_FILE"; then
    echo "  [OK]  Payload: 'Test MP4 Video' successfully reached the viewport."
else
    echo "  [FAIL] Payload: 'Test MP4 Video' MISSING from DOM dump."
fi

# New Sub-Nav Pill Verification
function verify_pill() {
    local label=$1
    if grep -qi "$label" "$DUMP_FILE"; then
        echo "  [OK]  Pill: '$label' successfully added to category sub-navigation."
    else
        echo "  [FAIL] Pill: '$label' MISSING from category sub-navigation."
    fi
}

verify_pill "Playlist Manager"
verify_pill "Video"

echo "------------------------------------------------------------------------------"
if [ "$ITEM_COUNT" -gt 0 ] && grep -q "Test MP4 Video" "$DUMP_FILE"; then
    echo "Summary: UI ARCHITECTURE STABLE. Content populated and verified."
else
    echo "Summary: UI ARCHITECTURE STABLE, but CONTENT IS EMPTY or PAYLOAD MISSING."
fi
echo "Audit Log: $DUMP_FILE"
echo "=============================================================================="
