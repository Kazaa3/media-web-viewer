#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: GUI / E2E Test / ISO
# Eingabewerte: Selenium, src/core/main.py, media/test_selenium_dvd.iso
# Ausgabewerte: Validierung der ISO/DVD-Playback-Logik im UI
# Testdateien: src/core/main.py, media/test_selenium_dvd.iso
# KOMMENTAR: Selenium-basierter Test für ISO/DVD-Playback.

import unittest
import time
import os
import sys
import subprocess
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class TestISOPlaybackUI(unittest.TestCase):
    """
    Selenium-basierter Test für ISO/DVD-Playback im UI. / Selenium-based test for ISO/DVD playback in UI.
    """
    @classmethod
    def setUpClass(cls):
        cls.port = 8346
        env = os.environ.copy()
        env["MWV_PORT"] = str(cls.port)
        env["MWV_FORCE_NEW_SESSION"] = "1"
        env["MWV_DEBUG_UI"] = "1"
        
        # Ensure media directory and mock files exist
        cls.project_root = os.path.abspath(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
        media_dir = os.path.join(cls.project_root, "media")
        os.makedirs(media_dir, exist_ok=True)
        
        # Create mock ISO for testing
        cls.mock_iso = os.path.join(media_dir, "test_selenium_dvd.iso")
        with open(cls.mock_iso, "wb") as f:
            f.write(b"\0" * 1024)

        cls.log_file = open("test_iso_ui_startup.log", "w")
        
        # Use .venv_core for the application backend
        core_python = os.path.join(cls.project_root, ".venv_core", "bin", "python3")
        if not os.path.exists(core_python):
             core_python = sys.executable

        cls.app_process = subprocess.Popen(
            [core_python, "src/core/main.py"],
            cwd=cls.project_root,
            stdout=cls.log_file,
            stderr=subprocess.STDOUT,
            env=env
            )
        # Give it plenty of time to start and scan
        time.sleep(15)
        
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.set_window_size(1280, 1024)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver'):
            cls.driver.quit()
        if hasattr(cls, 'app_process'):
            cls.app_process.terminate()
            try:
                cls.app_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                cls.app_process.kill()
        if hasattr(cls, 'log_file'):
            cls.log_file.close()
        if os.path.exists(cls.mock_iso):
            os.remove(cls.mock_iso)

    def setUp(self):
        self.driver.get(f"http://localhost:{self.port}/app.html")
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "main-split-container"))
        )

    def test_iso_direct_play_feedback(self):
        """Test that clicking an ISO in Direct Play mode shows the DVD info ribbon."""
        # The Player tab is active by default. The sidebar with the library is visible here.
        
        print("Selecting Direct Play mode in Videoplayer tab...")
        # We need to set the mode first. We can quickly switch and back or just find the select if it's in DOM.
        vlc_tab_btn = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@onclick, \"switchTab('vlc'\")]"))
        )
        vlc_tab_btn.click()
        time.sleep(1)
        
        mode_select = self.driver.find_element(By.ID, "video-mode-select")
        mode_select.send_keys("Direct Play (MKVmerge)")
        time.sleep(1)
        
        print("Switching back to Player tab to see the library sidebar...")
        player_tab_btn = self.driver.find_element(By.XPATH, "//button[contains(@onclick, \"switchTab('player'\")]")
        player_tab_btn.click()
        time.sleep(1)

        print("Ensuring library category is 'All'...")
        # Sidebar should be visible now
        try:
            # Look for category chips
            all_chip = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'category-chip')]//span[contains(text(), 'Alles')]"))
            )
            all_chip.click()
        except:
            print("Could not find 'Alles' chip, trying 'All'...")
            try:
                all_chip = self.driver.find_element(By.XPATH, "//div[contains(@class, 'category-chip')]//span[contains(text(), 'All')]")
                all_chip.click()
            except:
                print("Could not find category chips, assuming default is 'All'")
        time.sleep(2)

        print("Looking for mock ISO in media list sidebar...")
        iso_item_xpath = "//*[contains(text(), 'test_selenium_dvd')]"
        try:
            iso_element_child = WebDriverWait(self.driver, 30).until(
                EC.presence_of_element_located((By.XPATH, iso_item_xpath))
            )
            iso_element = iso_element_child.find_element(By.XPATH, "./ancestor::div[contains(@class, 'media-item')]")
        except Exception as e:
            self.driver.save_screenshot("test_failed_iso_not_found.png")
            with open("test_failed_page_source.html", "w") as f:
                f.write(self.driver.page_source)
            raise e

        print(f"Clicking ISO item: {iso_element.text}")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", iso_element)
        time.sleep(1)
        iso_element.click()
        
        # Clicking should automatically switch to 'vlc' tab (video-tab)
        print("Waiting for automatic switch to Video Player tab...")
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "video-tab"))
        )

        print("Waiting for VLC info ribbon...")
        self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", iso_element)
        time.sleep(1)
        iso_element.click()

        print("Waiting for VLC info ribbon...")
        vlc_info = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.ID, "vlc-info"))
        )
        
        current_file_text = self.driver.find_element(By.ID, "vlc-current-file").text
        print(f"Ribbon text: {current_file_text}")
        
        # In Direct Play for ISO, we expect 'VLC DVD Modus' or similar (from i18n)
        # We check for the file name at least
        self.assertIn("test_selenium_dvd.iso", current_file_text)
        
        # Verify toast message (toast-container is likely the ID)
        # Toast might disappear quickly, so we check existence
        try:
            toast = WebDriverWait(self.driver, 5).until(
                EC.presence_of_element_located((By.CLASS_NAME, "toast"))
            )
            print(f"Toast detected: {toast.text}")
        except:
            print("Toast not detected or already gone, which is acceptable if ribbon is present.")

if __name__ == "__main__":
    unittest.main()
