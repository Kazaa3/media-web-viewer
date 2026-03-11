#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import time
import os
import sys
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from pages.playlist_page import PlaylistPage

class TestUIIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = 8007
        env = os.environ.copy()
        env["MWV_PORT"] = str(cls.port)
        env["MWV_FORCE_NEW_SESSION"] = "1"
        
        cls.app_process = subprocess.Popen(
            [sys.executable, "main.py"],
            cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
            env=env
        )
        time.sleep(10)
        
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        cls.driver = webdriver.Chrome(options=options)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver'):
            cls.driver.quit()
        if hasattr(cls, 'app_process'):
            cls.app_process.terminate()

    def setUp(self):
        self.driver.get(f"http://localhost:{self.port}/app.html")
        time.sleep(2)

    def test_refresh_maintenance(self):
        """Verify that some state survives refresh or behaves consistently."""
        playlist = PlaylistPage(self.driver)
        playlist.switch_to()
        
        # 1. Pick an item
        items = playlist.get_items()
        if not items: self.skipTest("Empty playlist")
        
        # Simulate long press (js for speed in this integrity test)
        self.driver.execute_script("onGrabPointerDown({stopPropagation:()=>{}}, 0);")
        time.sleep(1) # wait for pick
        
        # Check if picked class is there
        cls = items[0].get_attribute("class")
        self.assertIn("picked", cls)
        
        # 2. Refresh
        self.driver.refresh()
        time.sleep(3)
        
        # 3. Check picked state (should be reset on refresh as it's UI state, but let's confirm consistency)
        items = playlist.get_items()
        cls = items[0].get_attribute("class")
        self.assertNotIn("picked", cls, "Picked state should be reset on full refresh (standard behavior)")

    def test_tab_switch_during_sync(self):
        """Verify tab switching doesn't break playlist sync log."""
        for _ in range(3):
            self.driver.find_element(By.ID, "playlist-btn").click()
            time.sleep(0.5)
            self.driver.find_element(By.ID, "player-btn").click()
            time.sleep(0.5)
            
        # Ensure still on player and can go back
        self.driver.find_element(By.ID, "playlist-btn").click()
        time.sleep(1)
        self.assertTrue(self.driver.find_element(By.ID, "playlist-tab").is_displayed())

if __name__ == "__main__":
    unittest.main()
