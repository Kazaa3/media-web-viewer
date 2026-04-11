#!/bin/bash
# headless_audit_v135.sh: Headless DOM Integrity Audit for Media Viewer v1.35 (Expanded)
# Requires: google-chrome (headless), backend running at http://localhost:8345/app.html

CHROME_BIN="/usr/bin/google-chrome"
APP_URL="http://localhost:8345/app.html"
TMP_DOM="/tmp/dom_dump_$$.html"

if [ ! -x "$CHROME_BIN" ]; then
  echo "ERROR: google-chrome not found at $CHROME_BIN."
  exit 1
fi

echo "Waiting 8 seconds for app to render..."
sleep 8

# Dump the DOM
$CHROME_BIN --headless --disable-gpu --dump-dom "$APP_URL" > "$TMP_DOM"

# Check for key nodes and content
QUEUE_NODE=$(grep -c 'id="player-view-warteschlange"' "$TMP_DOM")
LIB_NODE=$(grep -c 'id="lib-split-container"' "$TMP_DOM")
MEDIA_ITEMS=$(grep -c 'class="media-item-card"' "$TMP_DOM")
TEST_MP4=$(grep -c 'Test MP4 Video' "$TMP_DOM")
PILL_PLAYLIST=$(grep -c 'Playlist Manager' "$TMP_DOM")
PILL_CINEMA=$(grep -c 'Video Cinema' "$TMP_DOM")

# Report
echo "--- Headless DOM Audit Report (v1.35) ---"
echo "player-view-warteschlange node:   $QUEUE_NODE found"
echo "lib-split-container node:         $LIB_NODE found"
echo "media-item-card elements:         $MEDIA_ITEMS found"
echo "'Test MP4 Video' string:          $TEST_MP4 found"
echo "'Playlist Manager' pill:          $PILL_PLAYLIST found"
echo "'Video Cinema' pill:              $PILL_CINEMA found"

if [ "$MEDIA_ITEMS" -gt 0 ] && [ "$TEST_MP4" -gt 0 ]; then
  echo "SUCCESS: Media items and test video are present in the DOM. End-to-end data flow confirmed."
else
  echo "WARNING: Media items or test video missing. UI may be empty or broken."
fi

# Clean up
test -f "$TMP_DOM" && rm "$TMP_DOM"
