"""
Forensic Audit Engine (v1.47.02)
Standardized Global Audit Hub for PyAutoGUI, Selenium, and Playwright.
[AI-Anchor-Hash: 47_AUDIT_CORE_001]
"""
import sys
import os
import time
import json
import subprocess
from pathlib import Path
from datetime import datetime

# Unified Forensic Registry
from src.core.config_master import (
    GLOBAL_CONFIG, PROJECT_ROOT, 
    FORENSIC_AUDIT_REGISTRY, EEL_SETTINGS
)
from src.core.logger import get_logger

log = get_logger("api_audit")

# --- Audit Engine Bridges (v1.47) ---

try:
    from src.core.api_diagnostics import verify_frontend_liveness, capture_workstation_screenshot, audit_dom_state
    log.info("[Audit] Diagnostic bridges established.")
except ImportError:
    log.warning("[Audit] Diagnostic bridges missing. Using minimal local implementation.")
    def verify_frontend_liveness(): return {"status": "warn", "message": "Bridge missing"}
    def capture_workstation_screenshot(): return {"status": "error"}
    def audit_dom_state(state): return True

# --- Unified Automation Logic (Restored v1.47) ---

def run_playwright_audit():
    """
    Restores the Playwright-based UI structural audit.
    Delegates to the scripts/app_audit_playwright.py component.
    """
    log.info("[Audit-Playwright] Initializing High-Fidelity DOM pulse...")
    script_path = Path(FORENSIC_AUDIT_REGISTRY["paths"]["scripts"]) / FORENSIC_AUDIT_REGISTRY["automation_settings"]["playwright_script"]
    
    if not script_path.exists():
        return {"status": "error", "message": "Playwright script not found."}
        
    try:
        # Standardized subprocess execution via project venv
        result = subprocess.run(
            [sys.executable, str(script_path)],
            capture_output=True, text=True, timeout=FORENSIC_AUDIT_REGISTRY["automation_settings"]["timeout"]
        )
        return {"status": "ok" if result.returncode == 0 else "error", "output": result.stdout}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def run_selenium_session_audit(options=None):
    """
    Restores the Selenium-based session attachment tests.
    Targets existing workstation windows for forensic state extraction.
    """
    log.info("[Audit-Selenium] Attaching to active session testbed...")
    script_path = Path(FORENSIC_AUDIT_REGISTRY["paths"]["tests"]) / FORENSIC_AUDIT_REGISTRY["automation_settings"]["selenium_script"]
    
    if not script_path.exists():
        return {"status": "error", "message": "Selenium test script not found."}

    cmd = [sys.executable, str(script_path)]
    if options: cmd.extend(options)

    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return {"status": "ok", "output": result.stdout}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def run_pyautogui_proof():
    """
    Standardizes the PyAutoGUI forensic proof capture via the diagnostic bridge.
    """
    log.info("[Audit-PyAutoGUI] Capturing forensic screenshotproof...")
    return capture_workstation_screenshot()

# --- Integrated Global Audit Entrypoint ---

def generate_unified_audit_report():
    """
    Consolidates ALL forensic metrics (PyAutoGUI, Selenium, Playwright, DOM, Logging).
    [AI-Anchor: AUDIT_SYNC_V1]
    """
    log.info("[Audit-Engine] Synchronizing Multi-Tier Forensic Data...")
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "registry_version": "v1.47.02",
        "engines": {
            "pyautogui":  run_pyautogui_proof(),
            "playwright": run_playwright_audit() if "playwright" in FORENSIC_AUDIT_REGISTRY["enabled_engines"] else "DISABLED",
            "selenium":   run_selenium_session_audit() if "selenium" in FORENSIC_AUDIT_REGISTRY["enabled_engines"] else "DISABLED"
        },
        "system": {
             "liveness": verify_frontend_liveness(),
             "dom_cache": GLOBAL_CONFIG.get("last_dom_audit", "PENDING")
        }
    }
    
    # Save standardized artifact
    report_dir = Path(FORENSIC_AUDIT_REGISTRY["paths"]["reports"])
    report_dir.mkdir(parents=True, exist_ok=True)
    
    filename = f"unified_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    filepath = report_dir / filename
    filepath.write_text(json.dumps(report, indent=4), encoding='utf-8')
    
    log.info(f"[Audit-Engine] Unified Multi-Tier Report generated: {filename}")
    return {"status": "ok", "report_path": str(filepath), "report": report}
