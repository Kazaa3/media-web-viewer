
import os
import sys
import time
import requests
import subprocess
import logging
import re
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parents[1]
sys.path.append(str(PROJECT_ROOT))

# Setup logging
logging.basicConfig(level=logging.INFO)

from src.core.main import stream_to_mediamtx, resolve_media_path

def run_mtx_test():
    print("--- DVD MTX (MEDIA MTX) TEST SUITE ---")
    
    # 1. Start Server Health Check (Simple listener probe)
    try:
        # Check HLS listener
        requests.get("http://localhost:8888", timeout=2)
        print("✅ [HEALTH] MediaMTX HLS Listener found on :8888.")
    except Exception:
        print("❌ [HEALTH] MediaMTX HLS Listener not reachable. Is MediaMTX running?")
        return False

    # 2. Test Media Item
    test_item = "TestMovie (2024) DVD"
    safe_name = re.sub(r'[^a-zA-Z0-9]', '_', Path(test_item).stem)
    
    print(f"\n[TEST 1] Mode: MTX HLS for: {test_item}")
    res_hls = stream_to_mediamtx(test_item, protocol="hls")
    print(f"       Result: {res_hls}")
    
    if res_hls.get("status") == "play":
        manifest_url = res_hls.get("path")
        print(f"✅ [SUCCESS] HLS Setup OK. URL: {manifest_url}")
        
        # Poll for manifest
        print("         Polling for HLS manifest (this may take 5-10s)...")
        found = False
        for i in range(15):
             time.sleep(1)
             try:
                 r = requests.get(manifest_url, timeout=2)
                 if r.status_code == 200:
                     print(f"✅ [VERIFY] HLS Manifest active! Content Length: {len(r.text)}")
                     found = True
                     break
             except:
                 pass
        if not found:
             print("❌ [VERIFY] HLS Stream timed out (FFmpeg might have failed or DVD path invalid).")
             # Try to see if mediamtx logs anything or ffmpeg is alive
    else:
        print(f"❌ [FAILURE] HLS Setup failed: {res_hls.get('error')}")
        return False

    # 3. Test WebRTC
    print(f"\n[TEST 2] Mode: MTX WEBRTC for: {test_item}")
    res_rtc = stream_to_mediamtx(test_item, protocol="webrtc")
    print(f"       Result: {res_rtc}")
    
    if res_rtc.get("status") == "play":
        print(f"✅ [SUCCESS] WebRTC Setup OK. Endpoint: {res_rtc.get('path')}")
        # WebRTC manifest check is similar
        try:
            r = requests.get(res_rtc.get("path"), timeout=2)
            if r.status_code in [200, 404, 405]: # 405 because WHEP expects POST, but 200/404/405 means listener is there
                print(f"✅ [VERIFY] WebRTC (WHEP) Endpoint reachable.")
        except Exception as e:
            print(f"❌ [VERIFY] WebRTC Endpoint unreachable: {e}")
    else:
        print(f"❌ [FAILURE] WebRTC Setup failed: {res_rtc.get('error')}")
        return False

    print("\n--- MTX DVD TEST COMPLETED ---")
    return True

if __name__ == "__main__":
    success = run_mtx_test()
    sys.exit(0 if success else 1)
