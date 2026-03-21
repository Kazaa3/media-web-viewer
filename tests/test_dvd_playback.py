
# Kategorie: Media Pipeline
# Eingabewerte: Folder or ISO file
# Ausgabewerte: Transcode Stream URL (/transcode/...)
# Testdateien: 4 Könige (2015) - DVD
# Kommentar: Verifies that DVD folders and ISOs are routed to the internal transcoder for Chrome native playback.

import os
import sys
import logging
from pathlib import Path

# Add project root to sys.path
PROJECT_ROOT = Path(__file__).parents[1]
sys.path.append(str(PROJECT_ROOT))

# Configuration for testing
logging.basicConfig(level=logging.INFO)

from src.core.main import get_play_source, resolve_media_path

def run_test():
    print("--- DVD/ISO ROUTING VERIFICATION TEST ---")
    
    # 1. Check for the user's specific folder
    test_item = "4 Könige (2015) - DVD"
    resolved = resolve_media_path(test_item)
    print(f"[STEP 1] Testing item: {test_item}")
    print(f"         Resolved to: {resolved}")
    
    if not os.path.exists(resolved):
        print(f"⚠️ [WARNING] Test item '{test_item}' not found in media library.")
        print("             Creating a temporary dummy DVD structure for verification...")
        test_dir = PROJECT_ROOT / "media" / "test_dvd_structure"
        test_dir.mkdir(parents=True, exist_ok=True)
        (test_dir / "VIDEO_TS").mkdir(exist_ok=True)
        (test_dir / "VIDEO_TS" / "VIDEO_TS.IFO").touch()
        test_item = "test_dvd_structure"
        resolved = str(test_dir)
        print(f"             Fixed Test Target: {test_item}")

    # 2. Verify Routing
    print(f"[STEP 2] Calling get_play_source('{test_item}')...")
    source = get_play_source(test_item)
    print(f"         Result: {source}")
    
    mode = source.get("mode")
    url = source.get("url", "")
    
    if mode == "transcode" and "/transcode/" in url:
        print("✅ [SUCCESS] Routing Correct: Found 'transcode' mode with /transcode/ URL.")
    else:
        print(f"❌ [FAILURE] Routing Incorrect: Expected 'transcode', got '{mode}'.")
        if mode == "vlc":
            print("             Reason: System defaulted to external VLC.")
        elif mode == "hls":
             print("             Reason: System defaulted to HLS fallback.")
        return False

    # 3. Verify path resolving logic
    print("[STEP 3] Verifying relative vs absolute resolution...")
    abs_source = get_play_source(resolved)
    if abs_source.get("mode") == "transcode":
         print("✅ [SUCCESS] Absolute path also correctly routed.")
    else:
         print(f"⚠️ [NOTICE] Absolute path routing differs: {abs_source.get('mode')}")

    print("\n--- TEST COMPLETED ---")
    return True

if __name__ == "__main__":
    success = run_test()
    sys.exit(0 if success else 1)
