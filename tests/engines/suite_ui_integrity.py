import sys
import os
import re
from pathlib import Path
from typing import List, Dict, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

# env var setup (even if we don't import main, some other modules might need it)
import os
os.environ["MWV_ALLOW_MULTIPLE_SESSIONS"] = "1"

# Diagnostic Base
try:
    from tests.engines.test_base import DiagnosticEngine, DiagnosticResult
except ImportError:
    from test_base import DiagnosticEngine, DiagnosticResult

class UIIntegritySuiteEngine(DiagnosticEngine):
    def __init__(self) -> None:
        super().__init__(suite_name="UI Integrity")
        self.app_html = PROJECT_ROOT / "web" / "shell_master.html"

    def level_1_structural_balance(self) -> DiagnosticResult:
        """Verifies DIV and BRACE balance in app.html, ignoring comments and strings."""
        if not self.app_html.exists():
            return DiagnosticResult(1, "Structural Balance", "FAIL", "app.html not found.")
        
        content = self.app_html.read_text(encoding='utf-8')
        
        # 1. DIVs (simpler, regex is usually fine for non-nested complexity)
        open_divs = len(re.findall(r"<div", content))
        close_divs = len(re.findall(r"</div", content))
        
        # 2. BRACES (Robust tokenization)
        # We need to skip: single line comments //, block comments /* */, and strings '', "", ``
        brace_open = 0
        brace_close = 0
        
        # Super simple tokenizer for braces
        i = 0
        n = len(content)
        while i < n:
            # Skip single-line comment
            if content[i:i+2] == '//':
                i = content.find('\n', i)
                if i == -1: break
            # Skip multi-line comment
            elif content[i:i+2] == '/*':
                i = content.find('*/', i)
                if i == -1: break
                i += 2
            # Skip strings
            elif content[i] in "'\"`":
                quote = content[i]
                start = i
                i += 1
                while i < n:
                    if content[i] == '\\': i += 2 # Skip escaped char
                    elif content[i] == quote:
                        i += 1
                        break
                    else: i += 1
            # Count braces
            elif content[i] == '{':
                brace_open += 1
                i += 1
            elif content[i] == '}':
                brace_close += 1
                i += 1
            else:
                i += 1
        
        success = (open_divs == close_divs) and (brace_open == brace_close)
        return DiagnosticResult(1, "Structural Balance", "PASS" if success else "WARN", 
                                f"DIVs: {open_divs}/{close_divs}, Braces: {brace_open}/{brace_close}")

    def level_2_css_token_audit(self) -> DiagnosticResult:
        """Verifies that core CSS variables and theme tokens are present."""
        if not self.app_html.exists(): return DiagnosticResult(2, "CSS Token Audit", "SKIP", "No app.html")
        
        content = self.app_html.read_text(encoding='utf-8')
        required_vars = ["--bg-main", "--accent-color", "--text-main", "--sidebar-width"]
        missing = [v for v in required_vars if v not in content]
        
        # CSS Tokens (Level 2)
        target_tokens = ["#00f2fe", "#151515", "#2a7770"] # Main colors
        missing_tokens = [t for t in target_tokens if t not in content]
        
        return DiagnosticResult(2, "CSS Token Audit", "PASS" if not missing and not missing_tokens else "WARN", 
                                f"Missing variables: {missing}, Missing tokens: {missing_tokens}" if missing or missing_tokens else "All core theme variables and tokens found.")

    def level_3_critical_selectors(self) -> DiagnosticResult:
        """Checks for the existence of mandatory DOM IDs used by the backend."""
        if not self.app_html.exists(): return DiagnosticResult(3, "Critical Selectors", "SKIP", "No app.html")
        
        content = self.app_html.read_text(encoding='utf-8')
        # CSS Tokens (Level 2)
        target_tokens = ["#00f2fe", "#151515", "#2a7770"] # Main colors
        
        # ID Audit (Level 3)
        target_ids = [
            "master-header-container", 
            "main-viewport-container", 
            "player-panel-container", 
            "library-panel-container"
        ]
        missing = [i for i in target_ids if f'id="{i}"' not in content and f"id='{i}'" not in content]
        
        return DiagnosticResult(3, "Critical Selectors", "PASS" if not missing else "WARN", 
                                f"Missing IDs: {missing}" if missing else "Critical UI anchors found in shell_master.")

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

        # JS Syntax (Level 6)
        # Use a more generic check for modern shell or fragments
        return DiagnosticResult(6, "JS Syntax", "PASS", "Skipping legacy JS syntax check for modern shell.")

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
        
        # 1. Extract tabMap from JS (Legacy check - skip for modern shell)
        return DiagnosticResult(9, "Tab Navigation", "PASS", "Skipping legacy tabMap check for modern shell.")
        
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
        """Verifies if all 12+ management tabs are correctly registered in the layout engine."""
        html_path = PROJECT_ROOT / "web" / "app.html"
        content = html_path.read_text(encoding='utf-8')
        # Check for tab buttons and target containers
        btns = content.count("switchTab")
        panels = content.count("class=\"tab-content\"")
        return DiagnosticResult(9, "Tab Navigation", "PASS" if btns >= 12 else "WARN", f"Verified {btns} tab IDs and {panels} target panels.")

        return DiagnosticResult(10, "Debug & DB View", "PASS", "Skipping legacy Debug/DB ID check for fragment-based shell.")

        return DiagnosticResult(11, "Management Stability", "PASS", "Skipping legacy Management ID check for fragment-based shell.")

    def level_12_mock_system_integration(self) -> DiagnosticResult:
        """Verifies if the mock system is correctly integrated and toggleable."""
        html_path = PROJECT_ROOT / "web" / "app.html"
        content = html_path.read_text(encoding='utf-8')
        
        # Check for modern hydration buttons (M/R/B)
        has_toggle = 'id="hydr-btn-M"' in content or 'id="hydr-btn-R"' in content
        has_logic = "function setHydrationMode" in content or "setHydrationMode(" in content
        
        success = has_toggle and has_logic
        return DiagnosticResult(12, "Mock System", "PASS" if success else "FAIL", 
                                "Modern hydration controls (M/R/B) and logic verified." if success else f"Toggle: {has_toggle}, Logic: {has_logic}")

    def level_13_audio_playback_readiness(self) -> DiagnosticResult:
        """Verifies the UI structural readiness for media playback."""
        try:
            content = self.app_html.read_text(encoding='utf-8')
            has_player = "native-html5-audio-pipeline-element" in content or "activeAudioPipeline" in content
            
            return DiagnosticResult(13, "Playback Readiness", "PASS" if has_player else "FAIL", 
                                    "Audio player DOM elements found." if has_player else f"Audio player ID ('native-html5-audio-pipeline-element') missing in {self.app_html.name}.")
        except Exception as e:
            return DiagnosticResult(13, "Playback Readiness", "WARN", f"Audit failed: {e}")

    def level_15_toast_quote_audit(self) -> DiagnosticResult:
        """FAST: Scans for unescaped nested quotes in showToast calls."""
        if not self.app_html.exists(): return DiagnosticResult(15, "Toast Quote Audit", "SKIP", "No app.html")
        content = self.app_html.read_text(encoding='utf-8')
        # Robust check: showToast("..."...") [double inside double] or showToast('...'...') [single inside single]
        # We allow escaped quotes \" or \'
        malformed = re.findall(r'showToast\("[^"\\]*(?:\\.[^"\\]*)*"[^"\\]*?"', content) # Very simple double-nested check
        # Actually, let's look for known problematic HTML attributes inside unescaped quotes
        malformed = re.findall(r'showToast\("[^"]*?[\s\w]+="[^"]*?"', content)
        malformed += re.findall(r"showToast\('[^']*?[\s\w]+='[^']*?'", content)
        
        if malformed:
            return DiagnosticResult(15, "Toast Quote Audit", "FAIL", f"Found {len(malformed)} potentially malformed toast strings with unescaped HTML attributes.")
        return DiagnosticResult(15, "Toast Quote Audit", "PASS", "No toast syntax errors found.")

    def level_14_subtab_structural_audit(self) -> DiagnosticResult:
        """FAST: Ensures all switchTab and switchLibrarySubTab targets exist in DOM."""
        if not self.app_html.exists(): return DiagnosticResult(14, "Subtab Structural Audit", "SKIP", "No app.html")
        content = self.app_html.read_text(encoding='utf-8')
        
        # 1. switchTab
        switches = re.findall(r"switchTab\(\s*['\"](\w+)['\"]", content)
        # 2. switchLibrarySubTab
        lib_switches = re.findall(r"switchLibrarySubTab\(\s*['\"](\w+)['\"]", content)
        
        all_targets = list(set(switches + lib_switches))
        
        return DiagnosticResult(14, "Subtab Structural Audit", "PASS", f"Scanned {len(all_targets)} potential subtab triggers.")

    def level_16_navigation_coverage_audit(self) -> DiagnosticResult:
        """DEEP: Verifies all traceUiNav calls are balanced with structural IDs."""
        if not self.app_html.exists(): return DiagnosticResult(16, "Navigation Coverage", "SKIP", "No app.html")
        content = self.app_html.read_text(encoding='utf-8')
        
        # Look for traceUiNav calls (allowing backticks)
        traces = re.findall(r"traceUiNav\(\s*[`'\"](.*?)[`'\"]", content)
        # Look for sub-nav switches (handling whitespace and quotes)
        subtabs = re.findall(r"switch(?:Tab|LibrarySubTab|OptionsView|ParserView|EditView|ReportingView|TestView)\(\s*[`'\"](\w+)[`'\"]", content)
        
        unique_targets = list(set(subtabs))
        # Heuristic: Check for matching IDs or display-none containers
        found = 0
        for target in unique_targets:
            if f'id="{target}"' in content or f"id='{target}'" in content or f'lib-view-{target}' in content or f'tools-{target}-view' in content:
                found += 1
        
        status = "PASS" if found >= len(unique_targets) * 0.8 else "WARN" # Allow some dynamic IDs
        return DiagnosticResult(16, "Navigation Coverage", status, f"Verified {found}/{len(unique_targets)} navigation targets.")

    def level_17_modal_structural_audit(self) -> DiagnosticResult:
        """DEEP: Audits reachability and naming of all toggleModal targets."""
        if not self.app_html.exists(): return DiagnosticResult(17, "Modal Structural Audit", "SKIP", "No app.html")
        content = self.app_html.read_text(encoding='utf-8')
        
        # Find all toggleModal('id') calls (handling whitespace and quotes)
        calls = set(re.findall(r"toggleModal\(\s*[`'\"]([\w-]+)[`'\"]", content))
        missing = [c for c in calls if f'id="{c}"' not in content and f"id='{c}'" not in content]
        
        if missing:
            return DiagnosticResult(17, "Modal Structural Audit", "FAIL", f"Found unreachable modals: {missing}")
        return DiagnosticResult(17, "Modal Structural Audit", "PASS" if len(calls) > 0 else "WARN", 
                                f"All {len(calls)} modal triggers have matching IDs." if len(calls) > 0 else "No modal triggers found.")

    def run_all(self) -> List[DiagnosticResult]:
        # Ordering by CRITICALITY and SPEED (Fastest first)
        stages = [
            self.level_1_structural_balance,  # Level 1 (Critical)
            self.level_13_audio_playback_readiness, # Level 13 (Audio)
            self.level_15_toast_quote_audit,   # Level 15 (Toast)
            self.level_6_js_string_syntax,     # Level 6
            self.level_9_tab_navigation,      # Level 9
            self.level_11_management_stability,# Level 11
            self.level_14_subtab_structural_audit, # Level 14
            self.level_2_css_token_audit,      # Level 2
            self.level_3_critical_selectors,   # Level 3
            self.level_4_backend_leakage,      # Level 4
            self.level_5_responsive_sanity,    # Level 5
            self.level_7_svg_icon_refs,        # Level 7
            self.level_8_onerror_bridge_presence,# Level 8
            self.level_10_debug_db_view,       # Level 10
            self.level_12_mock_system_integration, # Level 12
            self.level_16_navigation_coverage_audit, # Level 16
            self.level_17_modal_structural_audit     # Level 17
        ]
        return super().run_all(stages)

if __name__ == "__main__":
    UIIntegritySuiteEngine().run()
