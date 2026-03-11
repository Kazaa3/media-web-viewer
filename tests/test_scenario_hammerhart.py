#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import unittest
import time
import os
import sys
import subprocess
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
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
        time.sleep(30) # Extensive wait for parsing
        
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
        time.sleep(5)

    def test_hammerhart_to_second_and_fifth(self):
        player = PlayerPage(self.driver)
        playlist = PlaylistPage(self.driver)

        # 1. Find Hammerhart
        print("Selecting 'Hammerhart' in Player...")
        media_items = self.driver.find_elements(By.CSS_SELECTOR, "#media-list .media-item")
        hammer_idx = -1
        for i, item in enumerate(media_items):
            if "Hammerhart" in item.text:
                hammer_idx = i
                break
        
        if hammer_idx == -1:
            self.fail("Could not find 'Hammerhart' in media list")
            
        player.play_index(hammer_idx)
        time.sleep(3)
        
        # 2. Switch to Playlist
        print("Switching to Playlist tab...")
        playlist.switch_to()
        time.sleep(3)
        
        # 3. Synchronize to Pos 0 (Pick & Insert)
        items = playlist.get_items()
        names = [it.text for it in items]
        current_idx = -1
        for i, name in enumerate(names):
            if "Hammerhart" in name:
                current_idx = i
                break
        
        if current_idx == -1:
            self.fail("Hammerhart not in playlist")

        print(f"Hammerhart is at index {current_idx}. Picking it...")
        grab_icon = items[current_idx].find_element(By.CLASS_NAME, "grab-icon")
        
        actions = ActionChains(self.driver)
        actions.move_to_element(grab_icon).click_and_hold().perform()
        time.sleep(1.5)
        actions.release().perform()
        time.sleep(2)
        
        print("Inserting at index 0 using JS click...")
        items = playlist.get_items()
        self.driver.execute_script("arguments[0].click();", items[0])
        time.sleep(5)
        
        names = playlist.get_item_names()
        print(f"Playlist after sync to 0: {names[:3]}")
        playlist.take_screenshot("hammerhart_pos1_check")
        self.assertIn("Hammerhart", names[0])

        # 4. Move to Pos 2 (index 1)
        print("Picking Hammerhart from index 0...")
        items = playlist.get_items()
        grab_icon = items[0].find_element(By.CLASS_NAME, "grab-icon")
        actions = ActionChains(self.driver)
        actions.move_to_element(grab_icon).click_and_hold().perform()
        time.sleep(1.5)
        actions.release().perform()
        time.sleep(2)
        
        print("Inserting at index 2...")
        items = playlist.get_items()
        self.driver.execute_script("arguments[0].click();", items[2])
        time.sleep(5)
        
        names = playlist.get_item_names()
        print(f"Playlist after move to 1: {names[:3]}")
        playlist.take_screenshot("hammerhart_pos2_check")
        self.assertIn("Hammerhart", names[1])

        # 5. Move to Pos 5 (index 4)
        print("Picking Hammerhart from index 1...")
        items = playlist.get_items()
        grab_icon = items[1].find_element(By.CLASS_NAME, "grab-icon")
        actions = ActionChains(self.driver)
        actions.move_to_element(grab_icon).click_and_hold().perform()
        time.sleep(1.5)
        actions.release().perform()
        time.sleep(2)
        
        print("Inserting at index 5...")
        items = playlist.get_items()
        self.driver.execute_script("arguments[0].click();", items[5])
        time.sleep(5)
        
        names = playlist.get_item_names()
        print(f"Final verify: {names[:6]}")
        playlist.take_screenshot("hammerhart_pos5_check")
        self.assertIn("Hammerhart", names[4])

if __name__ == "__main__":
    unittest.main()
