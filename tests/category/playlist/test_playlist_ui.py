#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: GUI / E2E Test
# Kommentar: Selenium-based test for Playlist reordering and remove logic.

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

class TestPlaylistUI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = 8003
        env = os.environ.copy()
        env["MWV_PORT"] = str(cls.port)
        env["MWV_FORCE_NEW_SESSION"] = "1"
        env["MWV_DEBUG_UI"] = "1"
        
        cls.fake_playlist_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "test_fake_playlist.json"))
        with open(cls.fake_playlist_path, "w", encoding="utf-8") as f:
            json.dump([
                {"name": "Track A", "path": "/fake/A.mp3"},
                {"name": "Track B", "path": "/fake/B.mp3"},
                {"name": "Track C", "path": "/fake/C.mp3"}
            ], f)

        cls.log_file = open("test_playlist_startup.log", "w")
        cls.app_process = subprocess.Popen(
            [sys.executable, "src.core.main.py"],
            cwd=os.path.abspath(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))),
            stdout=cls.log_file,
            stderr=subprocess.STDOUT,
            env=env
            )
        time.sleep(12)
        
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
        if os.path.exists(cls.fake_playlist_path):
            os.remove(cls.fake_playlist_path)

    def setUp(self):
        self.driver.get(f"http://localhost:{self.port}/app.html")
        WebDriverWait(self.driver, 15).until(
            EC.presence_of_element_located((By.ID, "main-split-container"))

    def take_screenshot(self, name):
        screenshot_dir = os.environ.get("MWV_GUI_PICTURES_DIR", os.path.dirname(__file__))
        ss_path = os.path.abspath(os.path.join(screenshot_dir, f"debug_playlist_{name}.png"))
        self.driver.save_screenshot(ss_path)
        print(f"Saved screenshot: {ss_path}")

    def test_playlist_reorder_and_remove(self):
        # 1. Wait for Parser/Backend to load library items in the Player tab
        #    The player tab is the default tab on startup.
        print("Waiting for media items to load in Player tab...")
        media_list_locator = (By.CSS_SELECTOR, "#media-list .media-item")
        
        # Increase timeout drastically to wait for the backend parser to finish loading all files
        WebDriverWait(self.driver, 45).until(
            EC.presence_of_all_elements_located(media_list_locator)
        
        # Verify we have at least 3 items before proceeding
        initial_items = self.driver.find_elements(*media_list_locator)
        if len(initial_items) < 3:
            self.fail(f"Not enough media items loaded to test playlist logic. Found {len(initial_items)}, need at least 3.")

        # 2. Click the first item to populate the playlist and start playback
        print("Clicking first media item to initialize playlist...")
        
        # We use JS to scroll and click to avoid StaleElementReferenceExceptions
        # since the UI may still be re-rendering the list in the background
        self.driver.execute_script("document.querySelectorAll('#media-list .media-item')[0].scrollIntoView({block: 'center'});")
        time.sleep(1)
        
        # Clicking any item in the player copies the entire media library into currentPlaylist
        self.driver.execute_script("document.querySelectorAll('#media-list .media-item')[0].click();")
        time.sleep(2) # Wait for backend playback handling

        # 3. Switch to playlist tab
        print("Switching to Playlist tab...")
        xpath = "//button[contains(@onclick, \"switchTab('playlist'\")]"
        btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        btn.click()
        time.sleep(2)

        self.take_screenshot("initial_load")

        # 4. Verify DOM has at least 3 items
        items = self.driver.find_elements(By.CSS_SELECTOR, "#playlist-list .media-item")
        self.assertGreaterEqual(len(items), 3, f"DOM does not show enough playlist items, found {len(items)}")
        
        names = [item.find_element(By.TAG_NAME, "strong").text for item in items[:3]]
        print(f"First 3 Playlist items loaded: {names}")
        
        TrackA = names[0]
        TrackB = names[1]
        TrackC = names[2]

        # 4. Click Move Down on Track A (index 0)
        print("Clicking Move Down on Track A (index 0)...")
        # Move Up is buttons[0], Move Down is buttons[1], Remove is buttons[2] (excluding grab)
        self.driver.execute_script("document.querySelectorAll('#playlist-list .media-item')[0].querySelectorAll('button')[1].click()")
        time.sleep(2)
        
        self.take_screenshot("after_move_down")

        items = self.driver.find_elements(By.CSS_SELECTOR, "#playlist-list .media-item")
        names = [item.find_element(By.TAG_NAME, "strong").text for item in items[:3]]
        print(f"Names after move down: {names}")
        self.assertEqual(names, [TrackB, TrackA, TrackC], "Move Down did not work visually")

        # 6. Click Move Up on Track C (now index 2)
        print(f"Clicking Move Up on {TrackC} (index 2)...")
        self.driver.execute_script("document.querySelectorAll('#playlist-list .media-item')[2].querySelectorAll('button')[0].click()")
        time.sleep(2)

        self.take_screenshot("after_move_up")

        items = self.driver.find_elements(By.CSS_SELECTOR, "#playlist-list .media-item")
        names = [item.find_element(By.TAG_NAME, "strong").text for item in items[:3]]
        print(f"Names after move up: {names}")
        self.assertEqual(names, [TrackB, TrackC, TrackA], "Move Up did not work visually")

        # 7. Click Remove on Track B (now index 0)
        print(f"Clicking Remove on {TrackB} (index 0)...")
        self.driver.execute_script("document.querySelectorAll('#playlist-list .media-item')[0].querySelectorAll('button')[2].click()")
        time.sleep(2)
        
        self.take_screenshot("after_remove")

        items = self.driver.find_elements(By.CSS_SELECTOR, "#playlist-list .media-item")
        names = [item.find_element(By.TAG_NAME, "strong").text for item in items[:2]]
        print(f"First 2 names after remove: {names}")
        self.assertEqual(names, [TrackC, TrackA], "Remove did not work visually")

if __name__ == "__main__":
    unittest.main()
