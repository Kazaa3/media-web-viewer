from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def grab_script_content():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print("[Selenium] Attached.")
        
        # Find the last script tag
        scripts = driver.find_elements("tag name", "script")
        if scripts:
            last_script = scripts[-1]
            content = last_script.get_attribute('innerHTML')
            print(f"[Selenium] Last script length: {len(content)}")
            
            # Find the line around 11170
            # Wait! The line numbers in app.html are absolute.
            # In innerHTML, it's relative to the start of the script.
            # Script starts at 6398. 11170 - 6398 = 4772.
            
            lines = content.split('\n')
            target_rel = 11170 - 6398
            
            if target_rel < len(lines):
                print(f"--- Line {11170} (Rel {target_rel}): ---")
                print(lines[target_rel])
                # Show few lines before/after
                for offset in range(-5, 5):
                    idx = target_rel + offset
                    if 0 <= idx < len(lines):
                         print(f"{idx}: {lines[idx]}")
            else:
                print(f"Rel {target_rel} is out of bounds (Max {len(lines)})")
                
    except Exception as e:
        print(f"[Selenium] Error: {e}")

if __name__ == "__main__":
    grab_script_content()
