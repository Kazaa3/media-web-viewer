#!/bin/bash
# headless_dom_audit.sh: Headless DOM Integrity Audit for Media Viewer v1.35
# Requires: google-chrome (headless), backend running at http://localhost:8345/app.html

CHROME_BIN="/usr/bin/google-chrome"
APP_URL="http://localhost:8345/app.html"
TMP_DOM="/tmp/dom_dump_$$.html"

if [ ! -x "$CHROME_BIN" ]; then
  echo "ERROR: google-chrome not found at $CHROME_BIN."
  exit 1
fi

echo "Waiting 5 seconds for app to render..."
sleep 5

# Dump the DOM
$CHROME_BIN --headless --disable-gpu --dump-dom "$APP_URL" > "$TMP_DOM"

# Check for key nodes and content
QUEUE_NODE=$(grep -c 'id="player-view-warteschlange"' "$TMP_DOM")
LIB_NODE=$(grep -c 'id="lib-split-container"' "$TMP_DOM")
MEDIA_ITEMS=$(grep -c 'class="media-item-card"' "$TMP_DOM")

# Report
echo "--- Headless DOM Audit Report ---"
echo "player-view-warteschlange node:   $QUEUE_NODE found"
echo "lib-split-container node:         $LIB_NODE found"
echo "media-item-card elements:         $MEDIA_ITEMS found"

if [ "$MEDIA_ITEMS" -eq 0 ]; then
  echo "WARNING: No media items rendered. UI may be empty."
else
  echo "SUCCESS: Media items are present in the DOM."
fi

# Clean up
test -f "$TMP_DOM" && rm "$TMP_DOM"
