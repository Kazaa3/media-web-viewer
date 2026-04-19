import os
import sys
import time
import json
from pathlib import Path

# Force Project Root Injection
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Mocking tkinter for PyAutoGUI
from unittest.mock import MagicMock
mock_tk = MagicMock()
mock_tk.TkVersion = 8.6
sys.modules["tkinter"] = mock_tk
sys.modules["tkinter.messagebox"] = MagicMock()

from src.core import api_audit

def verify_extended_diagnostics():
    print("--- [Verification] Nuclear Extended Forensic Audit (v1.48) ---")
    
    # 1. Run Extended Audit (Multi-Phase)
    print("[INFO] Launching Nuclear Audit Pulse...")
    result = api_audit.run_extended_forensic_audit()
    
    if result["status"] == "ok":
        print(f"[OK] Extended Report generated: {Path(result['report_path']).name}")
        report = result["report"]
        
        # Verify Phases
        print(f"[Phase 01] Connectivity: {report['phases']['01_connectivity']['status']}")
        print(f"[Phase 02] Structural:   {report['phases']['02_structural']['status']}")
        print(f"[Phase 03] Hydration:    {report['phases']['03_hydration'].get('is_hydrated', 'N/A')}")
        print(f"[Phase 04] Proof:         {report['phases']['04_proof']['status']}")
        
        # Check Findings
        findings = report['phases']['02_structural'].get('findings', {})
        print(f"[Findings] Structural DIVs checked: {len(findings) if findings else 0}")
        
    else:
        print(f"[FAIL] Extended Audit failed: {result.get('message')}")

    print("--- Verification Complete ---")

if __name__ == "__main__":
    if sys.platform.startswith('linux') and not os.environ.get('DISPLAY'):
         os.environ['DISPLAY'] = ':0' 
    verify_extended_diagnostics()
