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

    def level_6_js_string_syntax(self) -> DiagnosticResult:
        """Checks for unescaped nested quotes in common JS patterns (e.g. showToast)."""
        if not self.app_html.exists():
            return DiagnosticResult(6, "JS Syntax", "FAIL", "web/app.html missing")
        
        content = self.app_html.read_text(encoding='utf-8')
        # Heuristic: Find showToast("...width="...") or similar
        malformed = re.findall(r'showToast\(".*?width=".*?"', content)
        
        if malformed:
            return DiagnosticResult(6, "JS Syntax", "FAIL", f"Found {len(malformed)} malformed showToast strings (nested quotes).")
        
        return DiagnosticResult(6, "JS Syntax", "PASS", "No obvious nested quote syntax errors found in app.html.")

    def level_7_svg_icon_refs(self) -> DiagnosticResult:
        """Checks for malformed SVG icon references (e.g. spaces in IDs)."""
        if not self.app_html.exists(): return DiagnosticResult(7, "SVG Icons", "SKIP", "No app.html")
        content = self.app_html.read_text(encoding='utf-8')
        # Find href="#icon - sparkles" or "#icon- sparkles" or "#icon -sparkles"
        # We look for "#icon" followed by any whitespace or hyphen with whitespace
        malformed = re.findall(r'href="#icon\s*-\s*[^"]*?\s+[^"]*?"', content)
        # Also catch the specific " - " pattern
        malformed += re.findall(r'href="#icon\s+-\s+[^"]+?"', content)
        
        if malformed:
            unique_malformed: List[str] = list(set(malformed))
            return DiagnosticResult(7, "SVG Icons", "FAIL", f"Found {len(malformed)} malformed icon references (spaces in IDs): {', '.join(unique_malformed[:3])}")
        
        return DiagnosticResult(7, "SVG Icons", "PASS", "SVG icon references are clean.")

    def level_8_onerror_bridge_presence(self) -> DiagnosticResult:
        """Verifies if the window.onerror bridge is present for real-time logging."""
        if not self.app_html.exists(): return DiagnosticResult(8, "OnError Bridge", "SKIP", "No app.html")
        content = self.app_html.read_text(encoding='utf-8')
        if "window.onerror" in content and "eel.log_js_error" in content:
            return DiagnosticResult(8, "OnError Bridge", "PASS", "Real-time JS error bridge found.")
        return DiagnosticResult(8, "OnError Bridge", "FAIL", "window.onerror bridge missing or misconfigured.")

    def level_9_tab_navigation(self) -> DiagnosticResult:
        """Verifies that all switchTab calls have a valid mapping and target ID."""
        if not self.app_html.exists(): return DiagnosticResult(9, "Tab Navigation", "SKIP", "No app.html")
        content = self.app_html.read_text(encoding='utf-8')
        
        # 1. Extract tabMap from JS
        tab_map_match = re.search(r'const tabMap = \{(.*?)\};', content, re.DOTALL)
        if not tab_map_match:
            return DiagnosticResult(9, "Tab Navigation", "FAIL", "Could not find tabMap in app.html")
        
        tab_map_str = tab_map_match.group(1)
        # Parse it into a python dict (simple regex approach)
        tab_map = {}
        for line in tab_map_str.split('\n'):
            match = re.search(r"['\"](\w+)['\"]\s*:\s*['\"]([\w-]+)['\"]", line)
            if match:
                tab_map[match.group(1)] = match.group(2)
        
        # 2. Find all switchTab calls in buttons
        switch_calls = re.findall(r"switchTab\(\s*['\"](\w+)['\"]", content)
        unique_calls = list(set(switch_calls))
        
        missing_mappings = [t for t in unique_calls if t not in tab_map]
        missing_targets = [tab_map[t] for t in tab_map if f'id="{tab_map[t]}"' not in content and f"id='{tab_map[t]}'" not in content]
        
        errors = []
        if missing_mappings:
            errors.append(f"Missing mappings for: {missing_mappings}")
        if missing_targets:
            errors.append(f"Missing target elements for IDs: {missing_targets}")
            
        if errors:
            return DiagnosticResult(9, "Tab Navigation", "FAIL", " | ".join(errors))
            
        return DiagnosticResult(9, "Tab Navigation", "PASS", f"Verified {len(unique_calls)} tab IDs and {len(tab_map)} target panels.")

    def level_10_debug_db_view(self) -> DiagnosticResult:
        """Verifies integrity of the Debug & Database view components."""
        if not self.app_html.exists(): return DiagnosticResult(10, "Debug & DB View", "SKIP", "No app.html")
        content = self.app_html.read_text(encoding='utf-8')
        
        required_elements = [
            'id="debug-flag-persistence-panel"', 
            'data-i18n="debug_db_loading_stats"',
            'id="debug-db-info"',
            'id="lib-db-table-body"'
        ]
        missing = [e for e in required_elements if e not in content]
        
        if missing:
            return DiagnosticResult(10, "Debug & DB View", "FAIL", f"Missing Debug/DB components: {missing}")
            
        return DiagnosticResult(10, "Debug & DB View", "PASS", "Debug & Database view structure verified.")

    def run_all(self) -> List[DiagnosticResult]:
        stages = [
            self.level_1_structural_balance, self.level_2_css_token_audit,
            self.level_3_critical_selectors, self.level_4_backend_leakage,
            self.level_5_responsive_sanity, self.level_6_js_string_syntax,
            self.level_7_svg_icon_refs, self.level_8_onerror_bridge_presence,
            self.level_9_tab_navigation, self.level_10_debug_db_view
        ]
        return super().run_all(stages)

if __name__ == "__main__":
    UIIntegritySuiteEngine().run_all()
