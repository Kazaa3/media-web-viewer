import sys
import os
import json
import time
import subprocess
from pathlib import Path

# Project structure
from src.core.config_master import PROJECT_ROOT, DB_FILENAME, TEST_DIR, DATA_DIR
SCRIPTS_DIR = PROJECT_ROOT / "scripts"
REPORTS_DIR = SCRIPTS_DIR / "audit_reports"
SCREENSHOTS_DIR = REPORTS_DIR / "screenshots"

# Ensure directories exist
REPORTS_DIR.mkdir(parents=True, exist_ok=True)
SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

# Try to import playwright
try:
    from playwright.sync_api import sync_playwright
except ImportError:
    print("\n[ERROR] Playwright not found.")
    print("Please install it using: pip install playwright && playwright install chromium")
    sys.exit(1)

def run_audit(url=None, headless=True):
    if url:
        print(f"🚀 Connecting to Live Session at {url} (Headless: {headless})...")
        process = None
    else:
        print(f"🚀 Starting Automated App Audit (Headless: {headless})...")
        # 1. Start managed session
        managed_session_py = SCRIPTS_DIR / "managed_session.py"
        process = subprocess.Popen(
            [sys.executable, "-u", str(managed_session_py), "--silent"],
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            cwd=str(PROJECT_ROOT)
        )
        
        # Read the JSON metadata from STDOUT
        metadata_line = process.stdout.readline()
        try:
            session_data = json.loads(metadata_line)
            if session_data["status"] != "ready":
                raise Exception(f"Session failed to reach ready state: {session_data}")
            url = session_data["url"]
            print(f"✅ Managed session started at {url}")
        except Exception as e:
            print(f"❌ Failed to parse session metadata: {e}")
            process.kill()
            return

    audit_results = []
    
    # 2. Start Playwright
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        context = browser.new_context(viewport={'width': 1280, 'height': 800})
        page = context.new_page()
        
        # Track console errors
        console_logs = []
        page.on("console", lambda msg: console_logs.append({"type": msg.type, "text": msg.text}))

        def audit_tab(tab_id, expected_id):
            print(f"🔍 Auditing Tab: {tab_id.ljust(12)}", end="", flush=True)
            try:
                # Trigger tab switch
                page.evaluate(f"switchTab('{tab_id}')")
                time.sleep(1.5) # Wait for animation/render
                
                # Verify visibility
                panel = page.query_selector(f"#{expected_id}")
                is_visible = panel.is_visible() if panel else False
                
                # Screenshot
                shot_rel_path = f"screenshots/tab_{tab_id}.png"
                screenshot_path = REPORTS_DIR / shot_rel_path
                page.screenshot(path=str(screenshot_path))
                
                # Filter errors for this action
                all_logs = [l for l in console_logs]
                errors = [l['text'] for l in all_logs if l['type'] in ["error", "warning"]]
                # (Optional: Filter out known harmless errors)
                
                status = "PASS" if (is_visible and not any("ReferenceError" in e for e in errors)) else "FAIL"
                
                res = {
                    "tab": tab_id,
                    "status": status,
                    "visible": is_visible,
                    "shot_rel_path": shot_rel_path,
                    "console_errors": errors
                }
                audit_results.append(res)
                print(f" {'✅' if status == 'PASS' else '❌'}")
                return res
            except Exception as e:
                print(f" ❌ ERROR: {e}")
                audit_results.append({"tab": tab_id, "status": "ERROR", "message": str(e)})
                return None

        try:
            # Initial load
            page.goto(url, wait_until="networkidle")
            time.sleep(3) # Initial boot time
            
            tabs_to_audit = [
                ('player', 'player-tab-split-container'),
                ('library', 'lib-split-container'),
                ('video', 'player-main-content-pane'),
                ('debug', 'diagnostics-suite-fragment'),
                ('tests', 'diagnostics-health-view'),
                ('logbuch', 'logbook-fragment'),
                ('reporting', 'reporting-main-split-container')
            ]
            
            for tab, panel_id in tabs_to_audit:
                audit_tab(tab, panel_id)
                
        finally:
            browser.close()
            if process:
                process.terminate()

    # 3. Generate Report
    generate_report(audit_results)

def generate_report(results):
    report_path = REPORTS_DIR / "audit_report.md"
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# 🛡️ MWV App Audit Report\n\n")
        f.write(f"**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        f.write("## Summary\n\n")
        passed = len([r for r in results if r["status"] == "PASS"])
        f.write(f"- ✅ **Passed:** {passed}\n")
        f.write(f"- ❌ **Failed/Error:** {len(results) - passed}\n\n")
        
        f.write("## Detailed Results\n\n")
        f.write("| Tab | Status | Visibility | Errors | Screenshot |\n")
        f.write("| --- | --- | --- | --- | --- |\n")
        
        for r in results:
            status_icon = "✅" if r["status"] == "PASS" else "❌"
            err_count = len(r.get("console_errors", []))
            err_text = f"{err_count} errors" if err_count > 0 else "None"
            shot_link = f"[View]({r['shot_rel_path']})" if "shot_rel_path" in r else "N/A"
            f.write(f"| {r['tab']} | {status_icon} {r['status']} | {'Visible' if r.get('visible') else 'Hidden'} | {err_text} | {shot_link} |\n")
            
        f.write("\n## Failure Details\n\n")
        for r in results:
            if r["status"] != "PASS":
                f.write(f"### ❌ Tab: {r['tab']}\n")
                if r.get("console_errors"):
                    f.write("**Console Errors:**\n```\n")
                    f.write("\n".join(r["console_errors"]))
                    f.write("\n```\n")
                if "message" in r:
                    f.write(f"**Error Message:** {r['message']}\n")
                if "shot_rel_path" in r:
                    f.write(f"![{r['tab']}]({r['shot_rel_path']})\n")
                f.write("\n---\n")

    print(f"\n📄 Audit complete. Report generated at: {report_path}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="MWV App Audit (Playwright)")
    parser.add_argument("--url", help="Connect to an existing URL instead of starting a new session")
    parser.add_argument("--headed", action="store_true", help="Run browser in headed mode")
    args = parser.parse_args()
    
    run_audit(url=args.url, headless=not args.headed)
