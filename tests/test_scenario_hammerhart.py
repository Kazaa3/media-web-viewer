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
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.playlist_page import PlaylistPage
from pages.player_page import PlayerPage

class TestHammerhartReorder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = 8005
        env = os.environ.copy()
        env["MWV_PORT"] = str(cls.port)
        env["MWV_FORCE_NEW_SESSION"] = "1"
        
        cls.app_process = subprocess.Popen(
            [sys.executable, "main.py"],
            cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
            env=env
        )
        time.sleep(15) 
        
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        cls.driver = webdriver.Chrome(options=options)
        cls.driver.set_window_size(1280, 1024)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver'):
            cls.driver.quit()
        if hasattr(cls, 'app_process'):
            cls.app_process.terminate()

    def test_hammerhart_to_second_and_fifth(self):
        player = PlayerPage(self.driver)
        playlist = PlaylistPage(self.driver)
        self.driver.get(f"http://localhost:{self.port}/app.html")
        time.sleep(3)

        # 1. Search and Play Hammerhart
        print("Selecting 'Hammerhart' in Player...")
        # Direct play via index if known, or search. Let's assume it's in library.
        # But easier: just find it in the playlist if already there, or add it.
        # Since we start with a clean session, we might need to add it or it's there from default media.
        
        # 2. Switch to Playlist
        print("Switching to Playlist tab...")
        playlist.switch_to()
        
        # 3. Ensure Hammerhart is at index 0 for a clean start
        wait = WebDriverWait(self.driver, 20)
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "media-item")))
        
        items = playlist.get_items()
        current_idx = -1
        for i, item in enumerate(items):
            if "Hammerhart" in item.text:
                current_idx = i
                break
        
        if current_idx == -1:
            self.fail("Hammerhart not in playlist after 20s wait")

        if current_idx != 0:
            print(f"Hammerhart is at index {current_idx}. Moving to 0 for scenario start...")
            # Use direct JS to move and render
            self.driver.execute_script(f"""
                eel.move_item_to({current_idx}, 0)().then(res => {{
                    if(res && res.status === 'ok') {{
                        currentPlaylist = res.items;
                        playlistIndex = res.index;
                        renderPlaylist();
                    }}
                }});
            """)
            time.sleep(5)
            
        # Verify it's at 0
        items = playlist.get_items()
        names = playlist.get_item_names()
        print(f"Playlist at scenario start: {names[:3]}")
        self.assertIn("Hammerhart", names[0], "Hammerhart must be at index 0 to start scenario")

        # 4. Move to Pos 2 (index 1)
        print("Picking Hammerhart from index 0...")
        grab_icon = items[0].find_element(By.CLASS_NAME, "grab-icon")
        
        # Simulate mousedown via JS to be 100% sure it hits our handler
        # Simulate mousedown via JS to be 100% sure it hits our handler
        self.driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('mousedown', {bubbles: true}));", grab_icon)
        time.sleep(1.5) # wait for 400ms timer
        # Re-find
        items = playlist.get_items()
        grab_icon = items[0].find_element(By.CLASS_NAME, "grab-icon")
        self.driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('mouseup', {bubbles: true}));", grab_icon)
        time.sleep(1)
        
        print("Inserting at index 1 (Target: Item at old index 1)...")
        items = playlist.get_items()
        # Click the 2nd item (index 1) to insert BEFORE it
        self.driver.execute_script("arguments[0].click();", items[1])
        time.sleep(5)
        
        names = playlist.get_item_names()
        print(f"Playlist after move to 1: {names[:3]}")
        playlist.take_screenshot("hammerhart_pos2_check")
        self.assertIn("Hammerhart", names[1])

        # 5. Move to Pos 5 (index 4)
        print("Picking Hammerhart from index 1...")
        items = playlist.get_items()
        grab_icon = items[1].find_element(By.CLASS_NAME, "grab-icon")
        
        self.driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('mousedown', {bubbles: true}));", grab_icon)
        time.sleep(1.5)
        # Re-find
        items = playlist.get_items()
        grab_icon = items[1].find_element(By.CLASS_NAME, "grab-icon")
        self.driver.execute_script("arguments[0].dispatchEvent(new MouseEvent('mouseup', {bubbles: true}));", grab_icon)
        time.sleep(1)
        
        print("Inserting at index 5...")
        # Re-find items again to be sure
        items = playlist.get_items()
        # If we have at least 6 items
        target_idx = min(5, len(items)-1)
        print(f"Targeting index {target_idx} for insertion...")
        self.driver.execute_script("arguments[0].click();", items[target_idx])
        time.sleep(5)
        
        names = playlist.get_item_names()
        print(f"Final verify: {names[:6]}")
        playlist.take_screenshot("hammerhart_pos5_check")
        # Position 5 is index 4 if we moved it from index 1 forward
        self.assertIn("Hammerhart", names[target_idx - (1 if target_idx > 1 else 0)]) # Simplified check
        # More precise: it should be at target_idx OR target_idx-1 depending on logic.
        # Let's just check if it's there at all in the first 6
        self.assertTrue(any("Hammerhart" in n for n in names[:6]), "Hammerhart should remain in top 6")

if __name__ == "__main__":
    unittest.main()
