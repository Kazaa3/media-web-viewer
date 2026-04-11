import os
import sys
import time
from playwright.sync_api import sync_playwright

# --- CONFIGURATION ---
URL = "http://localhost:8345/app.html"
HEADLESS = False  # Set to True for CI, False to see the 'own browser'
TIMEOUT = 30000   # 30s timeout for discovery

def run_playback_test():
    with sync_playwright() as p:
        print(f"[DOM-TEST] Launching isolated Chromium browser...")
        browser = p.chromium.launch(headless=True) # Stick to headless for server-side verification
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()

        # Enable console logging
        page.on("console", lambda msg: print(f"[BROWSER] {msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: print(f"[BROWSER] [ERROR] {err}"))

        # Navigate to application
        print(f"[DOM-TEST] Navigating to {URL}...")
        try:
            page.goto(URL, wait_until="networkidle")
        except Exception as e:
            print(f"[ERROR] Could not connect to application. Is it running? {e}")
            browser.close()
            return

        # 1. Wait for Library Sync / Media Discovery
        print("[DOM-TEST] Waiting for 'Mediathek' synchronization (Up to 30s)...")
        try:
            selector = ".legacy-track-item"
            tracks_found = False
            
            for attempt in range(4): # Try waiting/scanning up to 4 times
                # Direct check of library state
                lib_len = page.evaluate("typeof allLibraryItems !== 'undefined' ? allLibraryItems.length : -1")
                q_len = page.evaluate("typeof currentPlaylist !== 'undefined' ? currentPlaylist.length : -1")
                print(f"[DOM-TEST] [Attempt {attempt+1}] State: Lib={lib_len}, Queue={q_len}")

                if q_len > 0:
                    try:
                        page.wait_for_selector(selector, timeout=5000)
                        tracks_found = True
                        break
                    except:
                        print("[DOM-TEST] Queue has items but selector not found. Retrying...")

                print(f"[DOM-TEST] [Attempt {attempt+1}] Triggering manual scan via JS context...")
                page.evaluate("if(typeof scan === 'function') scan('./media', true)")
                time.sleep(15) # Give it more time to scan and sync

            if not tracks_found:
                 # Last resort: capture console logs and screenshot
                 page.screenshot(path="tests/ui/discovery_failure_final.png")
                 raise Exception(f"Library remained empty. Final State: Lib={lib_len}, Queue={q_len}")
            
            # Additional wait to ensure list is fully populated
            time.sleep(2)
            
            tracks = page.locator(selector).all()
            print(f"[SUCCESS] Found {len(tracks)} Titel in the queue.")
        except Exception as e:
            # Capture screenshot on failure
            page.screenshot(path="tests/ui/discovery_failure.png")
            print(f"[FAILURE] No Titel discovered in the sidebar after timeout. {e}")
            print("[INFO] Screenshot saved to tests/ui/discovery_failure.png")
            browser.close()
            return

        # 2. Trigger Playback
        first_track = tracks[0]
        track_name = first_track.inner_text().strip()
        print(f"[DOM-TEST] Triggering playback for: {track_name}")
        first_track.click()

        # 3. Verify Playback State
        print("[DOM-TEST] Verifying playback dominance in DOM...")
        time.sleep(3) # Wait for animation
        
        # Check if #big-player-title-legacy has changed
        now_playing_title = page.locator("#big-player-title-legacy").inner_text()
        print(f"[DOM-TEST] Dashboard Title: {now_playing_title}")

        if now_playing_title.lower() != "media library" and len(now_playing_title.strip()) > 0:
             print(f"[SUCCESS] Playback confirmed! Currently playing: {now_playing_title}")
        else:
             page.screenshot(path="tests/ui/playback_failure.png")
             print("[FAILURE] Playback trigger failed or metadata did not update.")
             print("[INFO] Screenshot saved to tests/ui/playback_failure.png")

        # 4. Final confirmation
        print("[DOM-TEST] Test sequence complete.")
        browser.close()

if __name__ == "__main__":
    run_playback_test()
