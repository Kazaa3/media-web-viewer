#!/usr/bin/env python3
import warnings
# Suppress urllib3 warnings for cleaner output
with warnings.catch_warnings():
    warnings.simplefilter('ignore', category=UserWarning)
import sys
import time
import os
import requests
from pathlib import Path

# Need the port from the running instance
try:
    port_file = Path("src/parsers/.mwv_port")
    if not port_file.exists():
        port_file = Path("src/.mwv_port") # fallback
    if port_file.exists():
        PORT = int(port_file.read_text().strip())
    else:
        # Check running process
        import psutil
        PORT = None
        for conn in psutil.net_connections():
            if conn.pid and conn.laddr and conn.laddr.port > 1000:
                try:
                    p = psutil.Process(conn.pid)
                    if 'main.py' in ' '.join(p.cmdline()):
                        PORT = conn.laddr.port
                        break
                except:
                    pass
        if not PORT:
            PORT = int(os.environ.get("MWV_PORT", 8080))
except Exception as e:
    PORT = 8080

print(f"Connecting to MWV on port {PORT}...")

# Test 1: MP4 Native
print("\n--- Testing Chrome Native Playback (MP4) ---")
test_mp4 = Path("media/test_files/valid_test.mp4").resolve()
try:
    import urllib.request
    import json
    
    # We will simulate the eel call by just importing the function directly for testing
    # but since main is running, we can check the db or directly call eel?
    # Better yet, since we are diagnosing python logic, let's just import the function.
    sys.path.insert(0, str(Path.cwd()))
    from src.core.main import open_video
    
    res = open_video(str(test_mp4), "chrome", "chrome_direct")
    print("MP4 Direct Play:", res)
    assert res['mode'] == 'chrome_native', "Should play natively"
    assert "/media/valid_test.mp4" in res['path'], "Should serve static path"
except Exception as e:
    print("Failed Test 1:", e)

# Test 2: DVD Folder
print("\n--- Testing VLC DVD Folder Fallback ---")
test_dvd = Path("media/test_files/TestMovie (2024) - DVD").resolve()
try:
    res = open_video(str(test_dvd), "vlc", "vlc_iso")
    print("DVD Folder Play:", res)
    assert res['mode'] == 'vlc_external', "Should launch VLC externally"
except Exception as e:
    print("Failed Test 2:", e)

print("\nTests Complete.")

print("\n--- Testing VLC Shutdown ---")
try:
    from src.core.main import stop_vlc
    stop_res = stop_vlc()
    print("VLC Stop:", stop_res)
except Exception as e:
    print("Failed Test 3:", e)
