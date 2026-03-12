#!/usr/bin/env python3
"""
Generate Reference Screenshots for all GUI Tabs.
This script launches the backend, connects with Selenium headless,
iterates through all tabs, and saves a screenshot of each to a folder.
"""

import time
import os
import subprocess
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

# Setup paths
BASE_DIR = Path(__file__).parents[2]
SCREENSHOT_DIR = BASE_DIR / "tests" / "reference_screenshots"
SCREENSHOT_DIR.mkdir(parents=True, exist_ok=True)

port = 8010
env = os.environ.copy()
env["MWV_PORT"] = str(port)
env["MWV_FORCE_NEW_SESSION"] = "1"
env["MWV_DEBUG_UI"] = "1"

print(f"Starting server on port {port}...")
app_process = subprocess.Popen(
    [os.sys.executable, "src/core/main.py"],
    cwd=str(BASE_DIR),
    stdout=subprocess.DEVNULL,
    stderr=subprocess.STDOUT,
    env=env
            )
time.sleep(5)

options = Options()
options.add_argument("--headless")
options.add_argument("--window-size=1280,1024")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
driver = webdriver.Chrome(options=options)

try:
    print("Loading application...")
    driver.get(f"http://localhost:{port}/app.html")
    time.sleep(3)
    
    phases = ["0_initial", "1_after_refresh_1", "2_after_refresh_2", "3_after_refresh_3"]
    
    for phase_idx, phase_name in enumerate(phases):
        print(f"\n--- Phase P{phase_idx}: {phase_name} ---")
        if phase_idx > 0:
            print("Refreshing browser...")
            driver.refresh()
            time.sleep(3) # Wait for reload
            
        # Save the initial loaded state for this phase
        driver.save_screenshot(str(SCREENSHOT_DIR / f"P{phase_idx}_{phase_name}_00_load.png"))
        
        # Find all tab buttons (re-find after every refresh)
        buttons = driver.find_elements(By.CSS_SELECTOR, ".tab-btn")
        
        for idx, btn in enumerate(buttons, start=1):
            btn_text = btn.text.strip().replace(" ", "_").replace("️", "").replace("🎬", "").replace("⚙", "").replace("📓", "").replace("📋", "").replace("✨", "").strip()
            if not btn_text:
                continue
                
            print(f"Switching to tab: {btn_text}...")
            try:
                # Re-find the button in case elements went stale
                current_btns = driver.find_elements(By.CSS_SELECTOR, ".tab-btn")
                current_btns[idx-1].click()
                time.sleep(1.5) # Wait for animation/render
                
                # Save screenshot
                filename = f"P{phase_idx}_{phase_name}_{idx:02d}_tab_{btn_text}.png"
                filepath = SCREENSHOT_DIR / filename
                driver.save_screenshot(str(filepath))
                print(f"Saved {filename}")
            except Exception as e:
                print(f"Failed to capture {btn_text}: {e}")

    print(f"\nSuccessfully generated {len(list(SCREENSHOT_DIR.glob('*.png')))} reference screenshots in:")
    print(str(SCREENSHOT_DIR))

finally:
    driver.quit()
    app_process.terminate()
