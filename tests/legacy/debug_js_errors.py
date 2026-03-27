import time
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import requests

def debug_app_js():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print("[Selenium] Successfully attached to session on 9222")
        
        # Give current page a moment
        time.sleep(2)
        
        # Get logs
        logs = driver.get_log('browser')
        print(f"[Selenium] Retrieved {len(logs)} log entries.")
        
        errors = [l for l in logs if l['level'] == 'SEVERE']
        print(f"[Selenium] Found {len(errors)} SEVERE errors.")
        
        for err in errors:
            print(f"--- ERROR: {err['message']} ---")
            # Proactively send to backend log if it wasn't already caught
            try:
                msg = f"[SEL-EXTRACT] {err['message']}"
                driver.execute_script("if(window.eel && eel.log_js_error) eel.log_js_error({'message': arguments[0], 'type': 'SELENIUM_CAPTURED'})", msg)
            except:
                pass

        # Capture a screenshot for visual confirmation of layout
        driver.save_screenshot("/home/xc/#Coding/gui_media_web_viewer/tests/last_js_error.png")
        print("[Selenium] Screenshot saved to tests/last_js_error.png")
        
        # Check integrity via the helper function I added
        try:
            is_balanced = driver.execute_script("return window.logDivBalancePerTab ? window.logDivBalancePerTab() : 'Helper missing'")
            print(f"[Selenium] logDivBalancePerTab returned: {is_balanced}")
        except Exception as e:
            print(f"[Selenium] Failed to run helper: {e}")

    except Exception as e:
        print(f"[Selenium] Error attaching: {e}")
        print("Make sure the app is running with --remote-debugging-port=9222")

if __name__ == "__main__":
    debug_app_js()
