import unittest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
import sys

from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

class GuiTestSuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        service = Service(ChromeDriverManager().install())
        cls.driver = webdriver.Chrome(service=service, options=chrome_options)
        cls.base_url = "http://localhost:8345/app.html" # Fixed URL

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()

    def test_page_load(self):
        self.driver.get(self.base_url)
        # Fix: Sidebar ID is 'main-sidebar' in app.html
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, "main-sidebar"))
        )
        
        # Wait for title to synchronize (using WebDriverWait for robustness)
        try:
            WebDriverWait(self.driver, 10).until(
                lambda driver: "dict v1.34" in driver.title
            )
        except Exception:
            # Fallback for debug
            title = self.driver.title
            print(f"DEBUG: Current Title: {title}")
            self.assertIn("dict v1.34", title, f"Unexpected title: {title}")
        
        # Verify Player Tab (Active Queue) is the default start page
        player_tab = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "active-queue-tab-trigger"))
        )
        classes = player_tab.get_attribute("class")
        
        if "active" not in classes:
            print("FAILURE: Player tab NOT active on startup!")
            logs = self.driver.get_log('browser')
            for log in logs:
                print(f"Browser Console: {log['message']}")
        
        self.assertIn("active", classes, f"Player tab should be active by default. Current classes: {classes}")

    def test_no_js_errors(self):
        self.driver.get(self.base_url)
        time.sleep(3) # Wait for initial scripts
        logs = self.driver.get_log('browser')
        # Filter out 404 errors for assets like favicon.ico
        errors = [log for log in logs if log['level'] == 'SEVERE' and '404' not in log['message']]
        for error in errors:
            print(f"Browser Error: {error['message']}")
        self.assertEqual(len(errors), 0, f"Found {len(errors)} real JS errors in console")

    def test_structural_leakage(self):
        # Check if code literals or unescaped tags are visible in the body
        self.driver.get(self.base_url)
        body_text = self.driver.find_element(By.TAG_NAME, "body").text
        # Look for leaking JS/HTML snippets
        leakage_patterns = [
            "</script>",
            "eel.expose",
            "const history = await eel.get_benchmark_results()",
            "function()",
            "const ",
            "let "
        ]
        for pattern in leakage_patterns:
            self.assertNotIn(pattern, body_text, f"Detected structural leakage: '{pattern}' found in UI text")

    def test_tabs_integrity(self):
        self.driver.get(self.base_url)
        # Using correct mapping from app.html
        tabs_to_triggers = {
            "library": "coverflow-library-tab-trigger",
            "options": "system-registry-tab-trigger",
            "debug": "telemetry-inspector-tab-trigger",
            "vlc": "media-orchestrator-tab-trigger"
        }
        for tab_name, trigger_id in tabs_to_triggers.items():
            btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, trigger_id))
            )
            btn.click()
            time.sleep(1) # Allow for transition

if __name__ == "__main__":
    unittest.main()
