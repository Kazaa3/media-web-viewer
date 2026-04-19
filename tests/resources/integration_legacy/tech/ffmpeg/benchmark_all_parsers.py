#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Tech / FFmpeg (Benchmark)
# Eingabewerte: Alle Mediendateien im Bestand
# Ausgabewerte: Performance-Metriken pro Parser (duration, parser_times)
# Testdateien: src/parsers/media_parser.py, alle tech-spezifischen Parser
# Kommentar: Benchmark für alle Metadaten-Parser auf dem gesamten Medienbestand.
"""
FFmpeg Parser Benchmark Test Suite (DE/EN)
==========================================

DE:
Benchmark für alle Metadaten-Parser auf dem gesamten Medienbestand.

EN:
Benchmark for all metadata parsers on the entire media library.

Autor/Author: Media Web Viewer Team
Erstellt/Created: 2026-03-13
Version: 1.0.0
"""

import os
import sys
import glob
import time
import json
from pathlib import Path

from src.parsers import media_parser
from src.parsers.format_utils import PARSER_CONFIG

# Setup paths and centralized reporting
from src.core.config_master import PROJECT_ROOT, DB_FILENAME, TEST_DIR, DATA_DIR
# Allow override from environment (BuildSystem)
REPORT_DIR = Path(os.getenv("PERF_REPORT_DIR", str(PROJECT_ROOT / "tests" / "artifacts" / "reports")))

media_dir = PROJECT_ROOT / "media"
files = list(media_dir.glob("*.*"))

results = {
    "audit_metadata": {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "parser_config": PARSER_CONFIG,
        "media_dir": str(media_dir)
    },
    "format_stats": {},
    "detailed_results": {}
}

for f in files:
    name = f.name
    file_type = f.suffix.lower()
    t0 = time.time()
    
    # Init format stats if new
    if file_type not in results["format_stats"]:
        results["format_stats"][file_type] = {
            "count": 0,
            "success_count": 0,
            "total_duration": 0.0,
            "parsers_used": {}
        }
    
    fmt_stat = results["format_stats"][file_type]
    fmt_stat["count"] += 1

    file_size_mb = f.stat().st_size / (1024 * 1024)
    # Use lightweight mode for very large files (> 500MB) to avoid audit stalls/memory spikes
    extraction_mode = "full" if file_size_mb < 500 else "lightweight"
    
    mode_str = "FULL" if extraction_mode == "full" else "LIGHT"
    print(f"⏳ Processing: {name} ({file_type}, {file_size_mb:.1f}MB) [{mode_str}] ...", flush=True)

    try:
        # Use a localized timeout for each file to prevent total audit hang
        tags, times = media_parser.extract_metadata(
            str(f.absolute()),
            name,
            mode=extraction_mode,
            file_type=file_type,
            PARSER_CONFIG=PARSER_CONFIG
        )
        duration = time.time() - t0
        
        # Determine dominant parser
        parsers_in_this_run = [p for p, t in times.items() if t > 0]
        for p in parsers_in_this_run:
            fmt_stat["parsers_used"][p] = fmt_stat["parsers_used"].get(p, 0) + 1

        results["detailed_results"][name] = {
            "duration": duration,
            "parser_times": times,
            "status": "success",
            "tag_count": len(tags) if tags else 0
        }
        
        fmt_stat["success_count"] += 1
        fmt_stat["total_duration"] += duration

    except Exception as e:
        results["detailed_results"][name] = {
            "error": str(e),
            "status": "failed"
        }

# Finalize Stats
for fmt, data in results["format_stats"].items():
    if data["success_count"] > 0:
        data["avg_duration"] = data["total_duration"] / data["success_count"]
    data["success_rate"] = (data["success_count"] / data["count"]) * 100 if data["count"] > 0 else 0

REPORT_DIR.mkdir(parents=True, exist_ok=True)
report_path = REPORT_DIR / "performance_audit_results.json"
with open(report_path, "w", encoding="utf-8") as f_out:
    json.dump(results, f_out, indent=2, ensure_ascii=False)

print(f"📊 Performance Audit complete: {report_path}")
