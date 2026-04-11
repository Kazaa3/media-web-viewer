#!/usr/bin/env python3
import urllib.request
import urllib.error
import sys
import os
import time
import subprocess
import signal
from pathlib import Path

# Port where the app is expected to run (default 8345)
PORT = 8345
BASE_URL = f"http://localhost:{PORT}"

def check_route(route_name, url_path):
    url = f"{BASE_URL}{url_path}"
    print(f"[TEST] Checking {route_name}: {url}")
    try:
        # Use a HEAD request or a range request for efficiency if possible
        req = urllib.request.Request(url, method='HEAD')
        with urllib.request.urlopen(req) as response:
            print(f"  [PASS] Status: {response.status}")
            print(f"  [PASS] Content-Type: {response.headers.get('Content-Type')}")
            return True
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"  [FAIL] 404 Not Found (Route likely missing or file hidden)")
        else:
            print(f"  [WARN] Unexpected HTTP Error: {e.code}")
    except Exception as e:
        print(f"  [ERROR] Connection failed: {e}")
    return False

def main():
    print("======================================================")
    print("Media Routing Endpoint Suite - Connection Test")
    print("======================================================\n")
    print("Note: This test assumes the main MWV application is RUNNING.")
    print(f"Target: {BASE_URL}\n")
    
    # We test with common paths or placeholders
    # In a real scenario, we would grab a real item path from the DB
    routes = [
        ("RAW Media", "/media-raw/media/sample.mp3"),
        ("Direct Play", "/direct/media/sample.mp4"),
        ("Video Stream", "/video-stream/media/sample.mp4"),
        ("Transcoding", "/transcode/media/sample.mp4")
    ]
    
    all_passed = True
    for name, path in routes:
        if not check_route(name, path):
            all_passed = False
            
    print("\n------------------------------------------------------")
    if all_passed:
        print("[SUCCESS] All routing endpoints reachable.")
    else:
        print("[NOTICE] Some endpoints returned errors. This is expected if the specific sample files don't exist.")
        print("         However, if you see 404 for EVERY route, the server is likely down or routing is broken.")
    print("------------------------------------------------------")

if __name__ == "__main__":
    main()
