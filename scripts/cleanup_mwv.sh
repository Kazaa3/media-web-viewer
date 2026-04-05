#!/bin/bash
# cleanup_mwv.sh - Robustly terminate all Media Viewer processes

echo "[Cleanup] Stopping all MWV instances..."

# 1. Kill by Port
PIDS=$(lsof -ti :8345)
if [ ! -z "$PIDS" ]; then
    echo "[Cleanup] Killing processes on port 8345: $PIDS"
    echo "$PIDS" | xargs kill -9
fi

# 2. Kill by Name
echo "[Cleanup] Killing all Python main.py processes..."
pkill -9 -f "src/core/main.py" || true

# 3. Kill by Parent/Child relationship
# (Catching any stray gevent/eel workers)
ps -ef | grep "python" | grep "gui_media_web_viewer" | awk '{print $2}' | xargs kill -9 2>/dev/null || true

# 4. KILL TRANSCODER ZOMBIES (FFmpeg / FFplay)
echo "[Cleanup] Cleaning up transcoding/verifier zombies..."
pkill -9 -f "ffplay" || true
pkill -9 -f "ffmpeg" || true

# 5. Wait for OS to release port
sleep 1
echo "[Cleanup] Port status:"
lsof -i :8345 || echo "[Cleanup] Port 8345 is now FREE."

echo "[Cleanup] Done."
