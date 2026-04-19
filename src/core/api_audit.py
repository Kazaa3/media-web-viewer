"""
api_audit.py — Forensic Audit Engine (v1.46.132)
=================================================
Centralized audit API for the Media Workstation.
Reads all method definitions from GLOBAL_CONFIG["audit_master"].

Exposed Eel functions (via main.py registration):
    - get_audit_config()
    - run_audit(method_id, depth)
    - get_audit_report()
    - toggle_audit_method(method_id, enabled)
    - get_log_audit(depth)
    - get_backend_audit()
"""

import os
import re
import time
import shutil
import logging
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional

from src.core.config_master import (
    GLOBAL_CONFIG,
    PROJECT_ROOT,
    LOGS_DIR,
    SCRIPTS_DIR,
    DB_FILENAME,
)
from src.core import db

log = logging.getLogger("api_audit")

# ---------------------------------------------------------------------------
# Internal Helpers
# ---------------------------------------------------------------------------

def _get_audit_cfg() -> Dict[str, Any]:
    return GLOBAL_CONFIG.get("audit_master", {})


def _get_depth_config(depth: Optional[str] = None) -> Dict[str, Any]:
    cfg = _get_audit_cfg()
    if not depth:
        depth = cfg.get("depth", "standard")
    return cfg.get("depth_config", {}).get(depth, {"log_lines": 500, "dom_checks": True, "screenshots": False})


def _method_enabled(method_id: str) -> bool:
    cfg = _get_audit_cfg()
    if not cfg.get("enabled", True):
        return False
    method = cfg.get("methods", {}).get(method_id, {})
    return method.get("enabled", False)


def _check_requires(method_id: str) -> List[str]:
    """Returns a list of missing required binaries for a given method."""
    cfg = _get_audit_cfg()
    method = cfg.get("methods", {}).get(method_id, {})
    missing = []
    for req in method.get("requires", []):
        if not shutil.which(req):
            missing.append(req)
    return missing


# ---------------------------------------------------------------------------
# Public API — Config & Status
# ---------------------------------------------------------------------------

def get_audit_config() -> Dict[str, Any]:
    """
    Returns the full audit_master configuration with live availability checks.
    Safe to call at any time.
    """
    cfg = _get_audit_cfg()
    methods = cfg.get("methods", {})

    enriched_methods = {}
    for m_id, m_cfg in methods.items():
        missing = _check_requires(m_id)
        enriched_methods[m_id] = {
            **m_cfg,
            "missing_deps": missing,
            "ready": m_cfg.get("enabled", False) and len(missing) == 0,
        }

    return {
        "status": "ok",
        "enabled": cfg.get("enabled", True),
        "depth": cfg.get("depth", "standard"),
        "report_dir": cfg.get("report_dir", str(SCRIPTS_DIR / "audit_reports")),
        "report_format": cfg.get("report_format", "markdown"),
        "auto_run_on_startup": cfg.get("auto_run_on_startup", False),
        "methods": enriched_methods,
    }


def toggle_audit_method(method_id: str, enabled: bool) -> Dict[str, Any]:
    """Toggles an individual audit method on or off at runtime."""
    cfg = _get_audit_cfg()
    methods = cfg.get("methods", {})
    if method_id not in methods:
        return {"status": "error", "message": f"Unknown method: {method_id}"}
    methods[method_id]["enabled"] = bool(enabled)
    log.info(f"[AuditMaster] Method '{method_id}' set to enabled={enabled}")
    return {"status": "ok", "method": method_id, "enabled": enabled}


# ---------------------------------------------------------------------------
# Public API — Built-in Audit Methods
# ---------------------------------------------------------------------------

