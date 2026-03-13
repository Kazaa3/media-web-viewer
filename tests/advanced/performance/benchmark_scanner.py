#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Advanced / Performance
# Eingabewerte: Media directory path
# Ausgabewerte: Scan duration, Extraction performance per item
# Testdateien: src/core/main.py, src/core/models.py
# Kommentar: Benchmark für Scanner-Geschwindigkeit und Metadaten-Extraktion.

import time
import os
from pathlib import Path
from src.core.main import scan_media
from src.core.models import MediaItem

def run_benchmark():
    media_dir = Path("/home/xc/#Coding/gui_media_web_viewer/media")
    if not media_dir.exists():
        print("Media directory not found for benchmark.")
        return

    print("=== Scanner Benchmark ===")
    
    # Measure Scan Time
    start_scan = time.perf_counter()
    items = scan_media(str(media_dir))
    end_scan = time.perf_counter()
    
    scan_duration = end_scan - start_scan
    print(f"Total items found: {len(items)}")
    print(f"Scan duration: {scan_duration:.4f} seconds")
    if len(items) > 0:
        print(f"Average time per item (scan): {scan_duration/len(items):.6f} seconds")

    # Measure Extraction Time for specific types
    print("\n=== Extraction Performance (Top 5 largest) ===")
    # Sort items by file size if possible
    items_with_size = []
    for item in items:
        p = Path(item['path'])
        if p.exists():
            items_with_size.append((item, p.stat().st_size))
    
    items_with_size.sort(key=lambda x: x[1], reverse=True)
    
    for i, (item_dict, size) in enumerate(items_with_size[:5]):
        p = Path(item_dict['path'])
        start_ext = time.perf_counter()
        # Re-parse to measure
        MediaItem(p.name, str(p))
        end_ext = time.perf_counter()
        
        size_mb = size / (1024*1024)
        print(f"[{i+1}] {p.name} ({size_mb:.2f} MB): {end_ext - start_ext:.4f} seconds")

if __name__ == "__main__":
    run_benchmark()
