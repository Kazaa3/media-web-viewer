from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    page.on("console", lambda msg: print(f"BROWSER_LOG: {msg.text}"))
    
    print("Navigating to app...")
    page.goto("http://localhost:8345/app.html", wait_until="networkidle")
    time.sleep(4)
    
    # Dump variables
    try:
        all_len = page.evaluate("typeof allLibraryItems !== 'undefined' ? allLibraryItems.length : -1")
        all_items = page.evaluate("typeof allLibraryItems !== 'undefined' ? allLibraryItems.slice(0,2) : null")
        print(f"allLibraryItems length: {all_len}")
        print(f"Samples: {all_items}")
        
        # Test what the gallery gets
        audio_items = page.evaluate("""() => {
            const AUDIO_CATS = new Set(['audio', 'album', 'klassik', 'hörbuch', 'hörspiel', 'podcast', 'musik', 'compilation', 'single', 'radio']);
            return allLibraryItems.filter(i => {
                const cat = (i.category || i.logical_type || '').toLowerCase();
                return AUDIO_CATS.has(cat);
            });
        }""")
        print(f"audio_items length: {len(audio_items) if audio_items else 0}")
    except Exception as e:
        print(f"Error eval JS: {e}")
    
    browser.close()
