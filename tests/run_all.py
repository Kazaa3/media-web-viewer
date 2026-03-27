import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# Import all suites
try:
    from tests.engines.suite_ultimate import UltimateSuiteEngine
    from tests.engines.suite_items import ItemsSuiteEngine
    from tests.engines.suite_ui import UISuiteEngine
    from tests.engines.suite_env import EnvSuiteEngine
    from tests.engines.suite_database import DatabaseSuiteEngine
    from tests.engines.suite_player import PlayerSuiteEngine
except ImportError:
    from engines.suite_ultimate import UltimateSuiteEngine
    from engines.suite_items import ItemsSuiteEngine
    from engines.suite_ui import UISuiteEngine
    from engines.suite_env import EnvSuiteEngine
    from engines.suite_database import DatabaseSuiteEngine
    from engines.suite_player import PlayerSuiteEngine

# Diagnostic Base
try:
    from tests.engines.test_base import DiagnosticEngine, DiagnosticResult
except ImportError:
    from engines.test_base import DiagnosticEngine, DiagnosticResult

def run_master_diagnostic():
    print("="*60)
    print("ULTIMATE MEDIA WEB VIEWER - MASTER DIAGNOSTIC RUNNER")
    print("="*60)
    
    UltimateSuiteEngine().run_all()
    ItemsSuiteEngine().run_all()
    UISuiteEngine().run_all()
    EnvSuiteEngine().run_all()
    DatabaseSuiteEngine().run_all()
    PlayerSuiteEngine().run_all()
    
    print("\n" + "="*60)
    print("MASTER DIAGNOSTIC COMPLETE")
    print("="*60)

if __name__ == "__main__":
    run_master_diagnostic()
