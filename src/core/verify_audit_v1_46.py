import os
import sys
import time
from pathlib import Path

# Force Project Root Injection
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.core import api_diagnostics

def run_standardized_audit():
    print("--- [Verification] Standardized Forensic Audit (v1.46.142) ---")
    
    # 1. Take a screenshot via PyAutoGUI (Compliance Check)
    print("[INFO] Capturing forensic screenshot via PyAutoGUI...")
    ss_result = api_diagnostics.capture_workstation_screenshot()
    if ss_result["status"] == "ok":
        print(f"[OK] Screenshot saved: {ss_result['filename']}")
        print(f"     Path: {ss_result['path']}")
    else:
        print(f"[FAIL] Screenshot failed: {ss_result.get('message')}")

    # 2. Generate Global Audit Report
    print("[INFO] Generating Standardized Global Audit Report...")
    audit_result = api_diagnostics.generate_standardized_audit()
    if audit_result["status"] == "ok":
        print(f"[OK] Audit Report generated: {Path(audit_result['report_path']).name}")
        print(f"     Path: {audit_result['report_path']}")
        
        # Verify Liveness in report
        liveness = audit_result["report"]["connectivity"]["status"]
        print(f"[Audit] Connectivity Status: {liveness}")
    else:
        print(f"[FAIL] Audit Generation failed: {audit_result.get('message')}")

    print("--- Audit Complete ---")

if __name__ == "__main__":
    # Ensure DISPLAY is set for Linux X11-based pyautogui
    if sys.platform.startswith('linux') and not os.environ.get('DISPLAY'):
         os.environ['DISPLAY'] = ':0' 
         
    run_standardized_audit()
