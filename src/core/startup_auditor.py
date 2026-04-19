#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
startup_auditor.py - Forensic Integrity & Pre-Flight Validation (v1.52)
Comprehensive Multi-Tier Dependency Audit with Grouped Observations.
[AI-Anchor-Hash: 52_SELF_HEAL_GROUPED_006]
"""

import logging
import sys
import os
import subprocess
import importlib.util
from typing import List, Dict, Any, Tuple

log = logging.getLogger("app.integrity")

# --- MANDATORY CONFIGURATION SCHEMA ---
GOLDEN_SCHEMA = [
    "port", "vlc_port", "mtx_port", "db_filename", "forensic_hydration_registry",
    "ui_evolution_mode", "logging_registry", "ui_settings",
    ("ui_settings", "branch_architecture_registry"), ("ui_settings", "navigation_orchestrator")
]

def run_preflight_audit() -> bool:
    """Executes all integrity checks and returns True if stable."""
    log.info("[Audit] Starting Pre-Flight Integrity Check...")
    
    # 0. Dependency Healing (v1.52 Multi-Tier)
    if not ensure_critical_packages():
        log.critical("[Audit-Deps] FATAL: Multi-tier dependency stability could not be established.")
        return False
        
    # 1. Configuration Audit
    config_ok, config_errors = audit_config()
    if not config_ok:
        for err in config_errors: log.error(f"[Audit-Config] MISSING KEY PATH: {err}")
        return False
        
    # 2. Logic & Module Audit
    logic_ok, logic_errors = audit_logic()
    if not logic_ok:
        for err in logic_errors: log.error(f"[Audit-Logic] SYMBOL FAILURE: {err}")
        return False

    # 3. Hydration Stage Audit (No Real Mode Policy)
    hydr_ok, hydr_errors = audit_hydration_stages()
    if not hydr_ok:
        for err in hydr_errors: log.error(f"[Audit-Hydration] POLICY VIOLATION: {err}")
        return False

    # 4. Database Audit
    db_ok, db_errors = audit_database()
    if not db_ok:
        for err in db_errors: log.error(f"[Audit-DB] ACCESS FAILURE: {err}")
        return False

    log.info("[Audit] SUCCESS: System Integrity Verified. Proceeding to Boot.")
    return True

def ensure_critical_packages() -> bool:
    """
    Forensic Multi-Tier Dependency Auditor (v1.52).
    Checks and restores packages categorized by functional groups.
    """
    try:
        from src.core.config_master import DEPENDENCY_REGISTRY, APP_VERSION_CORE
    except ImportError:
        log.error("[Audit-Deps] Failed to import DEPENDENCY_REGISTRY. Aborting.")
        return False
    
    gov = DEPENDENCY_REGISTRY.get("bootstrap_governance", {})
    skip = gov.get("skip_updates", False)
    force = gov.get("force_updates", False)
    version_only = gov.get("update_on_version_change", True)
    last_version = gov.get("last_updated_version", "")

    # 1. Skip Update Guard
    if skip and not force:
        log.info("[Audit-Deps] Update cycle SKIPPED via --no-update flag.")
        return True # Assume environment is stable or handled manually

    # 2. Version-Change Guard ("lade nur wenn neue version")
    if version_only and not force:
        if APP_VERSION_CORE == last_version:
            log.info(f"[Audit-Deps] System version '{APP_VERSION_CORE}' matches last update. Skipping self-healing.")
            return True

    # 3. Global Enable Switch
    if not DEPENDENCY_REGISTRY.get("auto_install_enabled", True):
        log.warning("[Audit-Deps] Automated installation is DISABLED via global flag.")
        return _verify_all_groups_passive(DEPENDENCY_REGISTRY)

    package_groups = DEPENDENCY_REGISTRY.get("package_groups", {})
    mapping = {
        "pillow": "PIL",
        "vlc": "vlc",
        "m3u8": "m3u8",
        # Default: module_name == package_name
    }
    
    overall_success = True
    
    for group_name, packages in package_groups.items():
        log.info(f"[Audit-Deps] Verifying tier: {group_name.upper()}...")
        
        missing = []
        for pkg in packages:
            module_name = mapping.get(pkg.lower(), pkg)
            if not _is_resource_present(module_name):
                missing.append(pkg)
        
        if not missing:
            log.info(f"[Audit-Deps] Tier {group_name.upper()}: [OK]")
            continue
            
        log.warning(f"[Audit-Deps] Tier {group_name.upper()}: MISSING {missing}")
        
        # Restoration Sequence
        if not _restore_packages(missing, DEPENDENCY_REGISTRY):
            log.error(f"[Audit-Deps] Tier {group_name.upper()}: RESTORATION FAILED.")
            overall_success = False
            
    return overall_success

def _restore_packages(packages: List[str], registry: Dict) -> bool:
    """Orchestrates restoration for a list of packages."""
    local_cache = registry.get("linux_cache_path")
    offline_enforced = registry.get("offline_mode_enforced", False)
    
    for package in packages:
        success = False
        
        # Phase 1: Online
        if not offline_enforced:
            try:
                log.info(f"[Audit-Deps] PHASE-1 [ONLINE]: Installing '{package}'...")
                # [v1.53.001] Linux Stabilization: Use --break-system-packages to bypass PEP 668 in forensic environments
                cmd = [sys.executable, "-m", "pip", "install", "--timeout", "10", package]
                if sys.platform == "linux":
                    cmd.append("--break-system-packages")
                subprocess.check_call(cmd)
                log.info(f"[Audit-Deps] SUCCESS: '{package}' restored from Repository.")
                success = True
            except Exception as e:
                log.debug(f"[Audit-Deps] Phase-1 Failed for '{package}': {e}")

        # Phase 2: Local
        if not success and local_cache and os.path.exists(local_cache):
            try:
                log.info(f"[Audit-Deps] PHASE-2 [LOCAL]: Installing '{package}' from Cache...")
                cmd = [sys.executable, "-m", "pip", "install", "--no-index", "--find-links", str(local_cache), package]
                if sys.platform == "linux":
                    cmd.append("--break-system-packages")
                subprocess.check_call(cmd)
                log.info(f"[Audit-Deps] SUCCESS: '{package}' restored from LOCAL CACHE.")
                success = True
            except Exception as e:
                log.debug(f"[Audit-Deps] Phase-2 Failed for '{package}': {e}")
            
        if not success:
            log.error(f"[Audit-Deps] ABORT: Could not restore mission-critical package '{package}'.")
            return False
            
    return True

def _is_resource_present(module_name: str) -> bool:
    """Verifies module readiness without triggering system dependency alerts."""
    try:
        spec = importlib.util.find_spec(module_name)
        return spec is not None
    except:
        return False

def _verify_all_groups_passive(registry: Dict) -> bool:
    """Passive multi-tier check."""
    package_groups = registry.get("package_groups", {})
    mapping = {"pillow": "PIL"}
    all_ok = True
    for group, packages in package_groups.items():
        missing = [p for p in packages if not _is_resource_present(mapping.get(p.lower(), p))]
        if missing:
            log.error(f"[Audit-Deps] Tier {group.upper()}: MISSING {missing}")
            all_ok = False
        else:
            log.info(f"[Audit-Deps] Tier {group.upper()}: [OK]")
    return all_ok

def audit_config() -> Tuple[bool, List[Any]]:
    """Validates GLOBAL_CONFIG against the Golden Schema."""
    from src.core.config_master import GLOBAL_CONFIG
    errors = []
    for entry in GOLDEN_SCHEMA:
        if isinstance(entry, str):
            if entry not in GLOBAL_CONFIG: errors.append(entry)
        elif isinstance(entry, (tuple, list)):
            curr = GLOBAL_CONFIG
            found = True
            for part in entry:
                if isinstance(curr, dict) and part in curr: curr = curr[part]
                else: found = False; break
            if not found: errors.append(" -> ".join(entry))
    return (len(errors) == 0, errors)

def audit_hydration_stages() -> Tuple[bool, List[str]]:
    """Strictly monitors hydration stages and prevents Real Mode during active tests."""
    from src.core.config_master import GLOBAL_CONFIG
    errors = []
    registry = GLOBAL_CONFIG.get("forensic_hydration_registry", {})
    mode = registry.get("mode", "unknown").lower()
    db_active = registry.get("db_active")
    stage = registry.get("audit_stage")
    if mode == "real": errors.append("Real Mode is STRICTLY PROHIBITED by Pre-Flight Control.")
    if stage == 1 and db_active is True: errors.append(f"Stage 1 (Mock) cannot be active with db_active=True.")
    if mode == "mock" and stage != 1: errors.append(f"Mock Mode but audit_stage is '{stage}' (Expected: 1).")
    return (len(errors) == 0, errors)

def audit_logic() -> Tuple[bool, List[str]]:
    """Verifies that mission-critical functions are importable and functional."""
    errors = []
    try:
        from src.core import api_library
        if not hasattr(api_library, 'get_library'): errors.append("api_library.get_library (Missing)")
        from src.core import db
        if not hasattr(db, 'get_all_media'): errors.append("db.get_all_media (Missing)")
        from src.core import api_reporting
        if not hasattr(api_reporting, 'get_db_stats'): errors.append("api_reporting.get_db_stats (Missing)")
    except Exception as e: errors.append(f"Module Import Failure: {str(e)}")
    return (len(errors) == 0, errors)

def audit_database() -> Tuple[bool, List[str]]:
    """Checks if the configured database path is accessible."""
    from src.core.config_master import GLOBAL_CONFIG
    db_path = GLOBAL_CONFIG.get("db_filename")
    errors = []
    if not db_path: errors.append("Empty db_filename in config")
    elif not os.path.exists(db_path): errors.append(f"DB File not found: {db_path}")
    elif not os.access(db_path, os.R_OK | os.W_OK): errors.append(f"DB File Permission Denied: {db_path}")
    return (len(errors) == 0, errors)

# [v1.53.003-R3] High-Priority Alias for main.py bootstrap
run_audit = run_preflight_audit

if __name__ == "__main__":
    _current = os.path.dirname(os.path.abspath(__file__))
    _proot = os.path.dirname(os.path.dirname(_current))
    if _proot not in sys.path: sys.path.insert(0, _proot)
    logging.basicConfig(level=logging.INFO)
    if run_audit(): log.info("AUDIT SUCCESS"); sys.exit(0)
    else: log.error("AUDIT FAILURE"); sys.exit(1)
