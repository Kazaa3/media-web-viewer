from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def force_refresh():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print("[Selenium] Attached.")
        # Load with cache buster
        url = driver.current_url
        if '?' in url:
            url = url.split('?')[0]
        new_url = f"{url}?v={int(time.time())}"
        print(f"[Selenium] Navigating to: {new_url}")
        driver.get(new_url)
        time.sleep(2)
        print("[Selenium] Done.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    force_refresh()
