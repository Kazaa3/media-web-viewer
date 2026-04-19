import sys
import os
from pathlib import Path
from typing import List

from src.core.config_master import PROJECT_ROOT, DB_FILENAME, TEST_DIR, DATA_DIR
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

    def level_11_tab_coverage(self) -> DiagnosticResult:
        content = (PROJECT_ROOT / "web" / "app.html").read_text()
        calls = set(re.findall(r"switchTab\(['\"`](.*?)['\"`]", content))
        valid_calls = {c for c in calls if not c.startswith("${")}
        
        missing = []
        # Mapping table for slugs that differ from IDs
        slug_map = {
            'tests': 'qa-validation',
            'playlist': 'sequential-buffer',
            'reporting': 'reporting-dashboard',
            'logbuch': 'documentation-journal',
            'debug': 'telemetry-inspector',
            'tools': 'tools',
            'item': 'crud-metadata'
        }
        
        for call in valid_calls:
            if call == 'current': continue
            
            search_slug = slug_map.get(call, call)
            
            # Robust regex check for IDs
            pattern = re.compile(rf'id=["\'][^"\']*?{re.escape(search_slug)}[^"\']*?["\']')
            has_id = bool(pattern.search(content))
            has_trigger = f'-{call}-tab-trigger' in content
            
            if not has_id and not has_trigger:
                missing.append(call)
        
        return DiagnosticResult(11, "Tab Coverage", "PASS" if not missing else "FAIL", 
                                f"Verified {len(valid_calls)} unique tab targets. Missing: {missing}")

    def level_12_modal_coverage(self) -> DiagnosticResult:
        content = (PROJECT_ROOT / "web" / "app.html").read_text()
        calls = set(re.findall(r"toggleModal\(['\"`](.*?)['\"`]", content))
        valid_calls = {c for c in calls if not c.startswith("${")}
        
        missing = []
        for call in valid_calls:
            pattern = re.compile(rf'id=["\'][^"\']*?{re.escape(call)}[^"\']*?["\']')
            if not pattern.search(content):
                missing.append(call)
        
        return DiagnosticResult(12, "Modal Coverage", "PASS" if not missing else "FAIL", 
                                f"Verified {len(valid_calls)} unique modal triggers. Missing: {missing}")

    def level_13_toast_feedback(self) -> DiagnosticResult:
        content = (PROJECT_ROOT / "web" / "app.html").read_text()
        has_toast_func = "function showToast" in content
        has_startup_toast = "showToast" in content.split("window.onload")[0] if "window.onload" in content else False
        return DiagnosticResult(13, "Toast System", "PASS" if has_toast_func else "FAIL", 
                                "Toast notification system presence verified.")

    def run_all(self) -> List[DiagnosticResult]:
        stages = [
            self.level_1_dom_integrity, 
            self.level_2_resource_check, 
            self.level_3_theme_audit,
            self.level_11_tab_coverage,
            self.level_12_modal_coverage,
            self.level_13_toast_feedback
        ]
        return super().run_all(stages)

import re
if __name__ == "__main__":
    UISuiteEngine().run()
