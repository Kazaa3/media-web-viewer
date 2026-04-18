#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
startup_auditor.py - Forensic Integrity & Pre-Flight Validation (v1.46.034)
Ensures the system is in a stable state before Eel/Frontend initialization.
"""

import logging
import sys
import os
from typing import List, Dict, Any, Tuple

log = logging.getLogger("app.integrity")

# --- MANDATORY CONFIGURATION SCHEMA ---
# These keys MUST exist in GLOBAL_CONFIG for a safe boot.
# Tuple represents a nested path (e.g. ("ui_settings", "branch_architecture_registry"))
GOLDEN_SCHEMA = [
    "port",
    "vlc_port",
    "mtx_port",
    "db_filename",
    "forensic_hydration_registry",
    "ui_evolution_mode",
    "logging_registry",
    "ui_settings",
    ("ui_settings", "branch_architecture_registry"),
    ("ui_settings", "navigation_orchestrator")
]

def run_preflight_audit() -> bool:
    """
    Executes all integrity checks and returns True if stable.
    """
    log.info("[Audit] Starting Pre-Flight Integrity Check...")
    
    # 1. Configuration Audit
    config_ok, config_errors = audit_config()
    if not config_ok:
        for err in config_errors:
            log.error(f"[Audit-Config] MISSING KEY PATH: {err}")
        return False
        
    # 2. Logic & Module Audit
    logic_ok, logic_errors = audit_logic()
    if not logic_ok:
        for err in logic_errors:
            log.error(f"[Audit-Logic] SYMBOL FAILURE: {err}")
        return False

    # 3. Hydration Stage Audit (No Real Mode Policy)
    hydr_ok, hydr_errors = audit_hydration_stages()
    if not hydr_ok:
        for err in hydr_errors:
            log.error(f"[Audit-Hydration] POLICY VIOLATION: {err}")
        return False

    # 4. Database Audit
    db_ok, db_errors = audit_database()
    if not db_ok:
        for err in db_errors:
            log.error(f"[Audit-DB] ACCESS FAILURE: {err}")
        return False

    log.info("[Audit] SUCCESS: System Integrity Verified. Proceeding to Boot.")
    return True

def audit_config() -> Tuple[bool, List[Any]]:
    """Validates GLOBAL_CONFIG against the Golden Schema."""
    from src.core.config_master import GLOBAL_CONFIG
    errors = []
    
    for entry in GOLDEN_SCHEMA:
        if isinstance(entry, str):
            if entry not in GLOBAL_CONFIG:
                errors.append(entry)
        elif isinstance(entry, (tuple, list)):
            # Nested check
            curr = GLOBAL_CONFIG
            found = True
            for part in entry:
                if isinstance(curr, dict) and part in curr:
                    curr = curr[part]
                else:
                    found = False
                    break
            if not found:
                errors.append(" -> ".join(entry))
    
    return (len(errors) == 0, errors)

def audit_hydration_stages() -> Tuple[bool, List[str]]:
    """Strictly monitors hydration stages and prevents Real Mode during active tests."""
    from src.core.config_master import GLOBAL_CONFIG
    errors = []
    
    registry = GLOBAL_CONFIG.get("forensic_hydration_registry", {})
    mode = registry.get("mode", "unknown").lower()
    db_active = registry.get("db_active")
    stage = registry.get("audit_stage")

    if mode == "real":
        errors.append("Real Mode is STRICTLY PROHIBITED by Pre-Flight Control.")

    if stage == 1 and db_active is True:
        errors.append(f"Stage 1 (Mock) cannot be active simultaneously with 'db_active=True'.")

    if mode == "mock" and stage != 1:
        errors.append(f"Mock Mode configured but audit_stage is '{stage}' (Expected: 1).")

    return (len(errors) == 0, errors)

def audit_logic() -> Tuple[bool, List[str]]:
    """Verifies that mission-critical functions are importable and functional."""
    errors = []
    try:
        from src.core import api_library
        if not hasattr(api_library, 'get_library'):
            errors.append("api_library.get_library (Missing)")
        
        from src.core import db
        if not hasattr(db, 'get_all_media'):
            errors.append("db.get_all_media (Missing)")

        from src.core import api_reporting
        if not hasattr(api_reporting, 'get_db_stats'):
            errors.append("api_reporting.get_db_stats (Missing)")
            
    except Exception as e:
        errors.append(f"Module Import Failure: {str(e)}")
        
    return (len(errors) == 0, errors)

def audit_database() -> Tuple[bool, List[str]]:
    """Checks if the configured database path is accessible."""
    from src.core.config_master import GLOBAL_CONFIG
    db_path = GLOBAL_CONFIG.get("db_filename")
    errors = []
    
    if not db_path:
        errors.append("Empty db_filename in config")
        return False, errors
        
    if not os.path.exists(db_path):
        errors.append(f"DB File not found: {db_path}")
    elif not os.access(db_path, os.R_OK | os.W_OK):
        errors.append(f"DB File Permission Denied: {db_path}")
        
    return (len(errors) == 0, errors)

if __name__ == "__main__":
    # Internal CLI test
    import os
    _current = os.path.dirname(os.path.abspath(__file__))
    _proot = os.path.dirname(os.path.dirname(_current))
    if _proot not in sys.path:
        sys.path.insert(0, _proot)

    logging.basicConfig(level=logging.INFO)
    if run_preflight_audit():
        print("Pre-flight SUCCESS")
        sys.exit(0)
    else:
        print("Pre-flight FAILURE")
        sys.exit(1)
