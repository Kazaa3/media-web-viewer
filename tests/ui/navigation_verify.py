import sys
import os
import time
from pathlib import Path
from playwright.sync_api import sync_playwright

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
PORT = 8345

def verify_navigation():
    print(f"Starting Navigation Verification on port {PORT}...")
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        try:
            page.goto(f"http://127.0.0.1:{PORT}/app.html", timeout=10000)
            print("Page loaded.")
            
            # Map of main categories to expected sub-nav pills
            nav_map = {
                "media": ["Player", "Library Browser", "Video Cinema"],
                "reporting": ["Dashboard", "Database", "Video Health", "Audio Health", "Performance"],
                "tests": ["System Health", "Debug DB", "Latency"],
                "system": ["Environment", "Playback", "Advanced"],
                "edit": ["Metadata Tags", "Artwork Lab", "Media Analysis"],
                "library": ["Mediathek", "Dateibrowser", "Inventar & DB"],
                "tools": ["Parser Chain", "Transcoding"],
                "logbuch": ["Journal", "Documentation"]
            }
            
            for category, expected_pills in nav_map.items():
                print(f"Testing Category: {category}")
                
                # Click the sidebar item
                # The sidebar items use switchMainCategory('cat', this)
                sidebar_btn = page.query_selector(f"button[onclick*='switchMainCategory(\\'{category}\\'']")
                if not sidebar_btn:
                    print(f"  [ERROR] Sidebar button for {category} not found.")
                    continue
                
                sidebar_btn.click()
                time.sleep(1.0) # Wait for fragment and sub-nav to populate
                
                # Check for pills
                sub_nav = page.query_selector("#sub-nav-container")
                if not sub_nav or not sub_nav.is_visible():
                    print(f"  [ERROR] Sub-nav container not visible for {category}.")
                    continue
                
                pills = page.query_selector_all(".sub-pill-btn")
                pill_labels = [p.inner_text().strip() for p in pills]
                
                print(f"  Found pills: {pill_labels}")
                
                for expected in expected_pills:
                    if expected not in pill_labels:
                        print(f"  [FAIL] Expected pill '{expected}' missing.")
                    else:
                        print(f"  [PASS] Pill '{expected}' found.")
                        
            print("\nVerification Complete.")
            
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_navigation()
