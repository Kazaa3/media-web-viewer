from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

def binary_search_syntax_error():
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        print("[Selenium] Attached.")
        
        scripts = driver.find_elements("tag name", "script")
        last_script = scripts[-1]
        full_content = last_script.get_attribute('innerHTML')
        lines = full_content.split('\n')
        
        # Test prefixes of the script to see when it breaks
        low = 1
        high = len(lines)
        last_fail = high
        
        print(f"Testing {len(lines)} lines...")
        
        while low <= high:
            mid = (low + high) // 2
            test_content = '\n'.join(lines[:mid])
            
            # Close any open blocks for it to be valid? No, just check if it's a prefix error.
            # Actually we can just check if new Function(test_content) throws an UNEXPECTED token.
            
            error = driver.execute_script("""
                try {
                    new Function(arguments[0]);
                    return null;
                } catch(e) {
                    if (e.message.includes('Unexpected end of input')) return 'EOF'; // Normal for prefix
                    return e.message;
                }
            """, test_content)
            
            if error and error != 'EOF':
                print(f"Failed at line {mid}: {error}")
                last_fail = mid
                high = mid - 1
            else:
                low = mid + 1
        
        print(f"First syntax error found at line {last_fail} of the script.")
        # Line in file = 6398 + last_fail
        print(f"Absolute line in file: {6398 + last_fail}")
        
        # Print the problematic line
        print(f"Code: {lines[last_fail-1]}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    binary_search_syntax_error()
