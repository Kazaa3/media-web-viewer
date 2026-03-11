#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import time
import os
import sys
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By

class TestParserStalling(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = 8008
        env = os.environ.copy()
        env["MWV_PORT"] = str(cls.port)
        env["MWV_FORCE_NEW_SESSION"] = "1"
        # We don't need a special flag here, just normal startup which we know is slow
        
        cls.app_process = subprocess.Popen(
            [sys.executable, "main.py"],
            cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
            env=env
        )
        # Give it a bit but not enough to finish all parsing if it's large
        time.sleep(5)
        
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        cls.driver = webdriver.Chrome(options=options)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver'):
            cls.driver.quit()
        if hasattr(cls, 'app_process'):
            cls.app_process.terminate()

    def test_ui_responsiveness_during_scan(self):
        """Verify tabs can be switched while scanner is likely still running."""
        self.driver.get(f"http://localhost:{self.port}/app.html")
        time.sleep(2)
        
        # Try switching tabs rapidly
        tabs = ["playlist", "library", "player", "settings"]
        for tab in tabs:
            btn = self.driver.find_element(By.ID, f"{tab}-btn")
            btn.click()
            time.sleep(0.3)
            tab_content = self.driver.find_element(By.ID, f"{tab}-tab")
            self.assertTrue(tab_content.is_displayed(), f"Tab {tab} should be visible after click")

    def test_playlist_reorder_call_during_scan(self):
        """Verify that even if scans are ongoing, a reorder call (if playlist exists) is attempted."""
        self.driver.get(f"http://localhost:{self.port}/app.html")
        time.sleep(5) # wait for SOME items
        
        # Switch to playlist
        self.driver.find_element(By.ID, "playlist-btn").click()
        time.sleep(1)
        
        # Check if we have items. If not, we might need to wait more or have fixed media.
        items = self.driver.find_elements(By.CLASS_NAME, "media-item")
        if not items:
            print("No items yet, scanner might be slow. Retrying once...")
            time.sleep(10)
            items = self.driver.find_elements(By.CLASS_NAME, "media-item")
        
        if items:
            # Try to click move up (global button)
            move_up = self.driver.find_element(By.ID, "pl-move-up")
            # Should not crash the UI
            move_up.click()
            time.sleep(1)

if __name__ == "__main__":
    unittest.main()
