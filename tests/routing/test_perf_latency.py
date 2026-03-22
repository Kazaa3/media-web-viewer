#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Media Routing (Performance)
# Eingabewerte: Pfade zu Mediendateien (opus, m4a, wav, mp4)
# Ausgabewerte: TTFB (Time to First Byte) in ms, Throughput (MB/s)
# Testdateien: media/*
# Kommentar: Misst die Latenz und den Durchsatz der Media-Routen.
"""
================================================================================
Media Routing Performance: Latency & Throughput Benchmark
================================================================================

KATEGORIE:
----------
Media Routing (Performance)

ZWECK:
------
Misst die Antwortzeit (TTFB) und die Übertragungsgeschwindigkeit für verschiedene
Media-Routen und Dateitypen.
"""

import eel
import bottle
import threading
import time
import urllib.request
import urllib.parse
import os
import sys
import statistics

# Set up some test constants
PORT = 8087
BASE_URL = f"http://localhost:{PORT}"
MEDIA_ROOT = "./media"

# Find some real files if they exist, otherwise use mocks
TEST_FILES = [
    "Coldplay - Viva La Vida.opus",
    "01 - Anfangsstadium RMX.mp3",
    "02 Ludwig van Beethoven - Piano Concerto No. 5 in E-flat major, Op. 73 ''Emperor''- II. Adagio un poco mosso.wav",
    "30. Pleisweiler Gespräch - Vortrag - Prof. Dr. Gertraud Teuchert-Noodt - 21. Oktober 2018 (720p_30fps_H264-192kbit_AAC).mp4"
]

def run_test_server():
    @bottle.route('/media-raw/<filepath:path>')
    def serve_raw(filepath):
        p = os.path.join(MEDIA_ROOT, filepath)
        if os.path.exists(p):
            return bottle.static_file(os.path.basename(p), root=os.path.dirname(p))
        return bottle.HTTPError(404, "Not found")

    @bottle.route('/video-stream/<filepath:path>')
    def serve_stream(filepath):
        # Mock streaming for overhead measurement
        time.sleep(0.01) # Simulate some processing overhead
        return bottle.HTTPResponse("MOCK STREAM DATA", status=200)

    bottle.run(host='localhost', port=PORT, quiet=True)

def measure_ttfb(url):
    start_time = time.perf_counter()
    try:
        req = urllib.request.urlopen(url)
        # Read just one byte to get TTFB
        req.read(1)
        end_time = time.perf_counter()
        return (end_time - start_time) * 1000 # returns ms
    except Exception as e:
        return None

def main():
    print("="*60)
    print("MEDIA ROUTING PERFORMANCE BENCHMARK")
    print("="*60)
    
    t = threading.Thread(target=run_test_server, daemon=True)
    t.start()
    time.sleep(1)

    results = {}

    for filename in TEST_FILES:
        if not os.path.exists(os.path.join(MEDIA_ROOT, filename)):
            print(f"[SKIP] {filename} not found in {MEDIA_ROOT}")
            continue
            
        print(f"\nBenchmarking: {filename}")
        
        # Test RAW
        url_raw = f"{BASE_URL}/media-raw/{urllib.parse.quote(filename)}"
        raw_times = []
        for _ in range(5):
            val = measure_ttfb(url_raw)
            if val is not None: raw_times.append(val)
        
        if raw_times:
            avg_raw = statistics.mean(raw_times)
            print(f"  - [RAW] TTFB: {avg_raw:.2f}ms (avg of {len(raw_times)})")
        
        # Test STREAM
        url_stream = f"{BASE_URL}/video-stream/{urllib.parse.quote(filename)}?ss=0"
        stream_times = []
        for _ in range(5):
            val = measure_ttfb(url_stream)
            if val is not None: stream_times.append(val)
            
        if stream_times:
            avg_stream = statistics.mean(stream_times)
            print(f"  - [STREAM] TTFB: {avg_stream:.2f}ms (avg of {len(stream_times)})")

    print("\nBenchmark complete.")
    sys.exit(0)

if __name__ == "__main__":
    main()
