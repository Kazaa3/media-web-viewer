#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Performance Benchmark
# Eingabewerte: logger.py, db.py
# Ausgabewerte: Latenzstatistiken für Debug-Log-Schreibpfad und DB-Insert-Pfad
# Testdateien: Temporäre SQLite-DB
# Kommentar: Vergleicht, wie schnell Debug-Logs und DB-Schreibvorgänge lokal verarbeitet werden.

from __future__ import annotations

import json
import logging
import os
import statistics
import tempfile
import time
from pathlib import Path

import src.core.db as db
import src.core.logger as logger

def _pct(values: list[float], p: float) -> float:
    ordered = sorted(values)
    idx = min(len(ordered) - 1, int(len(ordered) * p))
    return ordered[idx]

def _stats(values_ms: list[float]) -> dict:
    return {
        "samples": len(values_ms),
        "avg_ms": round(statistics.mean(values_ms), 4),
        "median_ms": round(statistics.median(values_ms), 4),
        "p95_ms": round(_pct(values_ms, 0.95), 4),
        "min_ms": round(min(values_ms), 4),
        "max_ms": round(max(values_ms), 4),
    }

def benchmark_debug_log_write(samples: int = 500) -> dict:
    logger.setup_logging(debug_mode=True)
    logger.set_debug_flags({"db": True, "system": False})

    devnull = open(os.devnull, "w", encoding="utf-8")
    root_logger = logging.getLogger()
    original_streams: list[tuple[logging.Handler, object]] = []

    try:
        for handler in root_logger.handlers:
            if isinstance(handler, logging.StreamHandler):
                original_streams.append((handler, getattr(handler, "stream", None)))
                handler.setStream(devnull)

        timings_ms: list[float] = []
        for i in range(samples):
            start = time.perf_counter()
            logger.debug("db", f"benchmark-debug-log-{i}")
            timings_ms.append((time.perf_counter() - start) * 1000.0)

        return _stats(timings_ms)
    finally:
        for handler, original_stream in original_streams:
            if original_stream is not None:
                handler.setStream(original_stream)
        devnull.close()

def benchmark_db_insert_write(samples: int = 300) -> dict:
    original_db_filename = db.DB_FILENAME
    original_db_dir = db.DB_DIR

    with tempfile.TemporaryDirectory(prefix="mwv_bench_db_") as tmp:
        temp_dir = Path(tmp)
        db.DB_DIR = temp_dir
        db.DB_FILENAME = str(temp_dir / "media_library.db")
        db.init_db()

        timings_ms: list[float] = []
        for i in range(samples):
            item = {
                "name": f"bench_item_{i}.mp3",
                "path": f"/tmp/bench_item_{i}.mp3",
                "type": "mp3",
                "duration": "3:21",
                "category": "Audio",
                "is_transcoded": False,
                "transcoded_format": None,
                "tags": {"title": f"Bench {i}", "artist": "Benchmark"},
                "extension": "mp3",
                "container": "mpeg",
                "tag_type": "ID3",
                "codec": "mp3",
            }
            start = time.perf_counter()
            db.insert_media(item)
            timings_ms.append((time.perf_counter() - start) * 1000.0)

        result = _stats(timings_ms)

    db.DB_FILENAME = original_db_filename
    db.DB_DIR = original_db_dir
    return result

def main() -> None:
    samples_log = 500
    samples_db = 300

    debug_stats = benchmark_debug_log_write(samples=samples_log)
    db_stats = benchmark_db_insert_write(samples=samples_db)

    comparison = {
        "debug_vs_db_avg_ratio": round(
            (db_stats["avg_ms"] / debug_stats["avg_ms"]) if debug_stats["avg_ms"] > 0 else 0.0,
            2,
        ),
        "debug_vs_db_median_ratio": round(
            (db_stats["median_ms"] / debug_stats["median_ms"]) if debug_stats["median_ms"] > 0 else 0.0,
            2,
        ),
    }

    payload = {
        "benchmark": "debug_console_and_db_write_speed",
        "timestamp": int(time.time()),
        "debug_log_write": debug_stats,
        "db_insert_write": db_stats,
        "comparison": comparison,
        "notes": [
            "Debug logging uses logger.debug(component='db', ...) with debug mode enabled.",
            "Console stream is routed to /dev/null for noise reduction while preserving handler path overhead.",
            "DB benchmark uses temporary SQLite file and real insert_media() calls.",
        ],
    }

    print(json.dumps(payload, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
