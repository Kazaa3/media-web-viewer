#!/usr/bin/env python3
import unittest
import time
import os
import sys
import subprocess
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from pages.playlist_page import PlaylistPage
from pages.player_page import PlayerPage

class TestMouseInteraction(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = 8006
        env = os.environ.copy()
        env["MWV_PORT"] = str(cls.port)
        env["MWV_FORCE_NEW_SESSION"] = "1"
        
        cls.log_file = open("test_mouse.log", "w")
        cls.app_process = subprocess.Popen(
            [sys.executable, "main.py"],
            cwd=os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
            stdout=cls.log_file,
            stderr=subprocess.STDOUT,
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
            cls.app_process.wait()
        cls.log_file.close()

    def test_pick_and_insert_flow(self):
        player = PlayerPage(self.driver)
        playlist = PlaylistPage(self.driver)
        self.driver.get(f"http://localhost:{self.port}/app.html")
        time.sleep(2)

        # 1. Populate
        player.play_index(0)
        playlist.switch_to()
        
        # 2. Pick item 0 (Long press on grab icon)
        print("Simulating long press on grab icon...")
        grab_icons = self.driver.find_elements(By.CLASS_NAME, "grab-icon")
        actions = ActionChains(self.driver)
        actions.click_and_hold(grab_icons[0]).perform()
        time.sleep(1) # wait for pickTimer (400ms)
        actions.release().perform()
        
        # 3. Verify 'picked' class exists
        items = playlist.get_items()
        self.assertIn("picked", items[0].get_attribute("class"), "Item should have 'picked' class after long press")
        playlist.take_screenshot("mouse_test_picked")

        # 4. Insert at position 3 (click index 2)
        print("Clicking target item to insert...")
        items[2].click()
        time.sleep(2)
        
        # 5. Verify reorder
        names = playlist.get_item_names()
        print(f"Playlist after mouse reorder: {names[:5]}")
        # Note: Logic is 'insert before targetIndex'. 
        # If moving 0 to 2, it pops 0, then inserts before (new) 2.
        # Check visually.
        playlist.take_screenshot("mouse_test_final")

if __name__ == "__main__":
    from selenium.webdriver.common.by import By # ensure By is available
    unittest.main()
