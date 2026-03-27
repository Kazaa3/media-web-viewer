import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# Import all suites
try:
    from tests.suite_ultimate import UltimateSuiteEngine
    from tests.suite_items import ItemsSuiteEngine
    from tests.suite_ui import UISuiteEngine
    from tests.suite_env import EnvSuiteEngine
    from tests.suite_database import DatabaseSuiteEngine
except ImportError:
    from suite_ultimate import UltimateSuiteEngine
    from suite_items import ItemsSuiteEngine
    from suite_ui import UISuiteEngine
    from suite_env import EnvSuiteEngine
    from suite_database import DatabaseSuiteEngine

# Diagnostic Base
try:
    from tests.test_base import DiagnosticEngine, DiagnosticResult
except ImportError:
    from test_base import DiagnosticEngine, DiagnosticResult

def run_master_diagnostic():
    print("="*60)
    print("ULTIMATE MEDIA WEB VIEWER - MASTER DIAGNOSTIC RUNNER")
    print("="*60)
    
    UltimateSuiteEngine().run_all()
    ItemsSuiteEngine().run_all()
    UISuiteEngine().run_all()
    EnvSuiteEngine().run_all()
    DatabaseSuiteEngine().run_all()
    
    print("\n" + "="*60)
    print("MASTER DIAGNOSTIC COMPLETE")
    print("="*60)

if __name__ == "__main__":
    run_master_diagnostic()
