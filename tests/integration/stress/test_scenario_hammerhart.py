#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: UI Scenario (Hammerhart)
# Eingabewerte: Playlist-DOM, "Hammerhart" Song-ID
# Ausgabewerte: Reordered DOM, Backend-Persistence Status
# Testdateien: tests/test_scenario_hammerhart.py
# Kommentar: Komplexer E2E-Test für Playlist-Reordering via Drag & Drop.

import pytest
pytest.importorskip("selenium")

import unittest
import time
import os
import sys
import subprocess
import psutil
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import JavascriptException, StaleElementReferenceException, TimeoutException
from tests.selenium.pages.playlist_page import PlaylistPage
from tests.basic.utils.test_utils import manage_app_instance, wait_for_app, robust_action, save_screenshot

class TestHammerhartReorder(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        preferred = int(os.environ.get("MWV_PORT", 0)) or None
        cls.app_process = None
        decision, using_existing, cls.port, core_python = manage_app_instance(preferred)
        
        if decision == "START_NEW":
            env = os.environ.copy()
            env["MWV_PORT"] = str(cls.port)
            env["MWV_FORCE_NEW_SESSION"] = "1"
            cls.app_process = subprocess.Popen(
                [core_python, "src/core/main.py"],
                cwd=os.path.abspath(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))),
                env=env
            )
            if not wait_for_app(cls.port, timeout=60): raise RuntimeError("Failed to start")

        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36")
        cls.driver = webdriver.Chrome(options=options)

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'driver'): cls.driver.quit()
        if cls.app_process:
            # Check resource usage before terminating
            try:
                proc = psutil.Process(cls.app_process.pid)
                mem = proc.memory_info().rss / (1024 * 1024)
                files = len(proc.open_files())
                print(f"\n📊 Final Resource Usage for PID {cls.app_process.pid}:")
                print(f"  • Memory: {mem:.2f} MB")
                print(f"  • Open Files: {files}")
            except Exception as e:
                print(f"Could not retrieve final resource usage: {e}")
            cls.app_process.terminate()

    def test_hammerhart_to_second_and_fifth(self):
        playlist = PlaylistPage(self.driver)
        try:
            self.driver.get(f"http://localhost:{self.port}/app.html")
            wait = WebDriverWait(self.driver, 45)
            wait.until(EC.element_to_be_clickable((By.ID, "playlist-btn"))).click()
            wait.until(EC.presence_of_element_located((By.CLASS_NAME, "media-item")))
            
            # Initial Resource Snapshot
            proc = psutil.Process(self.app_process.pid) if self.app_process else None
            if proc:
                mem_start = proc.memory_info().rss / (1024 * 1024)
                files_start = len(proc.open_files())
                print(f"\n🚀 Hammerhart Start - PID {self.app_process.pid}: {mem_start:.2f} MB, {files_start} files")
            
            def find_hammer_idx():
                names = playlist.get_item_names()
                for i, name in enumerate(names):
                    if "Hammerhart" in name: return i
                return -1

            # Wait for scanner
            start_wait = time.time()
            current_idx = -1
            while time.time() - start_wait < 60:
                current_idx = find_hammer_idx()
                if current_idx != -1: break
                time.sleep(5)
            
            if current_idx == -1: self.fail("Hammerhart not found")

            def perform_drag():
            # 1. Grab (triggers re-render)
                items = self.driver.find_elements(By.CLASS_NAME, "media-item")
                target_pos = 1 if len(items) > 1 else 0
                idx = -1
                for i, item in enumerate(items):
                    if "Hammerhart" in item.text:
                        idx = i
                        break
                
                if idx == -1: return False
                if idx == target_pos: return True
                
                source_item = items[idx]
                grab = source_item.find_element(By.CLASS_NAME, "grab-icon")
                self.driver.execute_script("arguments[0].scrollIntoView();", grab)
                
                ActionChains(self.driver).click_and_hold(grab).perform()
                time.sleep(1) # Wait for re-render
                
                # 2. Re-find target
                items_new = self.driver.find_elements(By.CLASS_NAME, "media-item")
                if len(items_new) <= target_pos: return False
                target_new = items_new[target_pos]
                
                # Defensive scrolling for target
                self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", target_new)
                time.sleep(0.5)
                
                ActionChains(self.driver).move_to_element(target_new).pause(0.5).release().perform()
                return True

            robust_action(self.driver, perform_drag)
            time.sleep(3)
            final_names = playlist.get_item_names()
            self.assertIn("Hammerhart", final_names[1 if len(final_names) > 1 else 0])
        except Exception:
            save_screenshot(self.driver, "test_hammerhart_fail")
            raise

if __name__ == "__main__":
    unittest.main()
