import sys
import os
import time
import socket
import json
import logging
from pathlib import Path
from datetime import datetime

# Robust Eel shell fallback
try:
    from src.core.eel_shell import eel
except ImportError:
    import eel

# High-Fidelity Mocking of tkinter to satisfy PyAutoGUI/pymsgbox dependencies (v1.46.142)
import sys
from unittest.mock import MagicMock
mock_tk = MagicMock()
mock_tk.TkVersion = 8.6
if "tkinter" not in sys.modules:
    sys.modules["tkinter"] = mock_tk
if "tkinter.messagebox" not in sys.modules:
    sys.modules["tkinter.messagebox"] = MagicMock()

import pyautogui
    GLOBAL_CONFIG, PROJECT_ROOT, 
    EEL_SETTINGS, FORENSIC_TOOLS_LIST,
    get_tool_metadata
)
from src.core.logger import get_logger

log = get_logger("api_diagnostics")

# Forensic Audit Registry (v1.46.142)
AUDIT_REPORTS_DIR = PROJECT_ROOT / "logs" / "audit_reports"
AUDIT_REPORTS_DIR.mkdir(parents=True, exist_ok=True)

@eel.expose
def verify_frontend_liveness():
    """
    Standardized Port Liveness Audit (v1.46.142).
    Checks if the workstation frontend is serving on the configured port.
    """
    port = EEL_SETTINGS.get("port", 8345)
    host = EEL_SETTINGS.get("host", "localhost")
    
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(2.0)
            is_open = s.connect_ex((host, port)) == 0
            
        status = "HEALTHY" if is_open else "UNREACHABLE"
        log.info(f"[Audit] Port {port} liveness check: {status}")
        return {"status": status, "port": port, "host": host}
    except Exception as e:
        log.error(f"[Audit] Liveness check failed: {e}")
        return {"status": "ERROR", "message": str(e)}

@eel.expose
def capture_workstation_screenshot():
    """
    Forensic UI Capture via PyAutoGUI.
    Saves a full-screen snapshot of the current workstation state.
    """
    try:
        import pyautogui
        # Ensure display is available for Linux
        if sys.platform.startswith('linux') and not os.environ.get('DISPLAY'):
            return {"status": "error", "message": "No DISPLAY environment variable found."}

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"workstation_snapshot_{timestamp}.png"
        filepath = AUDIT_REPORTS_DIR / filename
        
        screenshot = pyautogui.screenshot()
        screenshot.save(str(filepath))
        
        log.info(f"[Audit] Forensic screenshot saved: {filename}")
        return {"status": "ok", "path": str(filepath), "filename": filename}
    except ImportError:
        return {"status": "error", "message": "PyAutoGUI package not found."}
    except Exception as e:
        log.error(f"[Audit] Screenshot capture failed: {e}")
        return {"status": "error", "message": str(e)}

@eel.expose
def trigger_dom_audit():
    """
    Triggers a hydration pulse in the frontend to verify critical UI components.
    """
    if hasattr(eel, "perform_dom_audit"):
        eel.perform_dom_audit()()
        return {"status": "ok", "message": "DOM audit pulse sent to UI."}
    else:
        return {"status": "error", "message": "Frontend DOM audit hook not found."}

@eel.expose
def audit_dom_state(state_summary):
    """
    Records the structural integrity and liveness of the UI (v1.46.142 Receiver).
    """
    log.warning(f"🛡️ [DOM-AUDIT] Liveness Report Received: {state_summary}")
    # Cache state in GLOBAL_CONFIG for standardized reporting
    GLOBAL_CONFIG["last_dom_audit"] = {
        "timestamp": time.time(),
        "summary": state_summary
    }
    return True

@eel.expose
def generate_standardized_audit():
    """
    Global Environmental Audit Report.
    Consolidates binaries, environment, and connectivity into a signed diagnostic artifact.
    """
    try:
        from src.core.api_testing import get_environment_inventory
        inventory = get_environment_inventory()
        liveness = verify_frontend_liveness()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "station_id": GLOBAL_CONFIG.get("station_id", "STATION_ALPHA"),
            "inventory": inventory,
            "connectivity": liveness,
            "status": "VALIDATED" if liveness["status"] == "HEALTHY" else "FAULTY"
        }
        
        report_file = AUDIT_REPORTS_DIR / f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_file.write_text(json.dumps(report, indent=4), encoding='utf-8')
        
        log.info(f"[Audit] Standardized Global Audit generated: {report_file.name}")
        return {"status": "ok", "report_path": str(report_file), "report": report}
    except Exception as e:
        log.error(f"[Audit] Global audit failed: {e}")
        return {"status": "error", "message": str(e)}
