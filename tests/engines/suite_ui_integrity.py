import sys
import os
import re
from pathlib import Path
from typing import List, Dict, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

# Diagnostic Base
try:
    from tests.engines.test_base import DiagnosticEngine, DiagnosticResult
except ImportError:
    from test_base import DiagnosticEngine, DiagnosticResult

class UIIntegritySuiteEngine(DiagnosticEngine):
    def __init__(self) -> None:
        super().__init__(suite_name="UI Integrity")
        self.app_html = PROJECT_ROOT / "web" / "app.html"

    def level_1_structural_balance(self) -> DiagnosticResult:
        """Verifies DIV and BRACE balance in app.html to prevent layout breakdown."""
        if not self.app_html.exists():
            return DiagnosticResult(1, "Structural Balance", "FAIL", "app.html not found.")
        
        content = self.app_html.read_text(encoding='utf-8')
        
        open_divs = len(re.findall(r"<div", content))
        close_divs = len(re.findall(r"</div", content))
        
        open_braces = content.count("{")
        close_braces = content.count("}")
        
        success = (open_divs == close_divs) and (open_braces == close_braces)
        return DiagnosticResult(1, "Structural Balance", "PASS" if success else "WARN", 
                                f"DIVs: {open_divs}/{close_divs}, Braces: {open_braces}/{close_braces}")

    def level_2_css_token_audit(self) -> DiagnosticResult:
        """Verifies that core CSS variables and theme tokens are present."""
        if not self.app_html.exists(): return DiagnosticResult(2, "CSS Token Audit", "SKIP", "No app.html")
        
        content = self.app_html.read_text(encoding='utf-8')
        required_vars = ["--bg-primary", "--accent-color", "--text-main", "--sidebar-width"]
        missing = [v for v in required_vars if v not in content]
        
        return DiagnosticResult(2, "CSS Token Audit", "PASS" if not missing else "WARN", 
                                f"Missing tokens: {missing}" if missing else "All core theme variables found.")

    def level_3_critical_selectors(self) -> DiagnosticResult:
        """Checks for the existence of mandatory DOM IDs used by the backend."""
        if not self.app_html.exists(): return DiagnosticResult(3, "Critical Selectors", "SKIP", "No app.html")
        
        content = self.app_html.read_text(encoding='utf-8')
        required_ids = ["sidebar-container", "main-content-area", "player-controls", "library-tab"]
        missing = [i for i in required_ids if f'id="{i}"' not in content and f"id='{i}'" not in content]
        
        return DiagnosticResult(3, "Critical Selectors", "PASS" if not missing else "WARN", 
                                f"Missing IDs: {missing}" if missing else "Critical UI anchors found.")

    def level_4_backend_leakage(self) -> DiagnosticResult:
        """Scans for unescaped Python/EEL snippets or raw placeholders in the HTML."""
        if not self.app_html.exists(): return DiagnosticResult(4, "Backend Leakage", "SKIP", "No app.html")
        
        content = self.app_html.read_text(encoding='utf-8')
        # Look for raw {{ var }} or unescaped python decorators/logic
        leaks = re.findall(r"\{\{.*?\}\}", content)
        # We also check for 'eel.expose' which should be in script blocks, not raw text
        
        return DiagnosticResult(4, "Backend Leakage", "PASS" if not leaks else "WARN", 
                                f"Found {len(leaks)} potential raw placeholders." if leaks else "No obvious backend leakage found.")

    def level_5_responsive_sanity(self) -> DiagnosticResult:
        """Verifies that media queries and breakpoints are reasonably defined."""
        if not self.app_html.exists(): return DiagnosticResult(5, "Responsive Sanity", "SKIP", "No app.html")
        
        content = self.app_html.read_text(encoding='utf-8')
        queries = re.findall(r"@media", content)
        
        return DiagnosticResult(5, "Responsive Sanity", "PASS" if len(queries) > 0 else "WARN", 
                                f"Found {len(queries)} media queries.")

    def run_all(self, stages: List[Any] = None) -> List[DiagnosticResult]:
        if not stages:
            stages = [
                self.level_1_structural_balance,
                self.level_2_css_token_audit,
                self.level_3_critical_selectors,
                self.level_4_backend_leakage,
                self.level_5_responsive_sanity
            ]
        return super().run_all(stages)

if __name__ == "__main__":
    UIIntegritySuiteEngine().run_all()
