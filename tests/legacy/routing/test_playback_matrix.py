import os
import sys
import time
import json
import logging
import subprocess
import threading
import requests
import statistics
import urllib.parse
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')
log = logging.getLogger("playback_matrix")

PROJECT_ROOT = Path(__file__).parents[2]
MEDIA_ROOT = PROJECT_ROOT / "media"
RESULTS_FILE = PROJECT_ROOT / "data" / "playback_benchmark_results.json"

# Mock server address (assume backend is running)
BASE_URL = "http://localhost:8000"

def get_file_info(path):
    """Get codec/container info using ffprobe"""
    cmd = [
        "ffprobe", "-v", "error", 
        "-show_entries", "format=format_name:stream=codec_name,codec_type", 
        "-of", "json", str(path)
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        data = json.loads(result.stdout)
        
        container = data.get("format", {}).get("format_name", "unknown")
        video_codec = None
        audio_codec = None
        
        for stream in data.get("streams", []):
            if stream.get("codec_type") == "video" and not video_codec:
                video_codec = stream.get("codec_name")
            elif stream.get("codec_type") == "audio" and not audio_codec:
                audio_codec = stream.get("codec_name")
        
        return video_codec, audio_codec, container
    except Exception as e:
        log.error(f"  [Error] {path.name}: {e}")
        return None, None, None

def measure_ttfb(url):
    """Measure Time to First Byte"""
    try:
        start = time.time()
        with requests.get(url, stream=True, timeout=5) as r:
            for _ in r.iter_content(chunk_size=1):
                return (time.time() - start) * 1000
    except:
        return None

def run_benchmark():
    files = list(MEDIA_ROOT.rglob("*"))
    files = [f for f in files if f.is_file() and f.suffix.lower() in [
        '.mp4', '.mkv', '.avi', '.webm', '.mov', '.ts', '.mp3', '.flac', '.wav', '.ogg', '.m4a', '.opus', '.wma', '.vob'
    ]]
    
    unique_combinations = {}
    
    log.info(f"Analyzing {len(files)} files for unique format/codec combinations...")
    for f in files:
        v, a, c = get_file_info(f)
        if v or a:
            key = f"{c}_{v or ''}_{a or ''}"
            if key not in unique_combinations:
                unique_combinations[key] = f
                
    log.info(f"Found {len(unique_combinations)} unique test vectors.")
    
    results = []
    
    for combo, f_path in unique_combinations.items():
        log.info(f"Testing: {f_path.name} ({combo})")
        
        stats = {
            "filename": f_path.name,
            "combo": combo,
            "size_mb": round(os.path.getsize(f_path) / (1024*1024), 2),
            "modes": {}
        }
        
        # Test 1: RAW
        url_raw = f"{BASE_URL}/media-raw/{urllib.parse.quote(f_path.relative_to(MEDIA_ROOT).as_posix())}"
        ttfb_raw = measure_ttfb(url_raw)
        stats["modes"]["raw"] = {"ttfb": round(ttfb_raw, 2) if ttfb_raw else None}
        
        # Test 2: STREAM (Default)
        url_stream = f"{BASE_URL}/video-stream/{urllib.parse.quote(f_path.relative_to(MEDIA_ROOT).as_posix())}"
        ttfb_stream = measure_ttfb(url_stream)
        stats["modes"]["stream"] = {"ttfb": round(ttfb_stream, 2) if ttfb_stream else None}
        
        results.append(stats)
        
    # Save results
    RESULTS_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(RESULTS_FILE, 'w') as f:
        json.dump(results, f, indent=4)
        
    log.info(f"Benchmark complete. Results saved to {RESULTS_FILE}")
    
    # Pretty Print Table to Log
    log.info("-" * 100)
    log.info(f"{'FILE':<30} | {'COMBO':<30} | {'RAW':<15} | {'STREAM':<15}")
    log.info("-" * 100)
    for res in results:
        raw_t = f"{res['modes']['raw']['ttfb']}ms" if res['modes']['raw']['ttfb'] else "ERR"
        stm_t = f"{res['modes']['stream']['ttfb']}ms" if res['modes']['stream']['ttfb'] else "ERR"
        log.info(f"{res['filename'][:30]:<30} | {res['combo'][:30]:<30} | {raw_t:<15} | {stm_t:<15}")
    log.info("-" * 100)

if __name__ == "__main__":
    run_benchmark()
