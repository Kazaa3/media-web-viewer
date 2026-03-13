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

PROJECT_ROOT = os.path.abspath(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

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
            PARSER_CONFIG=PARSER_CONFIG
        )
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

with open("tests/artifacts/reports/parser_benchmark_results.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2, ensure_ascii=False)

print("Benchmark abgeschlossen: tests/parser_benchmark_results.json")
