import sys
import os
from pathlib import Path
from typing import List

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# Diagnostic Base
try:
    from tests.test_base import DiagnosticEngine, DiagnosticResult
except ImportError:
    from test_base import DiagnosticEngine, DiagnosticResult

class ItemsSuiteEngine(DiagnosticEngine):
    def __init__(self) -> None:
        super().__init__(suite_name="Items")

    def level_1_ffprobe_mock(self) -> DiagnosticResult:
        return DiagnosticResult(1, "FFprobe Sim", "SKIP", "Staged for full migration")

    def run_all(self) -> List[DiagnosticResult]:
        return super().run_all([self.level_1_ffprobe_mock])

if __name__ == "__main__":
    ItemsSuiteEngine().run_all()
