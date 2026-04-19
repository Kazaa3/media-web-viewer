import os
import sys
from pathlib import Path
from typing import Dict, Any

from src.core.config_master import PROJECT_ROOT, SRC_DIR
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
