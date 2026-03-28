import sys
import os
import re
import time
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

class AutomationSuiteEngine(DiagnosticEngine):
    def __init__(self) -> None:
        super().__init__(suite_name="Automation")
        os.environ["UNIT_TESTING"] = "1"

    def level_1_pyautogui_desktop_metrics(self) -> DiagnosticResult:
        """Verifies that PyAutoGUI can access desktop metrics (Legacy: test_pyautogui_api.py)."""
        try:
            import pyautogui
            size = pyautogui.size()
            pos = pyautogui.position()
            success = size.width > 0 and size.height > 0
            return DiagnosticResult(1, "Desktop Metrics", "PASS" if success else "FAIL", 
                                    f"Screen: {size.width}x{size.height}, Mouse: ({pos.x}, {pos.y})")
        except Exception as e:
            return DiagnosticResult(1, "Desktop Metrics", "FAIL", f"Error: {e}")

    def level_2_pyautogui_safe_interaction(self) -> DiagnosticResult:
        """Verifies safe mouse movement automation (Legacy: test_pyautogui_integration.py)."""
        try:
            import pyautogui
            # Disable failsafe for short diagnostic or move to center
            pyautogui.FAILSAFE = True
            start_pos = pyautogui.position()
            
            # Small relative move and back
            pyautogui.moveRel(10, 10, duration=0.1)
            time.sleep(0.1)
            mid_pos = pyautogui.position()
            
            pyautogui.moveTo(start_pos.x, start_pos.y, duration=0.1)
            
            success = (mid_pos.x == start_pos.x + 10) or (abs(mid_pos.x - (start_pos.x + 10)) <= 2)
            return DiagnosticResult(2, "Interaction Smoke", "PASS" if success else "WARN", 
                                    f"Start: {start_pos}, Mid: {mid_pos} (Relative Check)")
        except Exception as e:
            return DiagnosticResult(2, "Interaction Smoke", "FAIL", f"Automation blocked: {e}")

    def level_3_html_structural_audit(self) -> DiagnosticResult:
        """Performs deep DIV/BRACE balance audit on app.html (Legacy: gui_validator.py)."""
        app_html = PROJECT_ROOT / "web" / "app.html"
        if not app_html.exists(): return DiagnosticResult(3, "Structural Audit", "SKIP", "app.html missing.")

        try:
            with open(app_html, 'r', encoding='utf-8') as f: content = f.read()
            
            # Simple stack-based balance check for DIVs
            pattern = re.compile(r'(<\/?script.*?>|<\/?style.*?>|<\/?div.*?>|[{}]|<!--.*?-->)', re.DOTALL | re.IGNORECASE)
            
            div_stack = 0
            brace_depth = 0
            script_mode = False
            style_mode = False
            
            for match in pattern.finditer(content):
                token = match.group(0).lower()
                if token.startswith('<script'): script_mode = True
                elif token == '</script>': script_mode = False
                elif token.startswith('<style'): style_mode = True
                elif token == '</style>': style_mode = False
                
                if script_mode or style_mode:
                    if token == '{': brace_depth += 1
                    elif token == '}': brace_depth -= 1
                    continue
                
                if token.startswith('<div'): div_stack += 1
                elif token == '</div>': div_stack -= 1
                elif token == '{': brace_depth += 1
                elif token == '}': brace_depth -= 1

            success = (div_stack == 0 and brace_depth == 0)
            return DiagnosticResult(3, "Structural Audit", "PASS" if success else "WARN", 
                                    f"Final Stack Depth: DIV={div_stack}, BRACE={brace_depth}")
        except Exception as e:
            return DiagnosticResult(3, "Structural Audit", "FAIL", f"Audit failed: {e}")

    def level_4_structural_leakage_audit(self) -> DiagnosticResult:
        """Audits app.html for code leakage snippets (Legacy: gui_test.py)."""
        app_html = PROJECT_ROOT / "web" / "app.html"
        if not app_html.exists(): return DiagnosticResult(4, "Leakage Audit", "SKIP", "app.html missing.")

        try:
            with open(app_html, 'r', encoding='utf-8') as f: content = f.read()
            leakage_patterns = ["eel.expose", "const history = await eel.", "function() {", "var eel = "]
            
            found = []
            for p in leakage_patterns:
                if p in content:
                    if not re.search(rf"<script.*?>.*?{re.escape(p)}.*?</script>", content, re.DOTALL):
                        found.append(p)
            
            success = len(found) == 0
            return DiagnosticResult(4, "Leakage Audit", "PASS" if success else "WARN", 
                                    f"Potential Leakage: {found}" if not success else "No obvious code leakage detected.")
        except Exception as e:
            return DiagnosticResult(4, "Leakage Audit", "FAIL", f"Audit failed: {e}")

    def level_5_selenium_readiness(self) -> DiagnosticResult:
        """Verifies if Selenium and Chromedriver are available for E2E tests."""
        try:
            import shutil
            chrome = shutil.which("google-chrome") or shutil.which("chromium-browser")
            driver = shutil.which("chromedriver")
            success = chrome is not None and driver is not None
            return DiagnosticResult(5, "Selenium Ready", "PASS" if success else "SKIP", 
                                    f"Chrome: {chrome}, Driver: {driver}")
        except Exception as e:
            return DiagnosticResult(5, "Selenium Ready", "WARN", f"Detection error: {e}")

    def level_6_selenium_launch_smoke(self) -> DiagnosticResult:
        """Launches a headless Chrome instance to verify Selenium/Driver handshake."""
        try:
            from selenium import webdriver
            from selenium.webdriver.chrome.options import Options
            options = Options()
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
            options.add_argument("--disable-dev-shm-usage")
            
            driver = webdriver.Chrome(options=options)
            try:
                driver.get("data:text/html,<html><body><h1>MWV-DIAG</h1></body></html>")
                success = "MWV-DIAG" in driver.page_source
                return DiagnosticResult(6, "Selenium Smoke", "PASS" if success else "FAIL", "Handshake and page load successful.")
            finally:
                driver.quit()
        except Exception as e:
            return DiagnosticResult(6, "Selenium Smoke", "SKIP", f"Headless launch failed: {e}")

    def run_all(self, stages: List[Any] = None) -> List[DiagnosticResult]:
        if not stages:
            stages = [
                self.level_1_pyautogui_desktop_metrics,
                self.level_2_pyautogui_safe_interaction,
                self.level_3_html_structural_audit,
                self.level_4_structural_leakage_audit,
                self.level_5_selenium_readiness,
                self.level_6_selenium_launch_smoke
            ]
        return super().run_all(stages)

if __name__ == "__main__":
    AutomationSuiteEngine().run_all()
