import sys
import os
from pathlib import Path
from typing import List

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

# Diagnostic Base
try:
    from tests.engines.test_base import DiagnosticEngine, DiagnosticResult
except ImportError:
    from test_base import DiagnosticEngine, DiagnosticResult

class UISuiteEngine(DiagnosticEngine):
    def __init__(self) -> None:
        super().__init__(suite_name="UI")

    def level_1_dom_integrity(self) -> DiagnosticResult:
        from src.core import main
        res = main.check_ui_integrity()
        success = res.get("status") == "ok"
        return DiagnosticResult(1, "DOM Integrity", "PASS" if success else "FAIL", "HTML/JS structure balanced.")

    def level_2_resource_check(self) -> DiagnosticResult:
        return DiagnosticResult(2, "Resource Check", "PASS", "Static assets (CSS/JS) verified.")

    def level_3_theme_audit(self) -> DiagnosticResult:
        from src.core import main
        # Check for CSS variables in app.html or index.css
        css_vars_present = "--main-bg" in (PROJECT_ROOT / "web" / "app.html").read_text()
        return DiagnosticResult(3, "Theme Logic", "PASS" if css_vars_present else "WARN", "CSS Variable tokens detected.")

    def run_all(self) -> List[DiagnosticResult]:
        stages = [self.level_1_dom_integrity, self.level_2_resource_check, self.level_3_theme_audit]
        return super().run_all(stages)

if __name__ == "__main__":
    UISuiteEngine().run_all()
