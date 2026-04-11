#!/usr/bin/env python3
import os
import sys
import time
import subprocess

def check_logs():
    print("[1/3] Checking logs for recovery signals...")
    log_file = "logs/app.log"
    if not os.path.exists(log_file):
        print("FAIL: logs/app.log missing.")
        return False
    
    with open(log_file, "r") as f:
        content = f.read()
        
    found_mock = "[DATA-LIB] STAGE-MOCK" in content or "Injected diagnostic mock item" in content
    found_render = "[LIBRARY-UI] RENDER-START" in content
    found_projected = "[LIBRARY-UI] STAGE-PROJECTED" in content
    
    print(f"  - Mock Injected: {found_mock}")
    print(f"  - Render Started: {found_render}")
    print(f"  - Projection Success: {found_projected}")
    
    return found_mock and found_render

def check_dom():
    print("[2/3] Capturing DOM via Headless Chrome...")
    # This uses the existing audit logic to dump DOM to /tmp/dom_dump_v135.html
    cmd = ["bash", "tests/ui/headless_audit_v135.sh"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    
    dump_path = "/tmp/dom_dump_v135.html"
    if not os.path.exists(dump_path):
        print("FAIL: DOM dump failed.")
        return False
        
    with open(dump_path, "r") as f:
        dom = f.read()
        
    found_mock_string = "[MOCK] System Test Audio" in dom
    print(f"  - Mock Item in DOM: {found_mock_string}")
    
    return found_mock_string

if __name__ == "__main__":
    print("=== Media Viewer Automated Recovery Test ===")
    success = True
    if not check_logs(): success = False
    if not check_dom(): success = False
    
    if success:
        print("\nSUCCESS: Recovery chain verified.")
        sys.exit(0)
    else:
        print("\nFAIL: Recovery chain broken.")
        sys.exit(1)
