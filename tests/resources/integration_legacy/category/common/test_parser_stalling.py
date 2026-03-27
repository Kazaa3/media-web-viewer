import pytest
pytest.importorskip("selenium")
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import time
import os
import sys
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tests.basic.utils.test_utils import manage_app_instance, wait_for_app, robust_action, save_screenshot

class TestParserStalling(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        preferred = int(os.environ.get("MWV_PORT", 0)) or None
        cls.app_process = None
        decision, using_existing, cls.port = manage_app_instance(preferred)
        
        if decision == "START_NEW":
            env = os.environ.copy()
            env["MWV_PORT"] = str(cls.port)
            env["MWV_FORCE_NEW_SESSION"] = "1"
            cls.app_process = subprocess.Popen(
                [sys.executable, "src/core/main.py"],
                cwd=os.path.abspath(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))),
                env=env
            )
            if not wait_for_app(cls.port): raise RuntimeError("Failed to start")

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")
        cls.driver = webdriver.Chrome(options=options)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver'): cls.driver.quit()
        if cls.app_process: cls.app_process.terminate()

    def test_ui_responsiveness_during_scan(self):
        try:
            self.driver.get(f"http://localhost:{port}/app.html")
            wait = WebDriverWait(self.driver, 45)
            for tab in ["playlist", "library", "player"]:
                def switch():
                    btn = wait.until(EC.element_to_be_clickable((By.ID, f"{tab}-btn")))
                    self.driver.execute_script("arguments[0].scrollIntoView();", btn)
                    btn.click()
                    wait.until(lambda d: d.find_element(By.ID, f"{tab}-tab").is_displayed())
                    return True
                robust_action(self.driver, switch)
                self.assertTrue(self.driver.find_element(By.ID, f"{tab}-tab").is_displayed())
        except Exception:
            save_screenshot(self.driver, "test_parser_stalling_responsiveness_fail")
            raise

    def test_drag_and_drop_during_scan(self):
        try:
            self.driver.get(f"http://localhost:{port}/app.html")
            wait = WebDriverWait(self.driver, 60)
            wait.until(EC.element_to_be_clickable((By.ID, "playlist-btn"))).click()
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "media-item")))
            
            def perform_dd():
                items = self.driver.find_elements(By.CLASS_NAME, "media-item")
                if len(items) < 2: return False
                grab = items[0].find_element(By.CLASS_NAME, "grab-icon")
                target = items[1]
                self.driver.execute_script("arguments[0].scrollIntoView();", grab)
                actions = ActionChains(self.driver)
                actions.click_and_hold(grab).pause(0.5).move_to_element(target).pause(0.5).release().perform()
                return True

            robust_action(self.driver, perform_dd)
            time.sleep(2)
            self.assertGreaterEqual(len(self.driver.find_elements(By.CLASS_NAME, "media-item")), 2)
        except Exception:
            save_screenshot(self.driver, "test_parser_stalling_dd_fail")
            raise

if __name__ == "__main__":
    unittest.main()
