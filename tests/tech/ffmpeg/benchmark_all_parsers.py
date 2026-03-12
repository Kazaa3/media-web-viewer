# Benchmark: Alle Parser auf allen Dateien
import os
import sys
import glob
import time
import json
from pathlib import Path

PROJECT_ROOT = os.path.abspath(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
if PROJECT_ROOT not in sys.path:
    

from src.parsers import media_parser

media_dir = os.path.join(PROJECT_ROOT, 'media')
files = glob.glob(os.path.join(media_dir, '*.*'))

PARSER_CONFIG = {
    "enable_ebml_parser": True,
    "enable_mkvparse_parser": True,
    "enable_enzyme_parser": True,
    "enable_pycdlib_parser": True,
    "enable_pymkv_parser": True,
    "enable_tinytag_parser": True,
    "enable_eyed3_parser": True,
    "enable_music_tag_parser": True,
}

results = {}

for f in files:
    name = os.path.basename(f)
    file_type = Path(f).suffix.lower()
    t0 = time.time()
    try:
        tags, times = media_parser.extract_metadata(
            os.path.abspath(f),
            name,
            mode="full",
            file_type=file_type,
        duration = time.time() - t0
        results[name] = {
            "duration": duration,
            "parser_times": times,
            "tags": tags,
        }
    except Exception as e:
        results[name] = {
            "error": str(e)
        }

with open("tests/parser_benchmark_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("Benchmark abgeschlossen: tests/parser_benchmark_results.json")
