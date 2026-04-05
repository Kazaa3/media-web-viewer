
import os
import sys
import time
import json
import argparse
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import WebDriverException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def check_div_balance(driver, view_id):
    """Checks div balance for a specific container via JS."""
    script = f"""
        var el = document.getElementById('{view_id}');
        if (!el) return {{ 'status': 'missing' }};
        var html = el.innerHTML;
        var opens = (html.match(/<div/gi) || []).length;
        var closes = (html.match(/<\\/div/gi) || []).length;
        return {{ 'opens': opens, 'closes': closes, 'balanced': opens === closes }};
    """
    try:
        return driver.execute_script(script)
    except:
        return {'status': 'error'}

def run_tests(args):
    print("--- SELENIUM COMPREHENSIVE SESSION TEST ---")
    print(f"Flags: Verbose={args.verbose}, Trace={args.trace}, Debug={args.debug}, DOM-Control={args.dom_control}")
    print(f"Time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    chrome_options = Options()
    chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")
    
    try:
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(10)
        print(f"[SUCCESS] Attached to session: {driver.title}")
        
        # 1. INITIALIZATION: Always start with Audio Player
        print("\n[STEP 1] Audio Player Initialization (Left Focus)...")
        try:
            # Re-focus or ensure we are on the player tab
            driver.execute_script("switchTab('player')")
            time.sleep(0.5)
            
            audio_el = driver.find_element(By.ID, "native-html5-audio-pipeline-element")
            print(f"  -> ✅ Audio element found: {audio_el.tag_name}")
            print(f"  -> State: {audio_el.get_property('paused') and 'Paused' or 'Playing/Ready'}")
            
            # Check player view div balance
            balance = check_div_balance(driver, "state-orchestrated-active-queue-list-container")
            if balance.get('status') != 'missing':
                print(f"  -> View Integrity: {balance['opens']} opens / {balance['closes']} closes | {'✅ Balanced' if balance['balanced'] else '❌ IMBALANCE'}")
        except Exception as e:
            print(f"  -> ❌ Audio Player check failed: {e}")

        # 2. NAVIGATION: Left to Right across all major menus
        print("\n[STEP 2] Multi-Tab Navigation & Integrity Check (Left -> Right)...")
        # Tuples of (tab_id, panel_id, label, button_id)
        tabs = [
            ('player', 'state-orchestrated-active-queue-list-container', 'Player/Queue', 'active-queue-tab-trigger'),
            ('library', 'coverflow-library-panel', 'Library/Index', 'coverflow-library-tab-trigger'),
            ('item', 'indexed-sqlite-media-repository-panel', 'Item Meta', 'indexed-sqlite-repository-tab-trigger'),
            ('file', 'filesystem-crawler-directory-panel', 'File Crawler', 'filesystem-crawler-tab-trigger'),
            ('edit', 'metadata-writer-crud-panel', 'CRUD Edit', 'crud-metadata-tab-trigger'),
            ('options', 'system-configuration-persistence-panel', 'Options', 'system-registry-tab-trigger'),
            ('parser', 'regex-provider-chain-orchestrator-panel', 'Parser Chain', 'chain-config-tab-trigger'),
            ('debug', 'debug-flag-persistence-panel', 'Telemetry', 'telemetry-inspector-tab-trigger'),
            ('tests', 'quality-assurance-regression-suite-panel', 'QA Tests', 'qa-validation-tab-trigger'),
            ('reporting', 'reporting-dashboard-panel', 'Reporting', 'reporting-dashboard-tab-trigger'),
            ('logbuch', 'localized-markdown-documentation-journal-panel', 'Logbuch', 'documentation-journal-tab-trigger'),
            ('playlist', 'json-serialized-sequence-buffer-panel', 'Playlist', 'sequential-buffer-tab-trigger'),
            ('vlc', 'multiplexed-media-player-orchestrator-panel', 'Video Player', 'media-orchestrator-tab-trigger')
        ]
        
        for tab_id, panel_id, label, btn_id in tabs:
            try:
                print(f"  -> Checking {label:15} [{tab_id:10}]...", end=" ")
                
                # In PP Mode (Production/Performance), we skip some delay or do direct interaction
                if args.pp_mode:
                    driver.execute_script(f"switchTab('{tab_id}')")
                elif args.dom_control:
                    driver.execute_script(f"switchTab('{tab_id}')")
                else:
                    try:
                        btn = driver.find_element(By.ID, btn_id)
                        driver.execute_script("arguments[0].scrollIntoView();", btn)
                        btn.click()
                    except:
                        driver.execute_script(f"switchTab('{tab_id}')")
                
                # Performance-adjusted sleep
                time.sleep(0.15 if args.pp_mode else 0.4)
                
                balance = check_div_balance(driver, panel_id)
                if balance.get('status') == 'missing':
                    print("⚠️ Panel Missing")
                else:
                    res_char = balance.get('balanced') and "✅" or "❌"
                    print(f"{res_char} Integrity: {balance['opens']}/{balance['closes']}")
                
            except Exception as e:
                print(f"❌ Error: {str(e)[:40]}...")

        # 3. CONSOLE & TRACE LOGS
        print("\n[STEP 3] Log & Console Analysis...")
        if args.trace:
            # Check for JS errors trapped in the UI Log
            try:
                # We need to switch back to 'tests' -> 'startup' to see the log if we use visual check
                driver.execute_script("switchTab('tests')")
                driver.execute_script("switchTestView('startup')")
                time.sleep(0.2)
                ui_log = driver.find_element(By.ID, "startup-error-log").text
                err_count = ui_log.lower().count("js-error")
                if err_count > 0:
                    print(f"  -> 🚫 FOUND {err_count} JS Errors in UI Log!")
                else:
                    print("  -> ✅ UI Log clean (No trapped JS errors).")
            except:
                print("  -> ⚠️ Could not read startup-error-log.")

        browser_logs = driver.get_log('browser')
        severe = [l for l in browser_logs if l['level'] == 'SEVERE']
        if severe:
            print(f"  -> ❌ FOUND {len(severe)} SEVERE console errors.")
            if args.verbose:
                for s in severe: print(f"     - {s['message']}")
        else:
            print("  -> ✅ Browser console is clean.")

        print("\n--- Selenium session validation completed ---")
        return True
    except Exception as e:
        print(f"\n[FATAL] Selenium error: {e}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--verbose', action='store_true')
    parser.add_argument('--trace', action='store_true')
    parser.add_argument('--debug', action='store_true')
    parser.add_argument('--dom-control', action='store_true')
    args = parser.parse_args()
    
    success = run_tests(args)
    sys.exit(0 if success else 1)
