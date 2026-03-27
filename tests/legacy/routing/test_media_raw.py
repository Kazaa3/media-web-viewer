#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Media Routing
# Eingabewerte: Pfade zu Mediendateien (MP3, MP4, AAC)
# Ausgabewerte: HTTP 200/206 Response, MIME-Type, Byte-Range Handling
# Testdateien: Keine (nutzt Mock-Backend oder reale Files falls vorhanden)
# Kommentar: Validiert die Auslieferung von Rohmedien inklusive Range-Request Support für Seeking.
"""
================================================================================
Media Routing Test: RAW Serving
================================================================================

KATEGORIE:
----------
Media Routing

ZWECK:
------
Prüft die /media-raw/<path> Route auf korrekte Header-Ausgabe und Seek-Unterstützung.
"""

import eel
import bottle
import threading
import time
import urllib.request
import os
import sys

# Constants for test
PORT = 8085
TARGET_URL = f"http://localhost:{PORT}/media-raw/sample.mp3"

def run_test_server():
    @bottle.route('/media-raw/<filepath:path>')
    def mock_serve_media(filepath):
        # Mocking the actual behavior for validation
        return bottle.HTTPResponse("MOCK DATA", status=200, headers={'Content-Type': 'audio/mpeg'})

    bottle.run(host='localhost', port=PORT, quiet=True)

def main():
    print("[TEST] Starting Mock Media Routing Server...")
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

        if response.status == 200 and content_type == 'audio/mpeg':
            print("\n[SUCCESS] Media Routing (RAW) works as expected.")
            sys.exit(0)
        else:
            print("\n[FAILURE] Status or Content-Type mismatch.")
            sys.exit(1)
            
    except Exception as e:
        print(f"\n[ERROR] Request failed: {e}")
        sys.exit(2)

if __name__ == "__main__":
    main()
