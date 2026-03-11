#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import time
import os
import sys
import subprocess
from selenium import webdriver
from pages.playlist_page import PlaylistPage
from pages.player_page import PlayerPage

class TestHammerhartReorder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = 8005
        env = os.environ.copy()
        env["MWV_PORT"] = str(cls.port)
        env["MWV_FORCE_NEW_SESSION"] = "1"
        env["MWV_DEBUG_UI"] = "1"
        
        cls.log_file = open("test_hammerhart.log", "w")
        cls.app_process = subprocess.Popen(
            [sys.executable, "main.py"],
            cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
            stdout=cls.log_file,
            stderr=subprocess.STDOUT,
            env=env
        )
        # Wait for backend to parse and start
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
            cls.app_process.wait()
        if hasattr(cls, 'log_file'):
            cls.log_file.close()

    def setUp(self):
        self.driver.get(f"http://localhost:{self.port}/app.html")
        time.sleep(2)

    def test_hammerhart_to_second_and_fifth(self):
        player = PlayerPage(self.driver)
        playlist = PlaylistPage(self.driver)

        # 1. Find Hammerhart in Player and play it
        # Note: We assume it's in the media list. 
        # In this specific test environment, we might need to search or just pick the index if known.
        # Based on previous tests, it's often early in the list.
        print("Selecting 'Hammerhart' in Player...")
        names_player = [it.text for it in self.driver.find_elements(By.CSS_SELECTOR, "#media-list .media-item strong")]
        hammer_idx = -1
        for i, name in enumerate(names_player):
            if "Hammerhart" in name:
                hammer_idx = i
                break
        
        if hammer_idx == -1:
            self.fail("Could not find 'Hammerhart' in media list")
            
        player.play_index(hammer_idx)
        
        # 2. Switch to Playlist
        print("Switching to Playlist tab...")
        playlist.switch_to()
        
        # 3. Verify it's at position 1 (index 0)
        items = playlist.get_item_names()
        print(f"Current Playlist: {items[:6]}")
        self.assertIn("Hammerhart", items[0], "Hammerhart should be at 1st position")
        playlist.take_screenshot("hammerhart_1_pos")

        # 4. Move to 2nd position (one Move Down)
        print("Moving 'Hammerhart' to 2nd position...")
        playlist.move_current_down()
        time.sleep(2)
        items = playlist.get_item_names()
        self.assertIn("Hammerhart", items[1], f"Hammerhart should be at 2nd position, found: {items[1]}")
        playlist.take_screenshot("hammerhart_2_pos")

        # 5. Move to 5th position (three more Move Down)
        print("Moving 'Hammerhart' to 5th position...")
        for _ in range(3):
            playlist.move_current_down()
            time.sleep(1)
            
        items = playlist.get_item_names()
        print(f"Playlist after reorder: {items[:6]}")
        self.assertIn("Hammerhart", items[4], f"Hammerhart should be at 5th position (index 4), found: {items[4]}")
        playlist.take_screenshot("hammerhart_5_pos")

if __name__ == "__main__":
    unittest.main()
