#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Advanced / Performance
# Eingabewerte: Current benchmark results, baseline results
# Ausgabewerte: Performance regression report (Delta %)
# Testdateien: src/parsers/media_parser.py
# Kommentar: Regression testing utility for Media Web Viewer. Compares current media extraction performance against historical baselines.

import os
import sys
import time
import json
import glob
from pathlib import Path
from typing import Dict, Any

# Setup paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.append(str(PROJECT_ROOT))

try:
    from src.parsers import media_parser
except ImportError:
    print("❌ Error: Could not import media_parser. Ensure PYTHONPATH is correct.")
    sys.path.append(str(PROJECT_ROOT / "src"))
    from src.parsers import media_parser

BASELINE_DIR = PROJECT_ROOT / "tests" / "artifacts" / "baseline"
# Allow override from environment (BuildSystem)
REPORT_DIR = Path(os.getenv("PERF_REPORT_DIR", str(PROJECT_ROOT / "tests" / "artifacts" / "reports")))
BASELINE_FILE = BASELINE_DIR / "parser_benchmark_results.json"

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

def run_current_benchmark() -> Dict[str, Any]:
    """Runs a fresh benchmark on the current media directory."""
    media_dir = PROJECT_ROOT / "media"
    files = glob.glob(str(media_dir / "*.*"))
    results = {}

    print(f"📊 Running current benchmark on {len(files)} files...")
    
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
                "tag_count": len(tags) if tags else 0,
                "status": "success"
            }
        except Exception as e:
            results[name] = {
                "error": str(e),
                "status": "failed"
            }
            
    return results

def compare_results(baseline: Dict[str, Any], current: Dict[str, Any]):
    """Compares current results against baseline and prints a summary."""
    print("\n" + "="*80)
    print(f"{'Performance Regression Report':^80}")
    print("="*80)
    print(f"{'Filename':<30} | {'Baseline (s)':<12} | {'Current (s)':<12} | {'Delta (%)':<10}")
    print("-" * 80)

    total_baseline_time = 0.0
    total_current_time = 0.0
    impacted_files = 0

    for name, current_data in current.items():
        if name not in baseline:
            # Skip files not in baseline for direct comparison
            continue
            
        baseline_data = baseline[name]
        
        if current_data["status"] == "failed" or baseline_data.get("status") == "failed":
            continue

        b_time = baseline_data.get("duration", 0.0)
        c_time = current_data.get("duration", 0.0)
        
        if b_time > 0:
            delta = ((c_time - b_time) / b_time) * 100
        else:
            delta = 0.0

        total_baseline_time += b_time
        total_current_time += c_time
        impacted_files += 1

        print(f"{name[:30]:<30} | {b_time:12.4f} | {c_time:12.4f} | {delta:+10.2f}%")

    print("="*80)
    if total_baseline_time > 0:
        total_delta = ((total_current_time - total_baseline_time) / total_baseline_time) * 100
    else:
        total_delta = 0.0

    print(f"SUMMARY ({impacted_files} files compared):")
    print(f"  • Total Baseline Time: {total_baseline_time:.4f} s")
    print(f"  • Total Current Time:  {total_current_time:.4f} s")
    print(f"  • Overall Delta:       {total_delta:+.2f}%")
    
    if total_delta > 10:
        print("\n⚠️ WARNING: Significant performance regression detected!")
    elif total_delta < -10:
        print("\n🚀 SUCCESS: Significant performance improvement detected!")
    else:
        print("\n✅ Performance is stable.")
    print("="*80)

def main():
    if not BASELINE_FILE.exists():
        print(f"⚠️ Warning: Baseline file not found at {BASELINE_FILE}")
        print("   Skipping comparison. A new report will be generated.")
        baseline = {}
    else:
        with open(BASELINE_FILE, "r", encoding="utf-8") as f:
            baseline = json.load(f)

    current = run_current_benchmark()
    
    if baseline:
        compare_results(baseline, current)
    else:
        print("📊 Current benchmark results collected.")

    # Save current as a report for future reference
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / f"comparison_report_{int(time.time())}.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(current, f, indent=2, ensure_ascii=False)
    print(f"Report saved to: {report_path}")

if __name__ == "__main__":
    main()
