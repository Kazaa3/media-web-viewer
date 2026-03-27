#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Selenium Player Dropdown Test
# Eingabewerte: WebDriver
# Ausgabewerte: Testresultate
# Testdateien: test_player_dropdowns.py
# Kommentar: Testet die dynamischen Dropdowns im Video Player Tab.

import pytest
import time
from selenium.webdriver.support.ui import Select
from .player_page import PlayerPage

class TestPlayerDropdowns:
    """
    DE:
    Testet die Synchronisation der Video-Player-Dropdowns (Player-Typ -> Video-Modus).
    
    EN:
    Tests the synchronization of video player dropdowns (Player Type -> Video Mode).
    """

    def test_dropdown_synchronization(self, driver):
        """
        DE:
        Prüft, ob die Video-Modi basierend auf dem Player-Typ korrekt aktualisiert werden.
        
        EN:
        Checks if video modes are correctly updated based on player type.
        """
        player_page = PlayerPage(driver)
        
        # Navigate to player tab if not there
        # (Assuming the driver is already at the correct URL and tab is active or we switch to it)
        # For this test, we assume the page is loaded.
        
        player_type_el = player_page.wait_for_element(player_page.PLAYER_TYPE)
        video_mode_el = player_page.wait_for_element(player_page.VIDEO_MODE)
        
        player_select = Select(player_type_el)
        mode_select = Select(video_mode_el)
        
        # Test Case 1: Select Chrome
        print("Testing Chrome Native modes...")
        player_select.select_by_value("chrome")
        time.sleep(0.5)
        options = [o.get_attribute("value") for o in mode_select.options]
        assert "chrome_direct" in options
        assert "chrome_hls" in options
        assert "vlc_cvlc" not in options
        
        # Test Case 2: Select VLC
        print("Testing VLC modes...")
        player_select.select_by_value("vlc")
        time.sleep(0.5)
        options = [o.get_attribute("value") for o in mode_select.options]
        assert "vlc_cvlc" in options
        assert "vlc_embedded" in options
        assert "chrome_direct" not in options
        
        # Test Case 3: Select PyPlayer
        print("Testing PyPlayer modes...")
        player_select.select_by_value("pyplayer")
        time.sleep(0.5)
        options = [o.get_attribute("value") for o in mode_select.options]
        assert "pyplayer_native" in options
        assert "pyplayer_pip" in options
        assert "vlc_cvlc" not in options
        
        print("✅ Dropdown synchronization verified successfully.")

if __name__ == "__main__":
    # This file is intended to be run via pytest with a browser fixture.
    pass
