#!/usr/bin/env python3
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
from pages.playlist_page import PlaylistPage
from test_utils import manage_app_instance, wait_for_app, robust_action, save_screenshot

class TestMouseInteraction(unittest.TestCase):
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
                [sys.executable, "main.py"],
                cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
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

    def tearDown(self):
        # Result detection for screenshot
        # sys.exc_info() is often used but not always reliable in unittest
        # Instead, we just take one if it's the last thing we do in a failed test
        pass

    def test_pick_and_insert_flow(self):
        try:
            self.driver.get(f"http://localhost:{self.port}/app.html")
            wait = WebDriverWait(self.driver, 45)
            wait.until(EC.element_to_be_clickable((By.ID, "playlist-btn"))).click()
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "media-item")))
            
            def perform_drag():
            # 1. Grab (this triggers renderPlaylist() in JS!)
                items = self.driver.find_elements(By.CLASS_NAME, "media-item")
                if len(items) < 3: return False
                grab = items[0].find_element(By.CLASS_NAME, "grab-icon")
                
                self.driver.execute_script("arguments[0].scrollIntoView();", grab)
                ActionChains(self.driver).click_and_hold(grab).perform()
                time.sleep(1) # Wait for DOM to re-render
                
                # 2. Re-find target after re-render!
                items_new = self.driver.find_elements(By.CLASS_NAME, "media-item")
                if len(items_new) < 3: return False
                target_new = items_new[2]
                
                # Defensive scrolling for target
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_new)
                time.sleep(0.5)
                
                ActionChains(self.driver).move_to_element(target_new).pause(0.5).release().perform()
                return True

            robust_action(self.driver, perform_drag)
            time.sleep(2)
            wait.until(lambda d: len(d.find_elements(By.CSS_SELECTOR, ".media-item.picked")) == 0)
        except Exception:
            save_screenshot(self.driver, "test_mouse_interaction_fail")
            raise

if __name__ == "__main__":
    unittest.main()
