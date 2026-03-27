from dataclasses import dataclass, asdict
from typing import Dict, Any, List, Optional, Union, Callable
import time

@dataclass
class DiagnosticResult:
    """Standardized result for any diagnostic test stage."""
    level: int
    name: str
    status: str  # "PASS", "FAIL", "SKIP", "WARN"
    message: str
    details: Optional[Dict[str, Any]] = None

class DiagnosticEngine:
    """
    Base class for all diagnostic engines.
    Provides standard logging and result tracking.
    """
    def __init__(self, suite_name: str = "Diagnostic Engine") -> None:
        self.suite_name = suite_name
        self.results: List[DiagnosticResult] = []

    def log_result(self, res: DiagnosticResult) -> None:
        self.results.append(res)
        icon = {"PASS": "✅", "FAIL": "❌", "SKIP": "⏭️", "WARN": "⚠️"}.get(res.status, "❓")
        # Determine prefix based on level if needed, or just suite name
        print(f"  [{self.suite_name}-L{res.level:02d}] {res.name}: {icon} {res.status} | {res.message}")

    def run_all(self, stages: List[Callable[[], DiagnosticResult]]) -> List[DiagnosticResult]:
        """Runs a sequence of diagnostic stages."""
        print(f"\n🚀 Starting {self.suite_name}...")
        for stage in stages:
            try:
                res = stage()
                self.log_result(res)
            except Exception as e:
                err_res = DiagnosticResult(0, stage.__name__, "FAIL", f"Unhandled Exception: {str(e)}")
                self.log_result(err_res)
        return self.results
