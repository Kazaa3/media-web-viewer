from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def evaluate_script_to_find_error():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print("[Selenium] Attached.")
        
        scripts = driver.find_elements("tag name", "script")
        last_script = scripts[-1]
        content = last_script.get_attribute('innerHTML')
        
        # Eval the script in a sandy environment in the browser to catch the error
        # Wait! It's already been evaluated and failed.
        # But we can try to re-eval a small portion until it fails.
        
        error = driver.execute_script("""
            try {
                new Function(arguments[0]);
                return 'No syntax error detected in this block via new Function()';
            } catch(e) {
                return e.name + ': ' + e.message + '\\nStack: ' + e.stack;
            }
        """, content)
        print(f"[Selenium] Result: {error}")
                
    except Exception as e:
        print(f"[Selenium] Error: {e}")

if __name__ == "__main__":
    evaluate_script_to_find_error()
