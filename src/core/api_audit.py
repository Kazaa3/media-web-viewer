"""
Forensic Audit Engine (v1.48.01)
Extended Global Audit Hub (PyAutoGUI, Selenium, Playwright, DOM, Hydration).
[AI-Anchor-Hash: 48_AUDIT_GRANULAR_002]
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

# --- Audit Engine Bridges (v1.48) ---

try:
    from src.core.api_diagnostics import verify_frontend_liveness, capture_workstation_screenshot
    log.info("[Audit] Diagnostic bridges established.")
except ImportError:
    log.warning("[Audit] Diagnostic bridges falling back to local mocks.")
    def verify_frontend_liveness(): return {"status": "warn", "message": "Bridge missing"}
    def capture_workstation_screenshot(): return {"status": "error"}

# --- Granular DOM Verification (v1.48 Restored) ---

@eel.expose
def perform_granular_dom_audit():
    """
    Step-by-step verification of critical UI 'Zwischenstufen' (Intermediate Stages).
    Checks for structural DIVs and hydration markers via the Eel bridge.
    """
    log.info("[Audit-DOM] Initializing Granular Structural Audit...")
    
    # 1. Critical Selector Registry
    selectors = [
        "body", "#app", "#main-layout", "#navbar", "#sidebar-nav", 
        "#workspace-container", "#hud-controls", "#media-stage"
    ]
    
    if not hasattr(eel, "verify_dom_elements"):
        log.error("[Audit-DOM] Frontend verification hook 'verify_dom_elements' not found.")
        return {"status": "error", "message": "UI bridge not hydrated."}

    # Atomic pulse to the frontend
    # Expected JS: eel.expose(verify_dom_elements); function verify_dom_elements(selectors) { ... }
    results = eel.verify_dom_elements(selectors)()
    
    log.info(f"[Audit-DOM] Structural findings: {results}")
    return {"status": "ok", "findings": results}

@eel.expose
def trace_hydration_lifecycle():
    """
    Traces the transition from 'Black Hole' to 'Fully Rendered' state.
    Captures intermediate hydration counts for fragments.
    """
    log.info("[Audit-Hydration] Tracing Fragment Lifecycle...")
    
    active_fragments = GLOBAL_CONFIG.get("active_ui_fragments", [])
    hydration_stats = GLOBAL_CONFIG.get("last_hydration_pulse", {})
    
    report = {
        "timestamp": time.time(),
        "fragments_count": len(active_fragments),
        "hydration_markers": hydration_stats,
        "is_hydrated": hydration_stats.get("success", False)
    }
    
    log.info(f"[Audit-Hydration] State: {'HYDRATED' if report['is_hydrated'] else 'STALLED'}")
    return report

# --- Restored Automation Logic (v1.48) ---

def run_playwright_audit():
    """Restores the Playwright UI audit logic."""
    log.info("[Audit-Playwright] Launching Playwright DOM Audit...")
    script_path = Path(FORENSIC_AUDIT_REGISTRY["paths"]["scripts"]) / FORENSIC_AUDIT_REGISTRY["automation_settings"]["playwright_script"]
    if not script_path.exists(): return {"status": "error", "message": "Script missing"}
    
    try:
        result = subprocess.run([sys.executable, str(script_path)], capture_output=True, text=True, timeout=30)
        return {"status": "ok", "output": result.stdout}
    except Exception as e: return {"status": "error", "message": str(e)}

def run_selenium_session_audit(options=None):
    """Restores the Selenium session attachment tests."""
    log.info("[Audit-Selenium] Running Selenium Session Extractor...")
    script_path = Path(FORENSIC_AUDIT_REGISTRY["paths"]["tests"]) / FORENSIC_AUDIT_REGISTRY["automation_settings"]["selenium_script"]
    if not script_path.exists(): return {"status": "error", "message": "Script missing"}
    
    cmd = [sys.executable, str(script_path)]
    if options: cmd.extend(options)
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        return {"status": "ok", "output": result.stdout}
    except Exception as e: return {"status": "error", "message": str(e)}

# --- Extended Multi-Phase Audit (v1.48) ---

@eel.expose
def run_extended_forensic_audit():
    """
    A Nuclear High-Density diagnostic suite for workstation failures.
    Runs in 4 phases: Connectivity -> DOM -> PyAutoGUI -> Automation.
    """
    log.warning("[Audit-Extended] STARTING NUCLEAR FORENSIC AUDIT...")
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "version": "v1.48.01-EXTENDED",
        "phases": {
            "01_connectivity": verify_frontend_liveness(),
            "02_structural":   perform_granular_dom_audit(),
            "03_hydration":    trace_hydration_lifecycle(),
            "04_proof":         capture_workstation_screenshot(),
            "05_automation": {
                "playwright": run_playwright_audit(),
                "selenium":   run_selenium_session_audit()
            }
        }
    }
    
    # Save Report
    report_dir = Path(FORENSIC_AUDIT_REGISTRY["paths"]["reports"])
    report_dir.mkdir(parents=True, exist_ok=True)
    report_file = report_dir / f"extended_audit_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    report_file.write_text(json.dumps(report, indent=4), encoding='utf-8')
    
    log.warning(f"[Audit-Extended] NUCLEAR AUDIT COMPLETE: {report_file.name}")
    return {"status": "ok", "report_path": str(report_file), "report": report}
