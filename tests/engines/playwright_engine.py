import sys
import os
import time
from pathlib import Path
from typing import List, Dict, Any, Optional

from src.core.config_master import PROJECT_ROOT, DB_FILENAME, TEST_DIR, DATA_DIR
sys.path.append(str(PROJECT_ROOT))

from tests.engines.test_base import DiagnosticEngine, DiagnosticResult

class PlaywrightEngine(DiagnosticEngine):
    """
    Modern diagnostic engine using Playwright for high-fidelity DOM testing.
    Replaces flaky Selenium sessions with stable CDP interactions.
    """
    
    def __init__(self, headless: bool = True):
        super().__init__(suite_name="Playwright")
        self.headless = headless
        self.browser = None
        self.context = None
        self.page = None

    def level_1_environment_handshake(self) -> DiagnosticResult:
        """Verifies Playwright installation and basic browser launch."""
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                version = browser.version
                browser.close()
                return DiagnosticResult(1, "Handshake", "PASS", f"Chromium launched. Version: {version}")
        except Exception as e:
            return DiagnosticResult(1, "Handshake", "FAIL", f"Playwright error: {e}")

    def level_2_dom_rendering_smoke(self) -> DiagnosticResult:
        """Launches the app and verifies basic HTML structure (header/tabs)."""
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                page = browser.new_page()
                # Use standard MWV port
                port = int(os.environ.get("MWV_PORT", 8345))
                url = f"http://127.0.0.1:{port}/app.html"
                
                try:
                    page.goto(url, timeout=5000)
                    title = page.title()
                    tabs = page.query_selector_all(".tab-btn")
                    count = len(tabs)
                    success = count > 0
                    return DiagnosticResult(2, "DOM Smoke", "PASS" if success else "FAIL", 
                                            f"URL: {url}, Title: {title}, Tabs found: {count}")
                except Exception as e:
                    return DiagnosticResult(2, "DOM Smoke", "FAIL", f"Page load failed: {e}")
                finally:
                    browser.close()
        except Exception as e:
            return DiagnosticResult(2, "DOM Smoke", "FAIL", f"Browser error: {e}")

    def level_3_tools_tab_visibility(self) -> DiagnosticResult:
        """Verifies that the new 'Tools' tab is correctly identified and clickable."""
        try:
            from playwright.sync_api import sync_playwright
            with sync_playwright() as p:
                browser = p.chromium.launch(headless=self.headless)
                page = browser.new_page()
                port = int(os.environ.get("MWV_PORT", 8345))
                page.goto(f"http://127.0.0.1:{port}/app.html", timeout=5000)
                
                # Check for the Tools tab trigger
                tools_btn = page.query_selector("button[onclick*='switchTab'][onclick*='tools']")
                if not tools_btn:
                    return DiagnosticResult(3, "Tools Tab", "FAIL", "Tools tab button not found.")
                
                tools_btn.click()
                time.sleep(0.5)
                
                # Check for the tools-tab container (ID fix verification)
                tools_pane = page.query_selector("#tools-tab")
                is_visible = tools_pane.is_visible() if tools_pane else False
                
                return DiagnosticResult(3, "Tools Tab", "PASS" if is_visible else "FAIL", 
                                        "Tools tab is visible and ID mapped correctly." if is_visible else "Tools tab did not render after click.")
                browser.close()
        except Exception as e:
            return DiagnosticResult(3, "Tools Tab", "FAIL", f"Verification error: {e}")

    def run_all(self, stages: List[Any] = None) -> List[DiagnosticResult]:
        if not stages:
            stages = [
                self.level_1_environment_handshake,
                self.level_2_dom_rendering_smoke,
                self.level_3_tools_tab_visibility
            ]
        return super().run_all(stages)

if __name__ == "__main__":
    PlaywrightEngine().run()
