#!/usr/bin/env python3
import sys
import os
import json
from pathlib import Path

# Fix paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from tests.integration.performance.compare_benchmarks import run_current_benchmark, BASELINE_FILE, BASELINE_DIR

def main():
    print(f"🚀 Generating performance baseline at {BASELINE_FILE}...")
    BASELINE_DIR.mkdir(parents=True, exist_ok=True)
    
    results = run_current_benchmark()
    
    with open(BASELINE_FILE, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
        
    print(f"✅ Baseline generated successfully with {len(results)} items.")

if __name__ == "__main__":
    main()
