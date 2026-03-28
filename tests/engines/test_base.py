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
        print(f"  [{self.suite_name}-L{res.level:02d}] {res.name}: {icon} {res.status} | {res.message}")

    def run(self, basis_only: bool = False) -> List[DiagnosticResult]:
        """Automatically discovers and runs all level_N methods."""
        stages = []
        for attr_name in dir(self):
            if attr_name.startswith("level_"):
                method = getattr(self, attr_name)
                if callable(method):
                    stages.append(method)
        
        def get_level(m):
            import re
            match = re.search(r'level_(\d+)', m.__name__)
            return int(match.group(1)) if match else 999
        
        stages.sort(key=get_level)
        return self._execute(stages, basis_only=basis_only)

    def run_all(self, stages: List[Callable[[], DiagnosticResult]]) -> List[DiagnosticResult]:
        """Legacy compatibility method."""
        return self._execute(stages, basis_only=False)

    def _execute(self, stages: List[Callable[[], DiagnosticResult]], basis_only: bool = False) -> List[DiagnosticResult]:
        """Internal executor with filtering."""
        print(f"\n🚀 Starting {self.suite_name} {'(BASIS ONLY)' if basis_only else ''}...")
        for stage in stages:
            try:
                import re
                match = re.search(r'level_(\d+)', stage.__name__)
                level = int(match.group(1)) if match else 0
                
                if basis_only and level > 2:
                    continue
                    
                res = stage()
                self.log_result(res)
            except Exception as e:
                err_res = DiagnosticResult(0, stage.__name__, "FAIL", f"Unhandled Exception: {str(e)}")
                self.log_result(err_res)
        return self.results
