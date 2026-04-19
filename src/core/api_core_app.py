import time
import os
import sys
import platform
import psutil
from pathlib import Path
from src.core.eel_shell import eel

from typing import Dict, Any
from src.core.config_master import PROJECT_ROOT, SRC_DIR, GLOBAL_CONFIG
from src.core.logger import get_logger

log = get_logger("api_core_app")

def ensure_stable_environment():
    """
    Maintains workstation stability by enforcing the correct virtual environment.
    (Migrated from main.py v1.46.132)
    """
    if os.environ.get("MWV_AUTO_REEXEC") == "1":
        return
        
    targets = [PROJECT_ROOT / ".venv", PROJECT_ROOT / ".venv_run"]
    for v in targets:
        if v.exists():
            venv_python = v / "bin" / "python"
            if venv_python.exists() and os.path.abspath(sys.executable) != os.path.abspath(str(venv_python)):
                log.info(f"[Core-Guard] Switching to Environment: {venv_python}")
                env = os.environ.copy()
                env["MWV_AUTO_REEXEC"] = "1"
                env["PYTHONPATH"] = f"{PROJECT_ROOT}:{SRC_DIR}:{env.get('PYTHONPATH', '')}"
                
                # Using os.execve to replace the current process (Forensic Pulse)
                os.execve(str(venv_python), [str(venv_python)] + sys.argv, env)
                sys.exit(0)

def get_app_identity() -> Dict[str, Any]:
    """Provides unique workstation identity and versioning state."""
    from src.core.config_master import APP_VERSION_FULL, APP_VERSION_BACKEND
    return {
        "identity": "Forensic-Media-Workstation",
        "version": APP_VERSION_FULL,
        "backend": APP_VERSION_BACKEND,
        "platform": sys.platform,
        "root": str(PROJECT_ROOT)
    }

def shutdown_application():
    """Clean shutdown of all workstation components."""
    log.info("[Core] Initiating formal shutdown sequence...")
    from src.core import api_tools
    api_tools.kill_stalled_forensic_processes()
    # Additional cleanup hooks can be added here
    sys.exit(0)

# --- Application Lifecycle API (Migrated from main.py v1.54.018) ---

@eel.expose
def shutdown_backend():
    """ Delegated Bridge to shutdown_application. """
    shutdown_application()

@eel.expose
def heartbeat():
    """ Explicit heartbeat for window health monitoring. """
    GLOBAL_CONFIG["frontend_last_heartbeat"] = time.time()
    return {"status": "ok", "timestamp": time.time()}

@eel.expose
def get_session_id():
    """ Returns the current backend session ID. """
    from src.core.main import SESSION_ID
    return SESSION_ID

# --- Environmental Detection & Lifecycle (Migrated from main.py v1.54.018) ---

def _detect_python_environment():
    """ Detect current Python environment: system, venv, or conda. """
    python_version = platform.python_version()
    python_executable = sys.executable
    in_venv = sys.prefix != sys.base_prefix
    venv_env = os.environ.get('VIRTUAL_ENV')
    if in_venv or venv_env:
        env_path = venv_env or sys.prefix
        return ('venv', Path(env_path).name, env_path, python_version, python_executable)
    conda_env = os.environ.get('CONDA_DEFAULT_ENV')
    conda_prefix = os.environ.get('CONDA_PREFIX')
    if conda_env and conda_prefix:
        return ('conda', conda_env, conda_prefix, python_version, python_executable)
    return ('system', None, sys.prefix, python_version, python_executable)

def find_venv_pid(venv_name):
    """ Locates the PID of a specific virtual environment process. """
    venv_path = str((PROJECT_ROOT / venv_name).resolve())
    for proc in psutil.process_iter(['pid', 'exe', 'cmdline']):
        try:
            exe = proc.info.get('exe')
            if exe and exe.startswith(venv_path): return proc.info['pid']
            cmdline = proc.info.get('cmdline')
            if cmdline and venv_path in ' '.join(cmdline): return proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied): continue
    return None

@eel.expose
def get_system_environment():
    """ Environment Forensic Audit: Provides real-time resource telemetry. """
    try:
        process = psutil.Process()
        cpu_percent = process.cpu_percent(interval=None)
        mem_rss_mb = process.memory_info().rss / (1024 * 1024)
        from src.core.main import APP_START_TIME, APP_VERSION_CORE
        uptime = time.time() - (APP_START_TIME or time.time())
        return {
            "status": "ok",
            "telemetry": {"cpu": f"{cpu_percent:.1f}%", "ram": f"{mem_rss_mb:.1f} MB", "uptime": f"{int(uptime)}s"},
            "platform": {"python": platform.python_version(), "os": platform.system() + " " + platform.release()},
            "pid": os.getpid()
        }
    except Exception as e:
        log.error(f"[Forensic-ENV] Environment Audit Failed: {e}")
        return {"status": "error", "message": str(e)}

@eel.expose
def get_startup_info():
    """ Returns dual-PID forensic info and startup metrics. """
    from src.core.main import APP_START_TIME, APP_VERSION_CORE, SESSION_ID
    return {
        "pid": os.getpid(),
        "boot_duration_sec": round(time.time() - (APP_START_TIME or time.time()), 2),
        "start_time": APP_START_TIME,
        "env": "diagnostic-lab-forensic",
        "version": APP_VERSION_CORE,
        "os": platform.system(),
        "node": platform.node()
    }

@eel.expose
def trigger_workstation_update(force: bool = False):
    """ Manually triggers the forensic self-healing update cycle. """
    log.info(f"🚀 [Governance] Manual Workstation Update Triggered (Force: {force})")
    from src.core.config_master import DEPENDENCY_REGISTRY
    orig_force = DEPENDENCY_REGISTRY["bootstrap_governance"].get("force_updates", False)
    if force: DEPENDENCY_REGISTRY["bootstrap_governance"]["force_updates"] = True
    try:
        from src.core.startup_auditor import ensure_critical_packages
        success = ensure_critical_packages()
        return {"status": "ok" if success else "error", "restored": success}
    except Exception as e:
        log.error(f"❌ [Governance] Runtime Update Failed: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        DEPENDENCY_REGISTRY["bootstrap_governance"]["force_updates"] = orig_force
