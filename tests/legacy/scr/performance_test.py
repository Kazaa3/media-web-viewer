#!/usr/bin/env python3
import time
import os
import sys
from pathlib import Path
from typing import List

# Ensure we can import local modules
sys.path.append(os.getcwd())

from models import MediaItem
from parsers.format_utils import PARSER_CONFIG

def run_benchmark(media_files: List[Path]):
    print(f"--- Performance Benchmark ---")
    print(f"Python Version: {sys.version}")
    print(f"Parser Mode: {PARSER_CONFIG.get('parser_mode', 'lightweight')}")
    print(f"Total Files: {len(media_files)}")
    print("-" * 30)

    start_time = time.time()
    results = []

    for i, path in enumerate(media_files):
        print(f"[{i+1}/{len(media_files)}] Processing: {path.name}...", end="", flush=True)
        t0 = time.time()
        try:
            item = MediaItem(path.name, str(path))
            dt = time.time() - t0
            results.append({
                'name': path.name,
                'time': dt,
                'type': item.logical_type,
                'art': item.art_path is not None
            })
            print(f" OK ({dt:.3f}s)")
        except Exception as e:
            print(f" FAILED: {e}")

    total_duration = time.time() - start_time
    print("-" * 30)
    print(f"Benchmark finished in {total_duration:.2f} seconds.")
    
    if results:
        avg_time = sum(r['time'] for r in results) / len(results)
        print(f"Average time per file: {avg_time:.3f}s")
        
        # Stability check
        success_rate = len(results) / len(media_files) * 100
        print(f"Stability (Success Rate): {success_rate:.1f}%")
        
        # Artwork extraction performance
        art_count = sum(1 for r in results if r['art'])
        print(f"Artwork extracted: {art_count}/{len(results)}")

if __name__ == "__main__":
    # Use media folder if it exists, otherwise fall back to some known paths or exit
    media_dir = Path("media")
    if not media_dir.exists():
        media_dir.mkdir(exist_ok=True)
        # Create some mocks if empty
        print("Media directory empty, creating mocks for benchmark...")
        # (Assuming the previous mock script ran or will be run)
        
    all_files = list(media_dir.rglob("*"))
    media_files = [f for f in all_files if f.is_file() and not f.name.startswith(".")]
    
    if not media_files:
        print("No media files found for benchmark. Please put some files in 'media/'")
        sys.exit(1)
        
    run_benchmark(media_files)