def get_log_audit(depth: Optional[str] = None) -> Dict[str, Any]:
    """
    Log-file based runtime audit. Scans the main application log
    for ERROR and WARNING entries.
    """
    if not _method_enabled("log_audit"):
        return {"status": "skipped", "reason": "log_audit is disabled"}

    depth_cfg = _get_depth_config(depth)
    max_lines = depth_cfg.get("log_lines", 500)

    log_file = LOGS_DIR / "media_viewer.log"
    if not log_file.exists():
        return {"status": "error", "message": f"Log file not found: {log_file}"}

    errors, warnings = [], []
    try:
        with open(log_file, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
        tail = lines[-max_lines:]
        for line in tail:
            stripped = line.strip()
            if " ERROR " in stripped or " CRITICAL " in stripped:
                errors.append(stripped)
            elif " WARNING " in stripped:
                warnings.append(stripped)
    except Exception as e:
        return {"status": "error", "message": str(e)}

    return {
        "status": "ok",
        "depth": depth or _get_audit_cfg().get("depth", "standard"),
        "lines_scanned": len(tail),
        "error_count": len(errors),
        "warning_count": len(warnings),
        "errors": errors[-50:],      # Cap at 50 for payload size
        "warnings": warnings[-50:],
        "log_file": str(log_file),
    }


def get_backend_audit() -> Dict[str, Any]:
    """
    Probes the backend state: DB connectivity, media item count,
    config integrity, and key runtime flags.
    """
    if not _method_enabled("backend_check"):
        return {"status": "skipped", "reason": "backend_check is disabled"}

    result = {
        "status": "ok",
        "timestamp": time.time(),
        "checks": {},
    }

    # 1. DB Connectivity
    try:
        item_count = len(db.get_all_media())
        result["checks"]["db"] = {"status": "ok", "item_count": item_count, "path": str(DB_FILENAME)}
    except Exception as e:
        result["checks"]["db"] = {"status": "error", "message": str(e)}

    # 2. Config Integrity (key sections present)
    required_sections = ["audit_master", "parser_registry", "storage_registry", "network_settings"]
    missing_sections = [s for s in required_sections if s not in GLOBAL_CONFIG]
    result["checks"]["config"] = {
        "status": "ok" if not missing_sections else "degraded",
        "missing_sections": missing_sections,
    }

    # 3. Binary Availability
    binaries = ["ffmpeg", "ffprobe", "vlc", "mkvmerge"]
    bin_status = {}
    for b in binaries:
        bin_status[b] = "available" if shutil.which(b) else "missing"
    result["checks"]["binaries"] = {"status": "ok", "detail": bin_status}

    # 4. Disk Space
    try:
        usage = shutil.disk_usage(PROJECT_ROOT)
        free_gb = usage.free / (1024 ** 3)
        result["checks"]["disk"] = {
            "status": "ok" if free_gb > 1 else "low",
            "free_gb": round(free_gb, 2),
        }
    except Exception as e:
        result["checks"]["disk"] = {"status": "error", "message": str(e)}

    # Aggregate status
    degraded = [k for k, v in result["checks"].items() if v.get("status") not in ("ok",)]
    if degraded:
        result["status"] = "degraded"
        result["degraded_checks"] = degraded

    return result


def run_audit(method_id: str, depth: Optional[str] = None) -> Dict[str, Any]:
    """
    Universal dispatcher: runs any registered audit method by ID.
    Built-in methods are called directly; script-based methods are spawned.
    """
    cfg = _get_audit_cfg()
    if not cfg.get("enabled", True):
        return {"status": "skipped", "reason": "Audit master is globally disabled"}

    methods = cfg.get("methods", {})
    if method_id not in methods:
        return {"status": "error", "message": f"Unknown audit method: {method_id}"}

    method = methods[method_id]
    if not method.get("enabled", False):
        return {"status": "skipped", "reason": f"Method '{method_id}' is disabled"}

    missing = _check_requires(method_id)
    if missing:
        return {"status": "error", "message": f"Missing dependencies: {missing}"}

    # --- Built-in method dispatch ---
    if method_id == "log_audit":
        return get_log_audit(depth)
    if method_id == "backend_check":
        return get_backend_audit()

    # --- Script-based method dispatch ---
    script = method.get("script")
    if not script or not Path(script).exists():
        return {"status": "error", "message": f"Script not found for '{method_id}': {script}"}

    timeout = method.get("timeout_sec", 30)
    try:
        proc = subprocess.run(
            [str(Path(script))],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=str(PROJECT_ROOT),
        )
        return {
            "status": "ok" if proc.returncode == 0 else "failed",
            "method": method_id,
            "returncode": proc.returncode,
            "stdout": proc.stdout[-4000:],
            "stderr": proc.stderr[-2000:],
        }
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "method": method_id, "timeout_sec": timeout}
    except Exception as e:
        return {"status": "error", "message": str(e)}


def get_audit_report() -> Dict[str, Any]:
    """
    Runs all enabled, ready audit methods and aggregates results
    into a unified forensic report.
    """
    cfg = _get_audit_cfg()
    if not cfg.get("enabled", True):
        return {"status": "skipped", "reason": "Audit master globally disabled"}

    depth = cfg.get("depth", "standard")
    methods = cfg.get("methods", {})
    report = {
        "status": "ok",
        "depth": depth,
        "timestamp": time.time(),
        "results": {},
        "summary": {"ok": 0, "degraded": 0, "failed": 0, "skipped": 0},
    }

    for m_id, m_cfg in methods.items():
        if not m_cfg.get("enabled", False):
            report["results"][m_id] = {"status": "skipped"}
            report["summary"]["skipped"] += 1
            continue

        result = run_audit(m_id, depth)
        report["results"][m_id] = result

        s = result.get("status", "failed")
        if s == "ok":
            report["summary"]["ok"] += 1
        elif s in ("degraded", "timeout"):
            report["summary"]["degraded"] += 1
        elif s == "skipped":
            report["summary"]["skipped"] += 1
        else:
            report["summary"]["failed"] += 1

    if report["summary"]["failed"] > 0:
        report["status"] = "failed"
    elif report["summary"]["degraded"] > 0:
        report["status"] = "degraded"

    return report
