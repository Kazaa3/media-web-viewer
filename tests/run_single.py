import sys
import os
from pathlib import Path

from src.core.config_master import PROJECT_ROOT, DB_FILENAME, TEST_DIR, DATA_DIR
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(PROJECT_ROOT / "src"))

from tests.engines.suite_ui_integrity import UIIntegritySuiteEngine

def run_single():
    print("="*60)
    print("RUNNING SINGLE SUITE: UI Integrity")
    print("="*60)
    
    suite = UIIntegritySuiteEngine()
    suite.run()
    
    print("\n" + "="*60)
    print("SINGLE SUITE RUN COMPLETE")
    print("="*60)

if __name__ == "__main__":
    os.environ["MWV_ALLOW_MULTIPLE_SESSIONS"] = "1"
    run_single()
