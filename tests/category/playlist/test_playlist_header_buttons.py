#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import time
import os
import sys
import subprocess
import json
from selenium import webdriver
from tests.selenium.pages.playlist_page import PlaylistPage
from tests.selenium.pages.player_page import PlayerPage

class TestPlaylistHeaderButtons(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = 8004
        env = os.environ.copy()
        env["MWV_PORT"] = str(cls.port)
        env["MWV_FORCE_NEW_SESSION"] = "1"
        env["MWV_DEBUG_UI"] = "1"
        
        cls.log_file = open("test_playlist_header.log", "w")
        cls.app_process = subprocess.Popen(
            [sys.executable, "src.core.main.py"],
            cwd=os.path.abspath(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))),
            stdout=cls.log_file,
            stderr=subprocess.STDOUT,
            env=env
            )
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

    def test_global_move_buttons(self):
        player = PlayerPage(self.driver)
        playlist = PlaylistPage(self.driver)

        # 1. Start playback to populate playlist
        print("Starting playback of first item...")
        player.play_index(0)
        
        # 2. Switch to playlist
        print("Switching to Playlist tab...")
        playlist.switch_to()
        
        # Capture initial state
        names = playlist.get_item_names()
        print(f"Initial Playlist: {names[:3]}")
        playing_idx = playlist.get_playing_item_index()
        self.assertEqual(playing_idx, 0, "First item should be playing")
        playlist.take_screenshot("header_test_0_initial")

        # 3. Move Current Down
        print("Clicking Global Move Down...")
        playlist.move_current_down()
        time.sleep(2)
        
        names_after = playlist.get_item_names()
        playing_idx_after = playlist.get_playing_item_index()
        print(f"Playlist after move down: {names_after[:3]}")
        print(f"Playing index after: {playing_idx_after}")
        
        self.assertEqual(playing_idx_after, 1, "Playing index should have moved to 1")
        self.assertEqual(names_after[1], names[0], "Original first item should now be at index 1")
        playlist.take_screenshot("header_test_1_after_down")

        # 4. Move Current Up
        print("Clicking Global Move Up...")
        playlist.move_current_up()
        time.sleep(2)
        
        names_final = playlist.get_item_names()
        playing_idx_final = playlist.get_playing_item_index()
        print(f"Playlist after move up: {names_final[:3]}")
        
        self.assertEqual(playing_idx_final, 0, "Playing index should be back at 0")
        self.assertEqual(names_final[0], names[0], "Original item should be back at index 0")
        playlist.take_screenshot("header_test_2_final")

if __name__ == "__main__":
    unittest.main()
