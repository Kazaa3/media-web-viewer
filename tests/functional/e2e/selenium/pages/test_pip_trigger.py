#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pytest
import time
from .player_page import PlayerPage

class TestPipFunctionality:
    def test_pip_toggle_browser_api_interaction(self, driver):
        """
        Verify that clicking the PiP button triggers the browser's Picture-in-Picture API.
        We monkey-patch requestPictureInPicture to verify it was called.
        """
        # 1. Load application (assuming driver is already at the base URL)
        # 2. Mock the PiP API in the browser
        driver.execute_script("""
            window._pipCalled = false;
            HTMLVideoElement.prototype.requestPictureInPicture = async function() {
                window._pipCalled = true;
                return {};
            };
            // Ensure pictureInPictureEnabled is true
            Object.defineProperty(document, 'pictureInPictureEnabled', { value: true, configurable: true });
        """)
        
        # 3. Switch to Video tab
        driver.execute_script("switchTab('video', document.getElementById('telemetry-inspector-tab-trigger'))") # Using a known button or just switching
        # Better: find the actual tab button
        tab_btn = driver.find_element("id", "telemetry-inspector-tab-trigger") # This is debug, need video
        # Let's find video tab trigger
        driver.execute_script("switchTab('video')")
        time.sleep(1)
        
        # 4. Click PiP button
        pip_btn = driver.find_element("id", "btn-pip")
        pip_btn.click()
        time.sleep(0.5)
        
        # 5. Verify call
        was_called = driver.execute_script("return window._pipCalled")
        assert was_called is True, "PiP API was not triggered by btn-pip"
        print("✅ PiP Frontend Trigger verified via Selenium.")
