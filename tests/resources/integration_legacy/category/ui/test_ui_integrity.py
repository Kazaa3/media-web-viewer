#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: UI Integration
# Eingabewerte: web/app.html
# Ausgabewerte: Tag-Balance, Tab-IDs, tabMap Status
# Testdateien: tests/test_ui_integrity.py
# ERWEITERUNGEN (TODO): [ ] Mocking-Tests für Session-Recovery, [ ] Browser-Launch Race-Condition Tests
# KOMMENTAR: Validiert die HTML-Struktur und JS-Tab-Konfiguration.
# VERWENDUNG: python3 tests/integration/category/ui/test_ui_integrity.py

"""
KATEGORIE: UI Integration
ZWECK: Validiert die HTML-Struktur und JS-Tab-Konfiguration des Frontends.
EINGABEWERTE: web/app.html
AUSGABEWERTE: Tag-Balance, Tab-IDs, tabMap Status
TESTDATEIEN: tests/test_ui_integrity.py
ERWEITERUNGEN (TODO): [ ] Mocking-Tests für Session-Recovery, [ ] Browser-Launch Race-Condition Tests
KOMMENTAR: Validiert die HTML-Struktur und JS-Tab-Konfiguration.
VERWENDUNG: python3 tests/integration/category/ui/test_ui_integrity.py
"""

import pytest
pytest.importorskip("selenium")

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
from tests.selenium.pages.playlist_page import PlaylistPage
from tests.basic.utils.test_utils import manage_app_instance, wait_for_app

class TestUIIntegrity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        preferred = int(os.environ.get("MWV_PORT", 0)) or None
        cls.app_process = None
        
        decision, using_existing, cls.port = manage_app_instance(preferred)
        
        if decision == "START_NEW":
            print(f"Starting new app instance on port {cls.port}...")
            env = os.environ.copy()
            env["MWV_PORT"] = str(cls.port)
            env["MWV_FORCE_NEW_SESSION"] = "1"
            
            cls.app_process = subprocess.Popen(
                [sys.executable, "src/core/main.py"],
                cwd=os.path.abspath(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))),
                env=env
            )
            if not wait_for_app(cls.port):
                cls.tearDownClass()
                raise RuntimeError(f"App failed to start on port {cls.port}")
        elif decision == "FAIL":
            raise RuntimeError("No existing app session found and starting new one is disabled.")

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.set_window_size(1280, 1024)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver'):
            cls.driver.quit()
        if cls.app_process:
            print(f"Terminating test-started app process (PID {cls.app_process.pid})...")
            cls.app_process.terminate()

    def setUp(self):
        self.driver.get(f"http://localhost:{port}/app.html")
        time.sleep(2)

    def test_refresh_maintenance(self):
        """Verify that some state survives refresh or behaves consistently."""
        playlist = PlaylistPage(self.driver)
        playlist.switch_to()
        
        # 1. Pick an item via ActionChains
        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "media-item")))
        items = playlist.get_items()
        if not items: self.skipTest("Empty playlist")
        
        grab_icon = items[0].find_element(By.CLASS_NAME, "grab-icon")
        actions = ActionChains(self.driver)
        actions.click_and_hold(grab_icon).perform()
        time.sleep(1) 
        
        # Check if picked class is there
        items = playlist.get_items() 
        cls = items[0].get_attribute("class")
        self.assertIn("picked", cls, "Item should have 'picked' class while mouse is down on handle")
        
        # 2. Refresh
        self.driver.refresh()
        time.sleep(3)
        
        # 3. Check picked state
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "media-item")))
        items = playlist.get_items()
        cls = items[0].get_attribute("class")
        self.assertNotIn("picked", cls, "Picked state should be reset on full refresh")

    def test_tab_switch_during_sync(self):
        """Verify tab switching doesn't break playlist sync log."""
        wait = WebDriverWait(self.driver, 30)
        wait.until(EC.element_to_be_clickable((By.ID, "playlist-btn")))
        
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
