#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: WebSocket Bridge Test
# Eingabewerte: Selenium, src/core/main.py
# Ausgabewerte: WebSocket Connectivity Report
# Testdateien: src/core/main.py, web/app.html
# Kommentar: Verifies the Eel WebSocket bridge by performing a round-trip ping from JS to Python.

import os
import sys
import time
import subprocess
import signal
from pathlib import Path
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def test_websocket_bridge():
    print("\n🧪 Test: WebSocket Bridge Connectivity Scan")
    
    project_root = Path(__file__).parent.parent.absolute()
    main_py = project_root / "src" / "core" / "main.py"
    port = 8346
    
    env = os.environ.copy()
    env["MWV_PORT"] = str(port)
    env["MWV_FORCE_NEW_SESSION"] = "1"
    env["MWV_DISABLE_BROWSER_OPEN"] = "1"
    env["MWV_DEBUG_UI"] = "0"

    print(f"   ├─ Starting backend server on port {port}...")
    log_file = open("tests/websocket_test_startup.log", "w")
    
    # Use .venv_core for the application backend
    core_python = project_root / ".venv_core" / "bin" / "python3"
    if not core_python.exists():
        core_python = Path(sys.executable)

    process = subprocess.Popen(
        [str(core_python), str(main_py)],
        cwd=str(project_root),
        stdout=log_file,
        stderr=subprocess.STDOUT,
        env=env,
        preexec_fn=os.setsid # Ensure we can kill the whole group later
    )

    driver = None
    success = False
    try:
        # Give it time to initialize Eel
        time.sleep(8)
        
        print("   ├─ Initializing Headless Chrome...")
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=chrome_options)
        
        print(f"   ├─ Navigating to http://localhost:{port}/app.html...")
        driver.get(f"http://localhost:{port}/app.html")
        
        # Wait for Eel to be ready
        print("   ├─ Waiting for WebSocket ready state...")
        # We check if eel is defined and if a simple call returns
        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script("return typeof eel !== 'undefined'")
        )
        
        print("   ├─ Executing Eel round-trip ping (JS -> Python -> JS)...")
        # api_ping(client_ts, payload_size)
        start_ts = int(time.time() * 1000)
        result = driver.execute_async_script("""
            var callback = arguments[arguments.length - 1];
            eel.api_ping(Date.now(), 1024)(function(response) {
                callback(response);
            });
        """)
        
        end_ts = int(time.time() * 1000)
        latency = end_ts - start_ts
        
        if result and "payload" in result:
            print(f"   └─ ✅ WebSocket Bridge OK. Latency: {latency}ms. Payload size: {len(result['payload'])} bytes.")
            success = True
        else:
            print("   └─ ❌ WebSocket Bridge Failed: Invalid or empty response.")
            
    except Exception as e:
        print(f"   └─ ❌ WebSocket Bridge Error: {e}")
        # Capture screenshot for debugging if it failed
        if driver:
             driver.save_screenshot("tests/websocket_error.png")
    finally:
        if driver:
            driver.quit()
        if process:
            print(f"   ├─ Shutting down backend server (PID {process.pid})...")
            os.killpg(os.getpgid(process.pid), signal.SIGTERM)
            process.wait(timeout=5)
        log_file.close()

    if success:
        print("\n✅ WebSocket connectivity verified.")
        return True
    return False

if __name__ == "__main__":
    if test_websocket_bridge():
        sys.exit(0)
    else:
        sys.exit(1)
