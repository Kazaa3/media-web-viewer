#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: GUI / E2E Test
# Eingabewerte: Browser UI
# Ausgabewerte: Visual consistency results
# Testdateien: web/app.html
# Kommentar: Selenium-based test to verify tab switching and refresh logic in the GUI.

import unittest
import time
import os
import subprocess
import signal
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

class TestGUITabsRefresh(unittest.TestCase):
    """
    @brief E2E Tests for verifying GUI tab switching and content rendering.
    """

    @classmethod
    def setUpClass(cls):
        # Set fixed port for testing
        cls.port = 8000
        env = os.environ.copy()
        env["MWV_PORT"] = str(cls.port)

        # Start the application in a subprocess
        cls.log_file = open("test_app_startup.log", "w")
        cls.app_process = subprocess.Popen(
            [os.sys.executable, "main.py"],
            cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
            stdout=cls.log_file,
            stderr=subprocess.STDOUT,
            env=env
        )
        time.sleep(10)  # Wait for app to initialize and start server

        # Initialize Selenium (Chrome Headless)
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.set_window_size(1280, 1024)

    @classmethod
    def tearDownClass(cls):
        cls.driver.quit()
        # Gracefully stop the app
        cls.app_process.terminate()
        try:
            cls.app_process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            cls.app_process.kill()

    def setUp(self):
        self.driver.get("http://localhost:8000")
        # Wait for the main container
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "app-container"))
        )

    def test_tab_switching_all(self):
        """Cycle through all tabs and verify they display content."""
        tabs = [
            "library", "playlist", "browser", "parser", 
            "edit", "options", "logbuch", "debug", "tests"
        ]
        
        for tab_id in tabs:
            with self.subTest(tab=tab_id):
                # Find the tab button (sidebar-nav items)
                # Buttons usually have onclick="switchTab('tab_id', ...)"
                try:
                    xpath = f"//div[contains(@class, 'sidebar-nav')]//div[contains(@onclick, \"switchTab('{tab_id}')\")]"
                    btn = WebDriverWait(self.driver, 5).until(
                        EC.element_to_be_clickable((By.XPATH, xpath))
                    )
                    btn.click()
                    time.sleep(0.5) # Wait for animation/render

                    # Verify tab content is visible
                    target_tab = self.driver.find_element(By.ID, f"{tab_id}-tab")
                    self.assertTrue(target_tab.is_displayed(), f"Tab {tab_id} is not displayed after click")
                    
                    # Basic content check (not empty)
                    inner_html = target_tab.get_attribute("innerHTML").strip()
                    self.assertTrue(len(inner_html) > 0, f"Tab {tab_id} has no content")
                    
                    print(f"✅ Verified tab: {tab_id}")
                except (TimeoutException, Exception) as e:
                    self.fail(f"Failed to switch to or verify tab {tab_id}: {str(e)}")

    def test_parser_tab_categories(self):
        """Verify the new 'Spiel' and 'Beigabe' categories exist in the Options tab."""
        # Switch to Options tab
        xpath = "//div[contains(@class, 'sidebar-nav')]//div[contains(@onclick, \"switchTab('options')\")]"
        btn = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        btn.click()
        time.sleep(1)

        # Check for cat-spiel and cat-beigabe checkboxes
        spiel_cb = self.driver.find_element(By.ID, "cat-spiel")
        beigabe_cb = self.driver.find_element(By.ID, "cat-beigabe")
        
        self.assertIsNotNone(spiel_cb, "PC-Spiele checkbox missing")
        self.assertIsNotNone(beigabe_cb, "Beigaben checkbox missing")
        
        print("✅ Verified new categories in Options tab")

    def test_parser_tab_population(self):
        """Verify that the Parser tab populates its list."""
        xpath = "//div[contains(@class, 'sidebar-nav')]//div[contains(@onclick, \"switchTab('parser')\")]"
        btn = WebDriverWait(self.driver, 5).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        btn.click()
        time.sleep(1)

        parser_list = self.driver.find_element(By.ID, "parser-list")
        items = parser_list.find_elements(By.CLASS_NAME, "parser-item")
        
        self.assertTrue(len(items) > 0, "Parser list is empty")
        print(f"✅ Verified Parser tab population: {len(items)} parsers found")

if __name__ == "__main__":
    unittest.main()
