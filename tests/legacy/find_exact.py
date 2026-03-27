from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def find_last_good_js():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        scripts = driver.find_elements("tag name", "script")
        full_content = scripts[-1].get_attribute('innerHTML')
        lines = full_content.split('\n')
        
        for i in range(1, len(lines)):
            test_content = '\n'.join(lines[:i])
            error = driver.execute_script("""
                try {
                    new Function(arguments[0]);
                    return null;
                } catch(e) {
                    return e.message;
                }
            """, test_content)
            
            if error and 'Unexpected end of input' not in error:
                print(f"FAILED AT ABS LINE {6398 + i}: {error}")
                print(f"CODE: {lines[i-1]}")
                # Print few context lines
                for offset in range(-3, 0):
                    idx = i - 1 + offset
                    if idx >= 0:
                        print(f"  {6398 + idx + 1}: {lines[idx]}")
                break

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_last_good_js()
