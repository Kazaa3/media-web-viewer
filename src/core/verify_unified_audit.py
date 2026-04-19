import os
import sys
import time
import json
from pathlib import Path

# Force Project Root Injection
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Mocking tkinter to bypass PyAutoGUI dependencies in minimal env
from unittest.mock import MagicMock
mock_tk = MagicMock()
mock_tk.TkVersion = 8.6
sys.modules["tkinter"] = mock_tk
sys.modules["tkinter.messagebox"] = MagicMock()

from src.core import api_audit

def verify_unified_engine():
    print("--- [Verification] Unified Forensic Audit Engine (v1.47) ---")
    
    # 1. Generate Unified Audit Report (PyAutoGUI + Liveness + System)
    print("[INFO] Triggering Synchronized Multi-Tier Audit...")
    result = api_audit.generate_unified_audit_report()
    
    if result["status"] == "ok":
        print(f"[OK] Multi-Tier Report generated: {Path(result['report_path']).name}")
        report = result["report"]
        
        # Verify Engines
        py_status = report["engines"]["pyautogui"]["status"]
        print(f"[Engine] PyAutoGUI: {py_status}")
        
        pw_status = report["engines"]["playwright"]
        print(f"[Engine] Playwright: {pw_status}")
        
        sel_status = report["engines"]["selenium"]
        print(f"[Engine] Selenium: {sel_status}")
        
        liveness = report["system"]["liveness"]["status"]
        print(f"[System] Port 8345 Connectivity: {liveness}")
        
    else:
        print(f"[FAIL] Audit Sync failed: {result.get('message')}")

    print("--- Verification Complete ---")

if __name__ == "__main__":
    if sys.platform.startswith('linux') and not os.environ.get('DISPLAY'):
         os.environ['DISPLAY'] = ':0' 
    verify_unified_engine()
