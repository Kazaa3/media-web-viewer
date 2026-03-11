#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import time
import os
import sys
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
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
        wait = WebDriverWait(self.driver, 20)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "media-item")))
        items = playlist.get_items()
        if not items: self.skipTest("Empty playlist")
        
        # Simulate long press via JS dispatch to trigger mousedown
        grab_icon = items[0].find_element(By.CLASS_NAME, "grab-icon")
        self.driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('mousedown', {bubbles: true}));", grab_icon)
        time.sleep(1) # wait for pick (400ms)
        
        # Check if picked class is there
        items = playlist.get_items() # re-fetch after renderPlaylist
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
        wait = WebDriverWait(self.driver, 20)
        for _ in range(3):
            wait.until(EC.element_to_be_clickable((By.ID, "playlist-btn"))).click()
            time.sleep(0.5)
            wait.until(EC.element_to_be_clickable((By.ID, "player-btn"))).click()
            time.sleep(0.5)
            
        # Ensure still on player and can go back
        wait.until(EC.element_to_be_clickable((By.ID, "playlist-btn"))).click()
        time.sleep(1)
        self.assertTrue(self.driver.find_element(By.ID, "playlist-tab").is_displayed())

if __name__ == "__main__":
    unittest.main()
