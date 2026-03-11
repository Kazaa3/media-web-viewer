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
            [sys.executable, "main.py"],
            cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
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
        )

    def take_screenshot(self, name):
        screenshot_dir = os.environ.get("MWV_GUI_PICTURES_DIR", os.path.dirname(__file__))
        ss_path = os.path.abspath(os.path.join(screenshot_dir, f"debug_playlist_{name}.png"))
        self.driver.save_screenshot(ss_path)
        print(f"Saved screenshot: {ss_path}")

    def test_playlist_reorder_and_remove(self):
        # 1. Switch to playlist tab
        xpath = "//button[contains(@onclick, \"switchTab('playlist'\")]"
        btn = WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable((By.XPATH, xpath)))
        btn.click()
        time.sleep(1)

        # 2. Inject fake playlist
        self.driver.set_script_timeout(10)
        inject_script = """
            var done = arguments[arguments.length - 1];
            var items = [
                {"name": "Track A", "path": "/fake/A.mp3"},
                {"name": "Track B", "path": "/fake/B.mp3"},
                {"name": "Track C", "path": "/fake/C.mp3"}
            ];
            eel.set_current_playlist(items)().then(res => {
                if (res.status === 'ok') {
                    currentPlaylist = items;
                    playlistIndex = -1;
                    renderPlaylist();
                    done(true);
                } else {
                    console.error("Set failed:", res);
                    done(false);
                }
            }).catch(e => {
                console.error("Eel error:", e);
                done(false);
            });
        """
        success = self.driver.execute_async_script(inject_script)
        self.assertTrue(success, "Failed to load test playlist via eel")
        time.sleep(1)

        self.take_screenshot("initial_load")

        # 3. Verify DOM has 3 items
        items = self.driver.find_elements(By.CSS_SELECTOR, "#playlist-list .media-item")
        self.assertEqual(len(items), 3, f"DOM does not show 3 playlist items, found {len(items)}")
        names = [item.find_element(By.TAG_NAME, "strong").text for item in items]
        self.assertEqual(names, ["Track A", "Track B", "Track C"])

        # 4. Click Move Down on Track A (index 0)
        print("Clicking Move Down on Track A (index 0)...")
        # Move Up is buttons[0], Move Down is buttons[1], Remove is buttons[2] (excluding grab)
        self.driver.execute_script("document.querySelectorAll('#playlist-list .media-item')[0].querySelectorAll('button')[1].click()")
        time.sleep(2)
        
        self.take_screenshot("after_move_down")

        items = self.driver.find_elements(By.CSS_SELECTOR, "#playlist-list .media-item")
        names = [item.find_element(By.TAG_NAME, "strong").text for item in items]
        print(f"Names after move down: {names}")
        self.assertEqual(names, ["Track B", "Track A", "Track C"], "Move Down did not work visually")

        # 5. Click Move Up on Track C (now index 2)
        print("Clicking Move Up on Track C (index 2)...")
        self.driver.execute_script("document.querySelectorAll('#playlist-list .media-item')[2].querySelectorAll('button')[0].click()")
        time.sleep(2)

        self.take_screenshot("after_move_up")

        items = self.driver.find_elements(By.CSS_SELECTOR, "#playlist-list .media-item")
        names = [item.find_element(By.TAG_NAME, "strong").text for item in items]
        print(f"Names after move up: {names}")
        self.assertEqual(names, ["Track B", "Track C", "Track A"], "Move Up did not work visually")

        # 6. Click Remove on Track B (now index 0)
        print("Clicking Remove on Track B (index 0)...")
        self.driver.execute_script("document.querySelectorAll('#playlist-list .media-item')[0].querySelectorAll('button')[2].click()")
        time.sleep(2)
        
        self.take_screenshot("after_remove")

        items = self.driver.find_elements(By.CSS_SELECTOR, "#playlist-list .media-item")
        names = [item.find_element(By.TAG_NAME, "strong").text for item in items]
        print(f"Names after remove: {names}")
        self.assertEqual(names, ["Track C", "Track A"], "Remove did not work visually")


if __name__ == "__main__":
    unittest.main()
