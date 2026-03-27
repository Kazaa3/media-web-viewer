import sys
import os
import re
from pathlib import Path
from typing import List, Dict, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(PROJECT_ROOT / "src"))

# Diagnostic Base
try:
    from tests.engines.test_base import DiagnosticEngine, DiagnosticResult
except ImportError:
    from test_base import DiagnosticEngine, DiagnosticResult

class CodeQualitySuiteEngine(DiagnosticEngine):
    def __init__(self) -> None:
        super().__init__(suite_name="Quality")
        os.environ["UNIT_TESTING"] = "1"

    def level_1_eel_api_alignment(self) -> DiagnosticResult:
        """Audits Frontend Eel calls vs Backend exposures (Legacy: test_compatibility.py)."""
        app_html = PROJECT_ROOT / "web" / "app.html"
        main_py = PROJECT_ROOT / "src" / "core" / "main.py"
        
        if not app_html.exists() or not main_py.exists():
            return DiagnosticResult(1, "Eel API Alignment", "FAIL", "app.html or main.py missing.")

        with open(app_html, 'r', encoding='utf-8') as f: html_content = f.read()
        with open(main_py, 'r', encoding='utf-8') as f: main_content = f.read()

        exposed = set(re.findall(r'@eel\.expose\s+def\s+([a-zA-Z0-9_]+)', main_content))
        eel_calls = set(re.findall(r'eel\.([a-zA-Z0-9_]+)\(', html_content))
        
        to_ignore = {'expose', 'set_host', 'start'}
        missing_in_backend = (eel_calls - exposed) - to_ignore
        
        success = len(missing_in_backend) == 0
        return DiagnosticResult(1, "Eel API Alignment", "PASS" if success else "FAIL", 
                                f"Mismatches: {missing_in_backend}" if not success else f"Verified {len(eel_calls)} API calls.")

    def level_2_html_sanity(self) -> DiagnosticResult:
        """Performs basic HTML structural audit (Legacy: test_compatibility.py)."""
        app_html = PROJECT_ROOT / "web" / "app.html"
        if not app_html.exists():
            return DiagnosticResult(2, "HTML Sanity", "SKIP", "app.html missing.")

        with open(app_html, 'r', encoding='utf-8') as f: html_content = f.read()
        
        open_divs = html_content.count("<div")
        close_divs = html_content.count("</div")
        
        success = open_divs == close_divs
        return DiagnosticResult(2, "HTML Sanity", "PASS" if success else "WARN", 
                                f"Div Balance: {open_divs} open vs {close_divs} close.")

    def level_3_tab_existence_audit(self) -> DiagnosticResult:
        """Verifies that all switchTab targets exist in HTML (Legacy: debug_ui.py)."""
        app_html = PROJECT_ROOT / "web" / "app.html"
        if not app_html.exists(): return DiagnosticResult(3, "Tab Audit", "SKIP", "app.html missing.")

        with open(app_html, 'r', encoding='utf-8') as f: html_content = f.read()
        tab_calls = set(re.findall(r"switchTab\(['\"]([^'\"]+)['\"]", html_content))
        
        missing_tabs = []
        for tab_id in tab_calls:
            if tab_id == "${tabId}" or tab_id == "playlist": continue # ignore dynamic or internal
            if f'id="{tab_id}"' not in html_content:
                missing_tabs.append(tab_id)
        
        success = len(missing_tabs) == 0
        return DiagnosticResult(3, "Tab Audit", "PASS" if success else "WARN", 
                                f"Missing Tab IDs: {missing_tabs}" if not success else f"Verified {len(tab_calls)} tab definitions.")

    def run_all(self, stages: List[Any] = None) -> List[DiagnosticResult]:
        if not stages:
            stages = [self.level_1_eel_api_alignment, self.level_2_html_sanity, self.level_3_tab_existence_audit]
        return super().run_all(stages)

if __name__ == "__main__":
    CodeQualitySuiteEngine().run_all()
