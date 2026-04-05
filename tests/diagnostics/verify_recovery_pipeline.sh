#!/bin/bash
# verify_recovery_pipeline.sh
# Audits the boot sequence and data handshake for Media Viewer v1.35.

LOG_FILE="logs/app.log"
echo "=== Media Viewer Pipeline Audit (v1.35) ==="

# 1. Check Boot Watchdog
echo -n "[1/4] Boot Watchdog Check... "
grep -q "BOOT-WATCHDOG" "$LOG_FILE"
if [ $? -eq 0 ]; then
    echo "OK"
else
    echo "FAIL (UI boot sequence stalled or tracing disabled)"
fi

# 2. Check Data Handshake (Backend to Frontend)
echo -n "[2/4] Backend-to-Frontend Handshake... "
grep -q "BACKEND-RAW" "$LOG_FILE"
if [ $? -eq 0 ]; then
    echo "OK"
else
    echo "FAIL (Data stalled in the Eel bridge)"
fi

# 3. Check Mock Injection (Recovery Mode)
echo -n "[3/4] Recovery Mock Injection... "
grep -q "STAGE-MOCK" "$LOG_FILE"
if [ $? -eq 0 ]; then
    echo "OK"
else
    echo "FAIL (Mock fallback ignored or real data found)"
fi

# 4. Check UI Projection (Filters)
echo -n "[4/4] UI Projection Success... "
grep -q "STAGE-PROJECTED" "$LOG_FILE"
if [ $? -eq 0 ]; then
    echo "OK"
else
    echo "FAIL (Items filtered out or render crash)"
fi

echo "Detailed log results can be found in: $LOG_FILE"
