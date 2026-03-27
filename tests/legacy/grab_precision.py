from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def grab_browser_code_around_line(abs_line):
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print("[Selenium] Attached.")
        
        scripts = driver.find_elements("tag name", "script")
        last_script = scripts[-1]
        content = last_script.get_attribute('innerHTML')
        lines = content.split('\n')
        
        # Script starts at 6398.
        rel_line = abs_line - 6398
        
        print(f"--- Code around Absolute {abs_line} (Rel {rel_line}): ---")
        for offset in range(-5, 5):
            idx = rel_line + offset
            if 0 <= idx < len(lines):
                print(f"{abs_line + offset}: {lines[idx]}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    grab_browser_code_around_line(7960)
