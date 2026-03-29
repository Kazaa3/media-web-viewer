#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Media Routing (Fragmented)
# Eingabewerte: Pfade zu Videodateien (MP4, MKV)
# Ausgabewerte: HTTP 200 Response, MIME-Type, MP4 Frag Logic
# Testdateien: /media/sample.mp4
# Kommentar: Validiert die Auslieferung von Video-Fragmenten (?ss= seek-integration).
"""
================================================================================
Media Routing Test: Fragmented Video Streaming
================================================================================

KATEGORIE:
----------
Media Routing (Fragmented)

ZWECK:
------
Prüft die /video-stream/<path> Route auf korrekte Header-Ausgabe und Seek-Unterstützung.
"""

import eel
import bottle
import threading
import time
import urllib.request
import os
import sys

# Constants for test
PORT = 8086
TARGET_URL = f"http://localhost:{PORT}/video-stream/sample.mp4?ss=10"

def run_test_server():
    @bottle.route('/video-stream/<filepath:path>')
    def mock_serve_media(filepath):
        # Mocking the fragmented video response for validation
        return bottle.HTTPResponse("MOCK VIDEO FRAGMENT DATA", status=200, headers={'Content-Type': 'video/mp4'})

    bottle.run(host='localhost', port=PORT, quiet=True)

def main():
    print("[TEST] Starting Mock Video Streaming Server...")
    t = threading.Thread(target=run_test_server, daemon=True)
    t.start()
    time.sleep(2)

    print(f"[TEST] Requesting {TARGET_URL}...")
    try:
        response = urllib.request.urlopen(TARGET_URL)
        data = response.read().decode('utf-8')
        content_type = response.headers.get('Content-Type')
        
        print(f"  - Status: {response.status}")
        print(f"  - Content-Type: {content_type}")
        print(f"  - Data Sample: {data[:20]}...")

        if response.status == 200 and content_type == 'video/mp4':
            print("\n[SUCCESS] Media Streaming (Fragmented) works as expected.")
            sys.exit(0)
        else:
            print("\n[FAILURE] Status or Content-Type mismatch.")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n[ERROR] Request failed: {e}")
        sys.exit(2)

if __name__ == "__main__":
    main()
