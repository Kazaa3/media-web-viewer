from src.core.eel_shell import eel
import sys
import os
import subprocess
import platform
import time
import re
import shutil
import json
import logging
from pathlib import Path
from typing import Any, Tuple, List, Dict

from .config_master import GLOBAL_CONFIG, PROJECT_ROOT
from .api_core_app import _detect_python_environment

log = logging.getLogger("mwv.api.environment")

_ENV_INFO_CACHE = {
    "data": None,
    "ts": 0.0,
}
_ENV_INFO_CACHE_TTL_SECONDS = 8.0

@eel.expose
def api_ping(client_ts=None, payload_size=0):
    """Eel roundtrip latency diagnostics."""
    now_ms = int(time.time() * 1000)
    try:
        size = int(payload_size)
    except Exception:
        size = 0
    size = max(0, min(size, 200000))
    payload = "x" * size if size > 0 else ""
    return {
        "status": "ok",
        "server_ts": now_ms,
        "client_ts": client_ts,
        "payload_size": size,
        "payload": payload,
    }

def _get_requirements_status():
    """Get install status for requirements.txt packages."""
    import importlib.util
    
    req_locations = [
        PROJECT_ROOT / "requirements.txt",
        PROJECT_ROOT / "infra" / "requirements-run.txt",
    ]
    
    requirements_file = next((loc for loc in req_locations if loc.exists()), None)
    if not requirements_file:
        return {"total": 0, "installed": 0, "missing": []}

    requirement_names = set()
    try:
        content = requirements_file.read_text(encoding="utf-8")
        for line in content.splitlines():
            line = line.strip()
            if not line or line.startswith(("#", "-")): continue
            pkg = re.split(r"(==|>=|<=|~=|!=|>|<|\[)", line, maxsplit=1)[0].strip()
            if pkg: requirement_names.add(pkg)
    except Exception as e:
        log.error(f"Error parsing requirements: {e}")

    installed, missing = [], []
    for pkg_name in requirement_names:
        import_name = pkg_name.replace("-", "_")
        try:
            if importlib.util.find_spec(import_name) is not None:
                installed.append(pkg_name)
            else:
                missing.append(pkg_name)
        except Exception:
            missing.append(pkg_name)

    return {
        "total": len(requirement_names),
        "installed_count": len(installed),
        "missing_count": len(missing),
        "missing": missing
    }

@eel.expose
def pip_install_packages(packages):
    """Installs Python packages via pip."""
    if not packages: return {"status": "ok"}
    if isinstance(packages, str): packages = [packages]
    try:
        cmd = [sys.executable, "-m", "pip", "install", *packages]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        if result.returncode == 0:
            _ENV_INFO_CACHE["data"] = None # Invalidate cache
            return {"status": "ok", "installed": packages}
        return {"status": "error", "error": result.stderr}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@eel.expose
def nuclear_restart():
    """Kills current backend and reboots via script."""
    script_path = PROJECT_ROOT / "scripts" / "reboot_mwv.sh"
    if script_path.exists():
        subprocess.Popen(["bash", str(script_path)], start_new_session=True)
        os._exit(0)
    return {"status": "error", "message": "Reboot script not found."}

@eel.expose
def get_sys_overview(force_refresh=False):
    """Returns comprehensive system and environment telemetry."""
    now = time.time()
    if not force_refresh and _ENV_INFO_CACHE["data"] is not None:
        if (now - _ENV_INFO_CACHE["ts"]) <= _ENV_INFO_CACHE_TTL_SECONDS:
            return _ENV_INFO_CACHE["data"]

    env_info = _detect_python_environment()
    req_status = _get_requirements_status()
    
    # Minimal synthesis for v1.54 dashboard
    result = {
        "python_version": env_info[3] if len(env_info)>3 else platform.python_version(),
        "python_path": sys.executable,
        "env_type": env_info[0] if len(env_info)>0 else "system",
        "requirements": {
            "installed": req_status.get("installed_count", 0),
            "total": req_status.get("total", 0),
            "missing": req_status.get("missing", [])
        }
    }
    
    _ENV_INFO_CACHE["data"] = result
    _ENV_INFO_CACHE["ts"] = now
    return result

@eel.expose
def get_venv_summary():
    """Summary of available project venvs."""
    env_info = _detect_python_environment()
    return {
        "current_environment": {
            "type": env_info[0],
            "name": env_info[1],
            "path": str(env_info[2]),
            "python_version": env_info[3]
        }
    }
