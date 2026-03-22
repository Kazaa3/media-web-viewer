#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Media Routing (Comprehensive)
# Eingabewerte: Alle Dateien im /media Ordner
# Ausgabewerte: Codec-Matrix, Route-Decision (Direct/Transcode), Parsing-Time
# Testdateien: media/*
# Kommentar: Benchmarkt die Routing-Logik für alle verfügbaren Dateiformate.
"""
================================================================================
Media Routing: Multi-Format & Codec Benchmark
================================================================================

KATEGORIE:
----------
Media Routing (Comprehensive)

ZWECK:
------
Analysiert alle Mediendateien im media-Verzeichnis und bewertet die Routing-Effizienz
für verschiedene Codecs und Container.
"""

import os
import sys
import time
import subprocess
import json
from pathlib import Path

MEDIA_ROOT = "./media"

# Define browser support matrix (simplified for benchmark)
BROWSER_NATIVE_SUPPORT = {
    "audio": ["mp3", "aac", "opus", "wav", "flac"],
    "video": ["h264", "vp8", "vp9", "av1"]
}

def get_file_info(filepath):
    """Uses ffprobe to extract codec and container info."""
    start_time = time.perf_counter()
    try:
        cmd = [
            "ffprobe", "-v", "quiet", 
            "-print_format", "json", 
            "-show_format", "-show_streams", 
            filepath
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        data = json.loads(result.stdout)
        
        streams = data.get("streams", [])
        v_codec = next((s["codec_name"] for s in streams if s["codec_type"] == "video"), None)
        a_codec = next((s["codec_name"] for s in streams if s["codec_type"] == "audio"), None)
        container = data.get("format", {}).get("format_name", "unknown")
        
        parse_time = (time.perf_counter() - start_time) * 1000
        return v_codec, a_codec, container, parse_time
    except Exception as e:
        return None, None, None, 0

def decide_route(v_codec, a_codec, container):
    """Simulates the routing logic."""
    if container == "matroska,webm" or container == "webm":
        return "WebM / Fragmented"
    
    if v_codec: # Video file
        if v_codec.startswith("h264") or v_codec == "vp8" or v_codec == "vp9":
            return "Direct (Native Browser)"
        return f"Transcode (to {v_codec} -> h264)"
    
    if a_codec: # Audio file
        if a_codec in BROWSER_NATIVE_SUPPORT["audio"]:
            return "Direct (Native Browser)"
        return f"Transcode (to {a_codec} -> aac/mp3)"
        
    return "Unknown / Logic Fallback"

def main():
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
    log = logging.getLogger("format_router")

    log.info("="*80)
    log.info(f"{'FILE':<40} | {'CODEC (V/A)':<20} | {'ROUTE':<20} | {'TIME'}")
    log.info("-" * 80)
    
    files = [f for f in os.listdir(MEDIA_ROOT) if os.path.isfile(os.path.join(MEDIA_ROOT, f))]
    
    summary = {
        "direct": 0,
        "transcode": 0,
        "total_time": 0.0,
        "count": 0
    }

    for filename in sorted(files):
        if filename.startswith(".") or filename.endswith(".iso") or filename.endswith(".cue") or filename.endswith(".bin"):
            continue
            
        path = os.path.join(MEDIA_ROOT, filename)
        v_codec, a_codec, container, parse_time = get_file_info(path)
        
        if not v_codec and not a_codec:
            log.debug(f"[SKIP] {filename} is not a recognized media file.")
            continue
            
        route = decide_route(v_codec, a_codec, container)
        
        codec_str = f"{v_codec or '-'}/{a_codec or '-'}"
        fn_display = str(filename)[:38]
        log.info(f"{fn_display:<40} | {codec_str:<20} | {route:<20} | {parse_time:.1f}ms")
        
        summary["count"] += 1
        summary["total_time"] += parse_time
        if "Direct" in route: summary["direct"] += 1
        else: summary["transcode"] += 1

    log.info("-" * 80)
    if summary["count"] > 0:
        avg_time = summary["total_time"] / summary["count"]
        log.info(f"TOTAL: {summary['count']} Files | AVG PARSE: {avg_time:.2f}ms")
        log.info(f"CAPABILITY: {summary['direct']} Native / {summary['transcode']} Needs Transcode")
    log.info("="*80)

if __name__ == "__main__":
    main()
