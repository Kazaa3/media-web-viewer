import os
import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

def run_diagnostics():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    # Try to connect to existing session
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print("--- [Diagnostics Suite] ---")
        print(f"Connected to session at {driver.current_url}")
        
        # 1. Capture Browser Logs
        print("\n[Step 1] Polling browser logs...")
        logs = driver.get_log('browser')
        for l in logs:
            level = l.get('level', 'INFO')
            message = l.get('message', '')
            print(f"[{level}] {message}")
            if level == 'SEVERE' and 'Eel' in message:
                print(">>> CRITICAL: Eel.js communication issue detected.")
        
        # 2. Check DOM Helper (window.logDivBalancePerTab)
        print("\n[Step 2] Executing DOM Integrity Helper...")
        try:
            res = driver.execute_script("return window.logDivBalancePerTab ? window.logDivBalancePerTab() : 'HELPER_MISSING'")
            print(f"DOM Integrity Result: {res}")
            if res == 'HELPER_MISSING':
                print(">>> WARNING: Your helper function was NOT defined (SyntaxError prevented script load?)")
        except Exception as e:
            print(f">>> ERROR running helper script: {e}")
            
        # 3. Capture Screenshot
        screenshot_path = os.path.abspath("tests/artifacts/diagnostic_view.png")
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        driver.save_screenshot(screenshot_path)
        print(f"\n[Step 3] Screenshot captured to: {screenshot_path}")
        
        # 4. Probe for Popup Interceptor
        print("\n[Step 4] Probing Popup Interceptor...")
        try:
            # Check if alert was hijacked
            is_hijacked = driver.execute_script("return window.alert.toString().includes('eel')")
            print(f"Alert Proxy active: {is_hijacked}")
        except:
            pass
            
        print("\n--- [Diagnostics Complete] ---")
        
    except Exception as e:
        print(f"Failed to connect to Debugger: {e}")
        print("Please ensure the app is running with --remote-debugging-port=9222")

if __name__ == "__main__":
    run_diagnostics()
