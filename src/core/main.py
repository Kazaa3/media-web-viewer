#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
dict - Desktop Media Player and Library Manager

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

# main.py – Entry point: initializes Eel, exposes API functions to the frontend, and starts the app.

import sys
import os
import platform
import time
from pathlib import Path

# Performance Telemetry: Global startup anchor
STARTUP_TIME = time.time()

# --- Path Bootstrapping & Import Normalization ---
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
# Ensure project root is in sys.path for absolute imports from src
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
# Add src/ for absolute imports (core, parsers)
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))
for sub in ["core", "parsers"]:
    sub_path = str(SRC_DIR / sub)
    if sub_path not in sys.path:
        sys.path.insert(0, sub_path)

def _detect_python_environment():
    """
    Detect current Python environment: system, venv, or conda.
    Returns tuple: (env_type, env_name, env_path, python_version, python_executable)
    """
    python_version = platform.python_version()
    python_executable = sys.executable
    
    # Check for venv
    in_venv = sys.prefix != sys.base_prefix
    venv_env = os.environ.get('VIRTUAL_ENV')
    
    if in_venv or venv_env:
        env_path = venv_env or sys.prefix
        env_name = Path(env_path).name if env_path else 'venv'
        return ('venv', env_name, env_path, python_version, python_executable)

    # Check for conda
    conda_env = os.environ.get('CONDA_DEFAULT_ENV')
    conda_prefix = os.environ.get('CONDA_PREFIX')
    
    if conda_env and conda_prefix:
        return ('conda', conda_env, conda_prefix, python_version, python_executable)
    
    # System Python
    return ('system', None, sys.prefix, python_version, python_executable)

# Benötigte Module importieren
try:
    from src.core.models import MediaItem
    import src.core.db as db
    import src.core.logger as logger
except ModuleNotFoundError as exc:
    missing_module = exc.name or "unknown"
    core_dir = Path(__file__).resolve().parent
    project_dir = core_dir.parent.parent
    local_venv_python = project_dir / ".venv_core" / "bin" / "python"
    already_reexecuted = os.environ.get("MWV_AUTO_REEXEC") == "1"

    # Auto-fallback: if started with wrong interpreter, re-exec with local .venv_core Python.
    if (
        not already_reexecuted
        and local_venv_python.is_file()
        and os.access(local_venv_python, os.X_OK)
        and Path(sys.executable).resolve() != local_venv_python.resolve()
    ):
        print(
            f"\nℹ️ Fehlende Abhängigkeit '{missing_module}' in aktueller Umgebung erkannt.\n"
            f"→ Starte automatisch neu mit Projekt-Umgebung:\n"
            f"  {local_venv_python}\n"
        )
        os.environ["MWV_AUTO_REEXEC"] = "1"
        os.execv(str(local_venv_python), [str(local_venv_python), str(Path(__file__).resolve()), *sys.argv[1:]])

    env_type, env_name, env_path, py_ver, py_exec = _detect_python_environment()

    if env_type == 'conda':
        current_env = f"📦 Conda: {env_name}\n   Pfad: {env_path}\n   Python: {py_exec}"
    elif env_type == 'venv':
        current_env = f"📦 Venv: {env_name}\n   Pfad: {env_path}\n   Python: {py_exec}"
    else:
        current_env = f"⚙️  System Python {py_ver}\n   Python: {py_exec}"

    print(
        f"\n❌ Abhängigkeit '{missing_module}' nicht installiert!\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📍 Aktuelle Umgebung:\n   {current_env}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"✅ Lösung: Starte mit der Projekt-Umgebung:\n\n"
        f"   cd {project_dir}\n"
        f"   source .venv_core/bin/activate\n"
        f"   python main.py\n\n"
        f"Falls .venv_core fehlt:\n"
        f"   python3 -m venv .venv_core\n"
        f"   source .venv_core/bin/activate\n"
        f"   pip install -r requirements.txt\n\n"
        f"Alternative: Mit Conda (falls verfügbar):\n"
        f"   conda activate <env-name>\n"
        f"   pip install -r requirements.txt\n"
        f"   python main.py\n"
    )
    raise SystemExit(1) from exc

import eel
import logging
import time
import subprocess
import threading
import re
import shutil
from typing import cast
from src.parsers.format_utils import (
    PARSER_CONFIG, load_parser_config, save_parser_config,
    AUDIO_EXTENSIONS, VIDEO_EXTENSIONS
)
import env_handler
import logger
from logger import get_logger

try:
    import vlc
    HAS_VLC = True
except ImportError:
    HAS_VLC = False

try:
    import m3u8
    HAS_M3U8 = True
except ImportError:
    HAS_M3U8 = False

_logger = get_logger("click_events")


def process_any_file(path: str) -> str:
    """Compatibility wrapper used by tests: process a file and return JSON string.
    Returns JSON string with either {'success': True, 'duration': ..., 'tags': {...}}
    or {'error': '...'} on failure.
    """
    import json
    try:
        from src.parsers.media_parser import extract_metadata
        from pathlib import Path as _Path
        filename = _Path(path).name
        duration, tags = extract_metadata(path, filename, mode='ultimate')
        return json.dumps({"success": True, "duration": duration, "tags": tags})
    except Exception as e:
        _logger.exception("process_any_file failed")
        return json.dumps({"error": str(e)})


# --- Compatibility stubs expected by tests ---
@eel.expose
def get_server_status():
    """Return a minimal server status dict used by unit tests and frontend checks."""
    try:
        return {
            "status": "ok",
            "version": VERSION,
            "time": int(time.time()),
        }
    except Exception:
        return {"status": "error"}


@eel.expose
def handle_click_batch(events):
    """Process a list of click events (compatibility helper for tests)."""
    results = []
    for ev in (events or []):
        try:
            et = ev.get("type") if isinstance(ev, dict) else None
            payload = ev.get("payload") if isinstance(ev, dict) else {}
            results.append(handle_click(et, payload))
        except Exception:
            results.append({"ok": False, "error": "processing_failed"})
    return {"results": results}


@eel.expose
def api_extract_metadata(path, name=None, mode='lightweight'):
    """Expose metadata extraction in a consistent dict form for tests/frontend."""
    try:
        from src.parsers.media_parser import extract_metadata
        if name is None:
            name = Path(path).name
        res = extract_metadata(path, name, mode=mode)
        # Normalize: prefer (duration, tags) shape
        duration = 0
        tags = {}
        if isinstance(res, tuple) and len(res) >= 2:
            a, b = res[0], res[1]
            if isinstance(a, (int, float)):
                duration = int(a)
                tags = b or {}
            elif isinstance(a, dict):
                tags = a
                if isinstance(b, (int, float)):
                    duration = int(b)
                elif isinstance(b, dict):
                    duration = int(b.get('duration', 0) or 0)
        elif isinstance(res, dict):
            tags = res
            duration = int(tags.get('duration', 0) or 0)
        return {"duration": duration, "tags": tags}
    except Exception as e:
        _logger.exception("api_extract_metadata failed")
        return {"error": str(e)}


def _get_installed_packages():
    """Return list of installed packages (name/version) and source.

    Lightweight implementation for tests that inspect main.py. Not exhaustive.
    """
    packages = []
    source = "pip"
    try:
        import importlib.metadata
        try:
            for dist in importlib.metadata.distributions():
                try:
                    pkg_name = dist.metadata['Name'] if dist.metadata and 'Name' in dist.metadata else dist.metadata.get('Name', None) if dist.metadata else None
                except Exception:
                    pkg_name = getattr(dist, 'metadata', None)
                try:
                    version = dist.version
                except Exception:
                    version = None
                if pkg_name:
                    packages.append({"name": pkg_name, "version": version})
            packages = sorted([p for p in packages if p.get('name')], key=lambda x: x['name'].lower())
            source = 'importlib.metadata'
        except Exception:
            # best-effort: if importlib.metadata iteration fails, fall through to pip fallback
            pass
    except Exception:
        pass

    if not packages:
        try:
            import sys, subprocess, json
            # Fallback to pip list via subprocess
            result = subprocess.run([sys.executable, '-m', 'pip', 'list', '--format=json'], capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                data = json.loads(result.stdout or '[]')
                packages = sorted([{"name": i.get('name'), "version": i.get('version')} for i in data], key=lambda x: x['name'].lower() if x.get('name') else '')
                source = 'pip'
        except Exception:
            packages = []
            source = 'none'

    return packages, source



@eel.expose
def handle_click(event_type: str, payload: dict):
    """
    Generic click-event handler called from the frontend.
    event_type: short string describing action (e.g. "pin", "play", "open")
    payload: dict with additional data (e.g. {"id": 42})
    """
    try:
        _logger.info("click event received", extra={"event": event_type, "payload": payload})
        # simple dispatch examples (extend as needed)
        if event_type == "pin":
            media_id = payload.get("id")
            # example: toggle pin state in db (implement db.toggle_pin if available)
            try:
                from db import toggle_pin
                toggled = toggle_pin(media_id)
                return {"ok": True, "action": "pin_toggled", "id": media_id, "toggled": toggled}
            except Exception:
                _logger.exception("pin action failed")
                return {"ok": False, "error": "pin_failed"}
        elif event_type == "play":
            path = payload.get("path")
            try:
                play_media(path)  # assumes play_media is defined/exposed
                return {"ok": True, "action": "play", "path": path}
            except Exception:
                _logger.exception("play action failed")
                return {"ok": False, "error": "play_failed"}
        else:
            _logger.debug("unhandled click event", extra={"event": event_type})
            return {"ok": True, "action": "noop", "event": event_type}
    except Exception:
        _logger.exception("handle_click unexpected error")
        return {"ok": False, "error": "internal_error"}


# Version laden
VERSION_FILE = PROJECT_ROOT / "VERSION"
try:
    VERSION = VERSION_FILE.read_text(encoding='utf-8').strip()
except Exception:
    VERSION = "1.34"  # Fallback
# --- Imprint/Impressum API ---
@eel.expose
def get_imprint_info():
    """
    Returns license, version, and maintainer info for imprint/impressum tab.
    """
    return {
        "version": VERSION,
        "developer": "kazaa3",
        "location": "Germany",
        "privacy": "Local storage in SQLite. No data transmission to external servers.",
        "license": "GNU GPL-3.0",
        "last_fix": "dict",
    }

@eel.expose
def get_version():
    """Returns the application version."""
    return VERSION

@eel.expose
def get_app_name():
    """Returns the application name."""
    return "dict"

# --- Environment Info API ---
@eel.expose
def get_environment_info_dict():
    """
    Returns full environment info dict for debug/console display.
    """
    import platform
    import sys
    env_type, env_name, env_path, py_ver, py_exec = _detect_python_environment()
    return {
        "env_type": env_type,
        "env_name": env_name,
        "env_path": env_path,
        "python_version": py_ver,
        "python_executable": py_exec,
        "platform": platform.platform(),
        "venv_active": sys.prefix != sys.base_prefix,
        "cwd": str(Path.cwd()),
        "os": platform.system(),
        "release": platform.release(),
        "machine": platform.machine(),
        "debug_flags": DEBUG_FLAGS,
    }

# --- Debug Console API ---
@eel.expose
def get_debug_console():
    """
    Returns debug logs, environment info, and dicts for GUI console.
    """
    from logger import get_ui_logs
    return {
        "logs": get_ui_logs(),
        "env": get_environment_info_dict(),
        "version": VERSION,
        "license": "GNU GPL-3.0",
        "debug_flags": DEBUG_FLAGS,
    }

@eel.expose
def save_tags_to_file(name, tags):
    """
    Writes updated tags to the media file and updates the DB.
    """
    try:
        path = db.get_path_by_name(name)
        if not path:
            return {"status": "error", "message": f"Datei '{name}' nicht in DB gefunden."}
        
        success = tag_writer.write_tags(path, tags)
        if success:
            db.update_media_tags(name, tags, tags.get('full_tags', {}))
            return {"status": "success", "message": f"Tags erfolgreich in '{name}' gespeichert."}
        else:
            return {"status": "error", "message": "Fehler beim Schreiben der Dateitags."}
    except Exception as e:
        logging.exception("save_tags_to_file failed")
        return {"status": "error", "message": str(e)}


@eel.expose
def get_all_parser_info():
    """Returns aggregated capabilities and settings schemas for all parsers."""
    from src.parsers.media_parser import get_parser_info
    return get_parser_info()


@eel.expose
def get_all_parser_settings():
    """Returns the current granular settings for all parsers."""
    return PARSER_CONFIG.get("parser_settings", {})


@eel.expose
def update_parser_settings(new_settings):
    """Updates the granular parser settings and saves to disk."""
    PARSER_CONFIG["parser_settings"].update(new_settings)
    save_parser_config()
    return {"status": "success"}


# --- Debug/Test API ---
@eel.expose
def run_debug_test():
    """
    Runs a simple debug test and returns result for GUI console.
    """
    import sys
    return {
        "test": "debug",
        "python_version": sys.version,
        "cwd": str(Path.cwd()),
        "result": "OK",
    }

_ENV_INFO_CACHE = {
    "data": None,
    "ts": 0.0,
}
_ENV_INFO_CACHE_TTL_SECONDS = 8.0



@eel.expose
def api_ping(client_ts=None, payload_size=0):
    """
    @brief Lightweight ping endpoint for Eel roundtrip latency diagnostics.
    @details Minimal payload endpoint to measure frontend↔backend roundtrip and payload transfer time.
    @param client_ts Optional client timestamp / Optionaler Client-Timestamp.
    @param payload_size Optional echo payload size in bytes (0..200000) / Optionale Echo-Payload.
    @return Dictionary with timestamps and payload size / Dictionary mit Zeitstempeln und Payload-Größe.
    """
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


@eel.expose
def pip_install_packages(packages):
    """
    @brief Installs a list of Python packages via pip.
    @param packages List of package names to install.
    @return Dictionary with status, output, and error message if any.
    """
    if not packages:
        return {"status": "ok", "message": "No packages to install"}
    
    if isinstance(packages, str):
        packages = [packages]

    try:
        # Using sys.executable to ensure we install in the current environment
        cmd = [sys.executable, "-m", "pip", "install", *packages]
        logging.info(f"Running pip install: {' '.join(cmd)}")
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=300 # 5 minutes timeout for installation
        )
        
        if result.returncode == 0:
            logging.info(f"Successfully installed packages: {', '.join(packages)}")
            # After installation, we should probably clear the environment info cache
            _ENV_INFO_CACHE["data"] = None
            _ENV_INFO_CACHE["ts"] = 0.0
            # Double check if they are really installed now
            status = _get_requirements_status() # Assuming _get_requirements_status is defined elsewhere
            still_missing = []
            for p in packages:
                # Normalize names for comparison (requirements.txt might have case differences)
                if any(p.lower() == m.lower() for m in status.get("missing", [])):
                    still_missing.append(p)
            
            if still_missing:
                logging.error(f"[PIP] Installation reported success but packages still missing: {still_missing}")
                return {
                    "status": "error", 
                    "error": f"Verification failed. Packages still missing: {', '.join(still_missing)}",
                    "output": result.stdout
                }
            
            return {"status": "ok", "output": result.stdout, "installed": packages}
        else:
            error_msg = result.stderr or result.stdout or "Unknown pip error"
            logging.error(f"Failed to install packages: {error_msg}")
            return {
                "status": "error",
                "error": error_msg,
                "output": result.stdout
            }
            
    except subprocess.TimeoutExpired:
        logging.error("Pip install timed out")
        return {"status": "error", "error": "Installation timed out"}
    except Exception as e:
        logging.error(f"Error during pip install: {str(e)}")
        return {"status": "error", "error": str(e)}
def _get_requirements_status():
    """Get install status for requirements.txt packages in current interpreter."""
    import importlib.util

    requirements_file = PROJECT_ROOT / "requirements.txt"
    status = {
        "available": requirements_file.exists(),
        "total": 0,
        "installed_count": 0,
        "missing_count": 0,
        "installed": [],
        "missing": [],
    }

    if not requirements_file.exists():
        return status

    import_overrides = {
        "python-vlc": "vlc",
        "bottle-websocket": "bottle_websocket",
        "gevent-websocket": "geventwebsocket",
        "pytest-cov": "pytest_cov",
        "pyinstaller": "PyInstaller",
        "pillow": "PIL",
    }

    requirement_names = set()
    try:
        for raw_line in requirements_file.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith(("-r", "--")):
                continue

            line = line.split(" #", 1)[0].split(";", 1)[0].strip()
            if not line:
                continue

            if " @ " in line:
                package_name = line.split(" @ ", 1)[0].strip()
            else:
                package_name = re.split(r"(==|>=|<=|~=|!=|>|<)", line, maxsplit=1)[0].strip()

            if package_name:
                requirement_names.add(package_name)
    except Exception as e:
        status["error"] = str(e)  # type: ignore
        return status

    installed = []
    missing = []
    for package_name in requirement_names:
        import_name = import_overrides.get(package_name.lower(), package_name.replace("-", "_"))
        if not import_name:
            missing.append(package_name)
            continue
        try:
            if importlib.util.find_spec(import_name) is not None:
                installed.append(package_name)
            else:
                missing.append(package_name)
        except Exception:
            missing.append(package_name)

    installed.sort(key=str.lower)
    missing.sort(key=str.lower)

    status["installed"] = installed
    status["missing"] = missing
    status["total"] = len(requirement_names)
    status["installed_count"] = len(installed)
    status["missing_count"] = len(missing)
    return status



@eel.expose
def get_environment_info(force_refresh=False):
    """
    @brief Returns comprehensive information about the Python environment.
    @details Gibt detaillierte Informationen über die Python-Umgebung zurück, 
             inklusive aktuelle Umgebung, System Python Installationen, und Conda Umgebungen.
    @return Dictionary with environment details / Dictionary mit Umgebungsdetails.
    """
    import platform
    import subprocess
    import json

    now = time.time()
    if not force_refresh and _ENV_INFO_CACHE["data"] is not None:
        if (now - float(_ENV_INFO_CACHE["ts"])) <= _ENV_INFO_CACHE_TTL_SECONDS:
            return _ENV_INFO_CACHE["data"]
    
    # ===== Current Environment =====
    # Check if we're in a virtual environment (venv/virtualenv)
    in_venv = sys.prefix != sys.base_prefix
    venv_path = sys.prefix if in_venv else None
    
    # Get VIRTUAL_ENV environment variable (more reliable for venv)
    venv_env = os.environ.get('VIRTUAL_ENV', None)
    
    # Check for Conda environment
    conda_env_name = os.environ.get('CONDA_DEFAULT_ENV', None)
    conda_prefix = os.environ.get('CONDA_PREFIX', None)
    in_conda = conda_env_name is not None or conda_prefix is not None
    
    # Determine active runtime environment type and path
    # Priority: active interpreter/venv > conda shell context > system
    env_type = None
    env_path = None
    env_name = None
    
    if in_venv or venv_env:
        env_type = "venv"
        env_path = venv_path or venv_env
        env_name = Path(env_path).name if env_path else None
    elif in_conda:
        env_type = "conda"
        env_path = conda_prefix
        env_name = conda_env_name
    else:
        env_type = "system"
    
    # Build current environment info
    current_env = {
        "type": env_type,
        "name": env_name,
        "path": env_path,
        "python_version": platform.python_version(),
        "python_executable": sys.executable,
    }
    
    # ===== Alternative Environments Discovery =====
    
    def _get_conda_environments():
        """Get list of available Conda environments."""
        environments = []
        try:
            # Main conda call with reduced timeout (3s)
            result = subprocess.run(
                ["conda", "env", "list", "--json"],
                capture_output=True,
                text=True,
                timeout=3
            )
            if result.returncode == 0:
                try:
                    data = json.loads(result.stdout)
                    for env_path in data.get("envs", []):
                        try:
                            env_name = Path(env_path).name
                            env_python = Path(env_path) / "bin" / "python"
                            
                            # Check existence and version with timeout (1s)
                            if env_python.exists():
                                v_result = subprocess.run(
                                    [str(env_python), "--version"],
                                    capture_output=True,
                                    text=True,
                                    timeout=1
                                )
                                version = v_result.stdout.strip() or v_result.stderr.strip()
                                is_recommended = env_name == "p14"
                                
                                environments.append({
                                    "name": env_name,
                                    "path": env_path,
                                    "version": version,
                                    "recommended": is_recommended
                                })
                        except (subprocess.TimeoutExpired, Exception):
                            continue
                except (json.JSONDecodeError, KeyError):
                    pass
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            pass
        return sorted(environments, key=lambda x: x["name"])
    
    def _get_system_pythons():
        """Get list of system Python installations."""
        pythons = []
        search_paths = ["/usr/bin", "/usr/local/bin", "/opt/python"]
        seen_versions = set()
        
        for search_path in search_paths:
            try:
                search_dir = Path(search_path)
                if not search_dir.exists():
                    continue
                
                # Use a specific glob to avoid listing too many files
                for python_exe in search_dir.glob("python3*"):
                    try:
                        if not python_exe.is_file() or not os.access(python_exe, os.X_OK):
                            continue
                        
                        result = subprocess.run(
                            [str(python_exe), "--version"],
                            capture_output=True,
                            text=True,
                            timeout=1
                        )
                        version = result.stdout.strip() or result.stderr.strip()
                        
                        if version and version not in seen_versions:
                            seen_versions.add(version)
                            pythons.append({
                                "path": str(python_exe),
                                "version": version
                            })
                    except (subprocess.TimeoutExpired, Exception):
                        pass
            except Exception:
                pass
        
        return sorted(pythons, key=lambda x: x["version"])
    
    def _get_packages_fallback():
        """Fallback method to get packages if pip list fails."""
        packages = []
        try:
            from importlib import metadata
            for dist in metadata.distributions():
                name = dist.metadata.get("Name") or dist.metadata.get("name")
                version = dist.version
                if not name:
                    continue
                packages.append({
                    "name": name,
                    "version": version
                })
            packages = sorted(packages, key=lambda x: x["name"].lower())
        except Exception:
            try:
                import pkg_resources
                for dist in pkg_resources.working_set:
                    packages.append({
                        "name": dist.project_name,
                        "version": dist.version
                    })
                packages = sorted(packages, key=lambda x: x["name"].lower())
            except Exception:
                pass
        return packages
    
    def _get_installed_packages():
        """Get list of installed packages in current environment."""
        packages = []
        source = "none"

        def _parse_columns_output(raw_text: str):
            parsed = []
            lines = [line.strip() for line in (raw_text or "").splitlines() if line.strip()]
            if not lines:
                return parsed
            for line in lines:
                if line.lower().startswith("package") and "version" in line.lower():
                    continue
                if set(line) <= set("- "):
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    parsed.append({"name": parts[0], "version": parts[1]})
            return parsed

        try:
            # Primary method: pip list --format=json (timeout 5s)
            result = subprocess.run(
                [sys.executable, "-m", "pip", "list", "--format=json", "--disable-pip-version-check"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                try:
                    packages_data = json.loads(result.stdout)
                    packages = sorted(packages_data, key=lambda x: x.get("name", "").lower())
                    source = "pip_list_json"
                except (json.JSONDecodeError, TypeError, KeyError):
                    logging.warning("Failed to parse pip list JSON - falling back")
                    packages = _get_packages_fallback()
                    source = "importlib_or_pkg_resources"
            else:
                # Fallback 1: pip list (columns)
                try:
                    fallback_result = subprocess.run(
                        [sys.executable, "-m", "pip", "list", "--format=columns", "--disable-pip-version-check"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if fallback_result.returncode == 0:
                        packages = sorted(
                            _parse_columns_output(fallback_result.stdout),
                            key=lambda x: x.get("name", "").lower()
                        )
                        if packages:
                            source = "pip_list_columns"
                except Exception:
                    pass

                # Fallback 2: importlib/pkg_resources
                if not packages:
                    packages = _get_packages_fallback()
                    source = "importlib_or_pkg_resources"
        except (subprocess.TimeoutExpired, Exception) as e:
            logging.warning(f"pip list failed ({type(e).__name__}) - using importlib fallback")
            packages = _get_packages_fallback()
            source = "importlib_or_pkg_resources"
            
        return packages, source
    
    def _find_local_venvs():
        """Find local venv directories in common locations."""
        venvs = []
        venv_names = [".venv", "venv", "env", ".env"]
        
        try:
            # Check project directory
            project_dir = Path(__file__).parent
            for venv_name in venv_names:
                try:
                    venv_path = project_dir / venv_name
                    if venv_path.exists() and (venv_path / "bin" / "python").exists():
                        python_exe = venv_path / "bin" / "python"
                        try:
                            result = subprocess.run(
                                [str(python_exe), "--version"],
                                capture_output=True,
                                text=True,
                                timeout=1
                            )
                            version = result.stdout.strip() or result.stderr.strip()
                            venvs.append({
                                "name": venv_name,
                                "path": str(venv_path),
                                "version": version,
                                "is_current": str(venv_path) == env_path
                            })
                        except (subprocess.TimeoutExpired, Exception):
                            pass
                except Exception:
                    pass
        except Exception:
            pass
        
        return venvs

    def _get_mediainfo_status():
        """Get runtime status for pymediainfo (python) and mediainfo (system)."""
        cli_path = shutil.which("mediainfo")
        pymediainfo_available = False
        pymediainfo_version = None

        try:
            import pymediainfo  # type: ignore
            pymediainfo_available = True
            pymediainfo_version = getattr(pymediainfo, "__version__", None)
        except Exception:
            pymediainfo_available = False

        mediainfo_cli_version = None
        if cli_path:
            try:
                result = subprocess.run(
                    [cli_path, "--version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=2,
                )
                output = result.stdout or ""
                match = re.search(r"v(\d+\.\d+(?:\.\d+)*)", output)
                mediainfo_cli_version = match.group(1) if match else None
            except Exception:
                mediainfo_cli_version = None

        return {
            "pymediainfo_available": pymediainfo_available,
            "pymediainfo_version": pymediainfo_version,
            "mediainfo_cli_available": bool(cli_path),
            "mediainfo_cli_path": cli_path,
            "mediainfo_cli_version": mediainfo_cli_version,
        }

    def _get_runtime_tools_status():
        ffmpeg_path = shutil.which("ffmpeg")
        ffprobe_path = shutil.which("ffprobe")
        vlc_cli_path = shutil.which("vlc")
        mkvinfo_path = shutil.which("mkvinfo")
        mkvmerge_path = shutil.which("mkvmerge")
        mkvinfo_version = None
        mkvmerge_version = None
        python_mkv_available = False
        python_mkv_version = None
        try:
            import pymkv
            python_mkv_available = True
            python_mkv_version = getattr(pymkv, "__version__", None)
        except Exception:
            python_mkv_available = False
        if mkvinfo_path:
            try:
                mkvinfo_result = subprocess.run(
                    [mkvinfo_path, "--version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=2,
                )
                first_line = (mkvinfo_result.stdout or "").splitlines()[0] if mkvinfo_result.stdout else ""
                match = re.search(r"mkvinfo v(\S+)", first_line)
                mkvinfo_version = match.group(1) if match else None
            except Exception:
                mkvinfo_version = None
        if mkvmerge_path:
            try:
                mkvmerge_result = subprocess.run(
                    [mkvmerge_path, "--version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=2,
                )
                first_line = (mkvmerge_result.stdout or "").splitlines()[0] if mkvmerge_result.stdout else ""
                match = re.search(r"mkvmerge v(\S+)", first_line)
                mkvmerge_version = match.group(1) if match else None
            except Exception:
                mkvmerge_version = None

        browser_candidates = [
            ("google-chrome", "google-chrome"),
            ("google-chrome-stable", "google-chrome-stable"),
            ("chromium", "chromium"),
            ("chromium-browser", "chromium-browser"),
            ("firefox", "firefox"),
        ]

        browser_name = None
        browser_path = None
        browser_version = None
        for candidate_name, binary in browser_candidates:
            found = shutil.which(binary)
            if found:
                browser_name = candidate_name
                browser_path = found
                break

        if browser_path:
            try:
                browser_result = subprocess.run(
                    [browser_path, "--version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=2,
                )
                first_line = (browser_result.stdout or "").splitlines()[0] if browser_result.stdout else ""
                match = re.search(r"(\d+\.\d+(?:\.\d+){1,3})", first_line)
                browser_version = match.group(1) if match else None
            except Exception:
                browser_version = None

        mutagen_available = False
        mutagen_version = None
        try:
            import mutagen  # type: ignore
            mutagen_available = True
            mutagen_version = getattr(mutagen, "version_string", None) or getattr(mutagen, "__version__", None)
        except Exception:
            mutagen_available = False

        python_vlc_available = bool(globals().get("HAS_VLC", False))
        python_vlc_version = None
        if python_vlc_available:
            try:
                python_vlc_version = getattr(vlc, "__version__", None)
            except Exception:
                python_vlc_version = None

        ffmpeg_version = None
        if ffmpeg_path:
            try:
                ffmpeg_result = subprocess.run(
                    [ffmpeg_path, "-version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=2,
                )
                first_line = (ffmpeg_result.stdout or "").splitlines()[0] if ffmpeg_result.stdout else ""
                match = re.search(r"ffmpeg version\s+([^\s]+)", first_line, re.IGNORECASE)
                ffmpeg_version = match.group(1) if match else None
            except Exception:
                ffmpeg_version = None

        ffprobe_version = None
        if ffprobe_path:
            try:
                ffprobe_result = subprocess.run(
                    [ffprobe_path, "-version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=2,
                )
                first_line = (ffprobe_result.stdout or "").splitlines()[0] if ffprobe_result.stdout else ""
                match = re.search(r"ffprobe version\s+([^\s]+)", first_line, re.IGNORECASE)
                ffprobe_version = match.group(1) if match else None
            except Exception:
                ffprobe_version = None

        vlc_cli_version = None
        if vlc_cli_path:
            try:
                vlc_result = subprocess.run(
                    [vlc_cli_path, "--version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=2,
                )
                first_line = (vlc_result.stdout or "").splitlines()[0] if vlc_result.stdout else ""
                match = re.search(r"(\d+\.\d+(?:\.\d+){1,3})", first_line)
                vlc_cli_version = match.group(1) if match else None
            except Exception:
                vlc_cli_version = None

        return {
            "ffmpeg_cli_available": bool(ffmpeg_path),
            "ffmpeg_cli_path": ffmpeg_path,
            "ffmpeg_cli_version": ffmpeg_version,
            "ffprobe_cli_available": bool(ffprobe_path),
            "ffprobe_cli_path": ffprobe_path,
            "ffprobe_cli_version": ffprobe_version,
            "mkvinfo_cli_available": bool(mkvinfo_path),
            "mkvinfo_cli_path": mkvinfo_path,
            "mkvinfo_cli_version": mkvinfo_version,
            "mkvmerge_cli_available": bool(mkvmerge_path),
            "mkvmerge_cli_path": mkvmerge_path,
            "mkvmerge_cli_version": mkvmerge_version,
            "python_mkv_available": python_mkv_available,
            "python_mkv_version": python_mkv_version,
            "browser_available": bool(browser_path),
            "browser_name": browser_name,
            "browser_path": browser_path,
            "browser_version": browser_version,
            "vlc_cli_available": bool(vlc_cli_path),
            "vlc_cli_path": vlc_cli_path,
            "vlc_cli_version": vlc_cli_version,
            "python_vlc_available": python_vlc_available,
            "python_vlc_version": python_vlc_version,
            "mutagen_available": mutagen_available,
            "mutagen_version": mutagen_version,
        }




    # Discovery logic
    # Discover available environments (cached/fast)
    conda_envs = _get_conda_environments()
    system_pythons = _get_system_pythons()
    installed_packages, installed_packages_source = _get_installed_packages()
    if not installed_packages:
        installed_packages = _get_packages_fallback()
        installed_packages_source = "importlib_or_pkg_resources"
    local_venvs = _find_local_venvs()
    mediainfo_status = _get_mediainfo_status()
    tools_status = _get_runtime_tools_status()
    requirements_status = _get_requirements_status()
    
    # ===== Build Response =====
    result = {
        # Current Environment (Primary)
        "python_version": platform.python_version(),
        "python_executable": sys.executable,
        "python_prefix": sys.prefix,
        "python_base_prefix": sys.base_prefix,
        "in_venv": in_venv,
        "venv_path": venv_path or venv_env,
        "in_conda": in_conda,
        "conda_env_name": conda_env_name,
        "conda_prefix": conda_prefix,
        "has_conda_context": bool(conda_env_name or conda_prefix),
        "env_type": env_type,
        "env_path": env_path,
        "env_name": env_name,
        "platform": platform.platform(),
        "platform_system": platform.system(),
        "platform_release": platform.release(),
        
        # Current Environment (Detailed)
        "current_environment": current_env,
        
        # Alternative Environments (Discovery Results)
        "available_conda_environments": conda_envs,
        "available_system_pythons": system_pythons,
        "local_venvs": local_venvs,
        
        # Installed Packages
        "installed_packages": installed_packages,
        "package_count": len(installed_packages),
        "installed_packages_source": installed_packages_source,
        "mediainfo_status": mediainfo_status,
        "tools_status": tools_status,
        "requirements_status": requirements_status,
        
        # Recommendations
        "recommended_environment": {
            "name": "venv_core",
            "type": "venv",
            "python_version": "3.14.2",
            "reason": "Lokale venv empfohlen: stabil, unabhängig von Anaconda"
        }
    }

    # UI Trace Logging - capture what frontend receives
    try:
        trace_log_path = Path(__file__).parent / "logs" / "ui_trace_environment_info.log"
        trace_log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(trace_log_path, "a", encoding="utf-8") as f:
            f.write(f"\n{'='*80}\n")
            f.write(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] get_environment_info() called\n")
            f.write(f"force_refresh: {force_refresh}\n")
            f.write(f"package_count: {len(installed_packages)}\n")
            f.write(f"installed_packages_source: {installed_packages_source}\n")
            f.write(f"requirements_status: {requirements_status}\n")
            f.write(f"first_3_packages: {installed_packages[:3] if installed_packages else 'EMPTY'}\n")
            f.write(f"env_type: {result.get('env_type')}\n")
            f.write(f"python_executable: {result.get('python_executable')}\n")
        
        # Also print to console for immediate visibility
        print(f"\n🔍 UI-TRACE: get_environment_info() → packages={len(installed_packages)}, source={installed_packages_source}, req={requirements_status}")
    except Exception as e:
        print(f"⚠️  UI-TRACE logging failed: {e}")

    _ENV_INFO_CACHE["data"] = result
    _ENV_INFO_CACHE["ts"] = time.time()
    return result


# Konfiguration
# 1. Ort für den automatischen Bibliotheks-Scan
SCAN_MEDIA_DIR = str(Path(__file__).parent / "media")

# 2. Standard-Pfad beim ersten Öffnen des Browsers
BROWSER_DEFAULT_DIR = str(Path.home())
# Redundante Definitionen entfernt, da diese nun aus parsers.format_utils importiert werden.
# (AUDIO_EXTENSIONS, VIDEO_EXTENSIONS etc. werden oben importiert)
IMAGE_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg', '.ico'
}
ARCHIVE_EXTENSIONS = {
    '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'
}


# Debug-Optionen
DEBUG_FLAGS = {
    "system": False,
    "ui": False,
    "lib": False,
    "browser": False,
    "edit": False,
    "options": False,
    "start": False,
    "parser": False,
    "scan": False,
    "player": False,
    "db": False,
    "tests": False,
    "api": False,
    "web": False,
    "i18n": False,
    "websocket": False,
    "performance": False,
    "metadata": False,
    "transcode": False,
    "file_ops": False,
    "network": False
}

def initialize_debug_flags(args=None):
    """
    @brief Initializes debug mode and flags based on CLI arguments.
    """
    if args is None:
        args = sys.argv
    
    debug_mode = "--debug" in args
    logger.setup_logging(debug_mode)
    
    if debug_mode:
        for key in DEBUG_FLAGS:
            DEBUG_FLAGS[key] = True
        logger.set_debug_flags(DEBUG_FLAGS)
        logging.info("[System] Full Debug-Mode activated (--debug). All flags set to True.")
    else:
        logger.set_debug_flags(DEBUG_FLAGS)

# Initialize logging early with default sys.argv
initialize_debug_flags()


def is_no_gui_mode(args: list[str] | None = None) -> bool:
    """
    Check whether no-GUI mode is enabled.

    No-GUI mode disables UI/websocket/browser startup and runs
    the app in a connectionless local-only mode.
    """
    if args is None:
        args = sys.argv
    return "--ng" in args or "--no-gui" in args or "--sessionless" in args


def is_connectionless_browser_mode(args: list[str] | None = None) -> bool:
    """
    Check whether browser-based connectionless mode is enabled.

    In this mode the app opens the frontend in browser without starting
    Eel/WebSocket backend session.
    """
    if args is None:
        args = sys.argv
    return "--n" in args


def get_preferred_browser():
    """
    Get the preferred browser controller for launching the application.

    Preference order:
    1. Chromium
    2. Firefox
    3. Google Chrome
    4. Default system browser

    Returns:
        webbrowser.BaseBrowser: Browser controller instance
    """
    import webbrowser
    import shutil

    browser_candidates = [
        ('chromium-browser', 'Chromium'),
        ('chromium', 'Chromium'),
        ('firefox', 'Firefox'),
        ('google-chrome', 'Google Chrome'),
        ('chrome', 'Google Chrome'),
    ]

    for browser_cmd, browser_name in browser_candidates:
        browser_path = shutil.which(browser_cmd)
        if browser_path:
            logging.info(f"[Browser] Selected: {browser_name} ({browser_path})")
            try:
                return webbrowser.get(f'{browser_path} %s')
            except Exception as e:
                logging.warning(f"[Browser] Failed to register {browser_name}: {e}")
                continue

    logging.warning("[Browser] Using system default browser (Vivaldi or other)")
    return webbrowser


def open_session_url(url: str) -> bool:
    """Open a session URL in app-mode window when possible, else fallback browser."""
    import shutil

    browser_candidates = [
        'chromium-browser',
        'chromium',
    ]

    for browser_cmd in browser_candidates:
        browser_path = shutil.which(browser_cmd)
        if browser_path:
            logging.info(f"[Browser] Launching {browser_cmd} in app mode")
            try:
                subprocess.Popen([
                    browser_path,
                    f'--app={url}',
                    '--new-window',
                    '--no-first-run',
                    '--no-default-browser-check',
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
                )
                return True
            except Exception as e:
                logging.warning(f"[Browser] Failed to launch {browser_cmd}: {e}")

    logging.warning("[Browser] Chromium not found, falling back to preferred browser")
    try:
        browser = get_preferred_browser()
        browser.open(url)
        return True
    except Exception as e:
        logging.warning(f"[Browser] Fallback browser launch failed: {e}")
        return False


def run_sessionless_mode() -> dict:
    """
    Execute sessionless startup flow and return status information.
    """
    db.init_db()
    stats = db.get_db_stats()
    legacy_dbs = db.list_legacy_databases()
    return {
        "mode": "no-gui",
        "active_db": str(db.get_active_db_path()),
        "total_items": int(stats.get("total_items", 0)),
        "legacy_db_count": len(legacy_dbs),
        "scan_dirs": PARSER_CONFIG.get("scan_dirs", []),
    }


def run_connectionless_browser_mode() -> dict:
    """
    Execute connectionless browser mode and return status information.

    Opens web/app.html directly in browser without starting Eel.
    """
    db.init_db()
    stats = db.get_db_stats()
    app_file = (Path(__file__).parent / "web" / "app.html").resolve()
    app_url = app_file.as_uri()

    if os.environ.get("MWV_DISABLE_BROWSER_OPEN") == "1":
        logging.info("[Mode-N] Browser launch suppressed by MWV_DISABLE_BROWSER_OPEN=1")
    else:
        browser = get_preferred_browser()
        browser.open(app_url)

    return {
        "mode": "connectionless-browser",
        "active_db": str(db.get_active_db_path()),
        "total_items": int(stats.get("total_items", 0)),
        "app_url": app_url,
        "scan_dirs": PARSER_CONFIG.get("scan_dirs", []),
    }


def check_running_sessions() -> list[dict]:
    """
    Check for currently running dict sessions.
    
    Returns:
        list[dict]: List of active sessions with pid, port, and command info
    """
    import psutil

    sessions = []
    current_pid = os.getpid()
    pid_to_port: dict[int, int] = {}

    try:
        for conn in psutil.net_connections(kind='tcp'):
            if conn.status != 'LISTEN':
                continue
            if not conn.pid or conn.pid == current_pid:
                continue

            laddr = conn.laddr
            host = None
            port = None

            if hasattr(laddr, 'ip') and hasattr(laddr, 'port'):
                host = laddr.ip
                port = laddr.port
            elif isinstance(laddr, tuple) and len(laddr) >= 2:
                host, port = laddr[0], laddr[1]

            if host not in ('127.0.0.1', '::1', '0.0.0.0'):
                continue
            if isinstance(port, int) and conn.pid not in pid_to_port:
                pid_to_port[conn.pid] = port
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        pass

    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            pid = proc.info['pid']
            if pid == current_pid:
                continue

            cmdline = proc.info.get('cmdline') or []
            if not cmdline:
                continue

            if any('main.py' in str(arg) for arg in cmdline):
                sessions.append({
                    'pid': pid,
                    'port': pid_to_port.get(pid),
                    'cmdline': ' '.join(cmdline),
                })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    return sessions


def is_session_url_reachable(url: str, timeout: float = 1.0) -> bool:
    """Check whether an existing session URL responds in time."""
    import urllib.request

    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            return 200 <= int(getattr(response, 'status', 200)) < 500
    except Exception:
        return False


def is_port_in_use(port: int) -> bool:
    """
    Check if a specific port is in use.
    
    Args:
        port: Port number to check
        
    Returns:
        bool: True if port is in use, False otherwise
    """
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(('127.0.0.1', port))
            return False
        except OSError:
            return True


def _ensure_project_venv_active() -> None:
    """Re-exec into local project .venv_core interpreter when available."""
    if os.environ.get("MWV_DISABLE_AUTO_VENV") == "1":
        return
    if os.environ.get("MWV_AUTO_VENV_REEXEC") == "1":
        return

    # PROJECT_ROOT is already defined at top level as Path(__file__).resolve().parent.parent.parent
    venv_python = PROJECT_ROOT / ".venv_core" / "bin" / "python"
    if not (venv_python.is_file() and os.access(venv_python, os.X_OK)):
        return

    try:
        current_exec = Path(sys.executable).resolve()
        target_exec = venv_python.resolve()
    except Exception:
        return

    if current_exec == target_exec:
        return

    logging.info(f"[Startup] Re-exec into project .venv_core interpreter: {target_exec}")
    os.environ["MWV_AUTO_VENV_REEXEC"] = "1"
    os.execv(str(target_exec), [str(target_exec), str(Path(__file__).resolve()), *sys.argv[1:]])


# Defer these calls to if __name__ == '__main__': block

# Log environment information at startup
def _log_environment_info():
    """Log Python environment details at startup."""
    env_type, env_name, env_path, py_ver, py_exec = _detect_python_environment()
    
    logging.info("═" * 60)
    logging.info("[Startup] Application started - Environment Information")
    logging.info("─" * 60)
    
    if env_type == 'conda':
        logging.info(f"  Environment Type: Conda")
        logging.info(f"  Environment Name: {env_name}")
        logging.info(f"  Environment Path: {env_path}")
    elif env_type == 'venv':
        logging.info(f"  Environment Type: Virtual Environment (venv)")
        logging.info(f"  Environment Name: {env_name}")
        logging.info(f"  Environment Path: {env_path}")
    else:
        logging.info(f"  Environment Type: System Python")
        logging.info(f"  Environment Path: {env_path}")
    
    logging.info(f"  Python Version: {py_ver}")
    logging.info(f"  Python Executable: {py_exec}")
    logging.info("═" * 60)

_log_environment_info()


def debug_log(message: str) -> None:
    """
    @brief Universal logging helper (bridged to central logging system).
    """
    logging.info(message)
    # Eel callback if front-end is already listening
    try:
        if hasattr(eel, 'log_to_debug'):
            eel.log_to_debug(message)()
    except Exception:
        pass


if DEBUG_FLAGS["start"]:
    debug_log("[Startup] main.py loading...")

# Removed redundant debug flag processing (now in initialize_debug_flags)


@eel.expose
def get_debug_logs():
    """
    @brief Returns the entire log history as a single string.
    @details Gibt den gesamten bisherigen Log-Verlauf als String zurück.
    @return Multi-line log string / Mehrzeiliger Log-String.
    """
    return "\n".join(logger.get_ui_logs())


@eel.expose
def get_debug_flags():
    """
    @brief Returns the current internal debug flags.
    @details Gibt die aktuell gesetzten internen Debug-Flags zurück.
    @return Dictionary of debug flags / Dictionary der Debug-Flags.
    """
    return DEBUG_FLAGS


@eel.expose
def set_debug_flag(key, value):
    """
    @brief Sets a specific debug flag.
    @details Setzt ein spezifisches Debug-Flag.
    @param key Flag name / Name des Flags.
    @param value Boolean value / Boole'scher Wert.
    """
    if key in DEBUG_FLAGS:
        DEBUG_FLAGS[key] = value
        debug_log(f"[Debug] Flag '{key}' auf {value} gesetzt.")


@eel.expose
def set_all_debug_flags(value):
    """
    @brief Activates or deactivates all debug flags simultaneously.
    @details Aktiviert oder deaktiviert alle Debug-Flags gleichzeitig.
    @param value Boolean value / Boole'scher Wert.
    """
    for key in DEBUG_FLAGS:
        DEBUG_FLAGS[key] = value
    debug_log(f"[Debug] Alle Flags wurden auf {value} gesetzt.")


@eel.expose
def get_language():
    """
    @brief Returns the currently selected UI language.
    @details Gibt die aktuell gewählte Sprache zurück.
    @return Language code (e.g. 'de', 'en') / Sprachcode.
    """
    return PARSER_CONFIG.get("language", "de")


@eel.expose
def set_language(lang):
    """
    @brief Sets the UI language of the application.
    @details Setzt die Sprache der Anwendung.
    @param lang Language code / Sprachcode.
    @return True if successful / True falls erfolgreich.
    """
    PARSER_CONFIG["language"] = lang
    save_parser_config()
    if DEBUG_FLAGS["system"]:
        debug_log(f"[System] Sprache auf '{lang}' gesetzt.")
    return True


# Benutzerdefinierte Module

# Eigene Parser
from src.parsers import tag_writer


# Eigene bottle Web-Routen
from web import app_bottle  # noqa: F401  # Register bottle routes: /media and /cover

# Models


@eel.expose
def get_library():
    """
    @brief Returns all media items from the database without re-scanning.
    @details Gibt alle Medien aus der Datenbank zurück ohne neu zu scannen.
    @return Dict with list of media items / Dokument mit Medien-Liste.
    """
    all_media = db.get_all_media()
    displayed_cats = PARSER_CONFIG.get("displayed_categories")
    # If explicitly None, default to everything (Legacy behavior or first run)
    # If empty list [], it means the user unchecked EVERYTHING (Respect that)
    if displayed_cats is None:
        displayed_cats = ["audio", "video", "images", "documents", "ebooks", "abbild"]
    
    # We map internal categories to the setting keys
    # logical_type: 'Audio', 'Video', 'Bilder', 'Dokument', 'E-Book', 'Abbild'
    cat_map = {
        "audio": ["Audio", "Album", "Hörbuch", "Klassik", "Compilation", "Single"],
        "video": ["Video", "Film", "Serie"],
        "images": ["Bilder"],
        "documents": ["Dokument"],
        "ebooks": ["E-Book"],
        "abbild": ["Abbild", "ISO/Image", "Disk Image", "PAL DVD", "NTSC DVD", "Blu-ray", 
                   "PAL DVD (Abbild)", "NTSC DVD (Abbild)", "DVD (Abbild)", "Blu-ray (Abbild)", 
                   "Audio-CD (Abbild)", "CD-ROM (Abbild)", "Disk-Abbild", "Film",
                   "Spiel", "Beigabe", "Software"]
    }
    
    allowed_internal_cats = []
    for cat in displayed_cats:
        allowed_internal_cats.extend(cat_map.get(cat, []))
        
    filtered_media = [item for item in all_media if item.get('category') in allowed_internal_cats]
    return {"media": filtered_media}


@eel.expose
def clear_database():
    """
    @brief Deletes all entries from the library database.
    @details Löscht alle Einträge aus der Bibliothek-Datenbank.
    @return Status dictionary / Status-Dictionary.
    """
    if DEBUG_FLAGS["db"]:
        debug_log("[Debug-DB] Tabelle wird geleert...")
    db.clear_media()
    return {"status": "ok", "message": "Datenbank geleert", "media": []}


@eel.expose
def reset_app_data():
    """
    @brief Wipes the database and configuration files (private user data).
    @details Löscht Datenbank und Konfigurationsdateien (Private Daten).
    @return Status dictionary with list of deleted paths / Status-Dictionary.
    """
    import shutil
    from pathlib import Path

    deleted = []

    # Paths to clear:
    # 1. ~/.media-web-viewer (Database)
    db_dir = db.DB_DIR
    # 2. ~/.config/gui_media_web_viewer (Parser Config)
    config_dir = Path.home() / ".config" / "gui_media_web_viewer"  # Programmname im config-Pfad für bessere Übersicht ändern

    for p in [db_dir, config_dir]:
        if p.exists():
            try:
                if p.is_dir():
                    shutil.rmtree(p, ignore_errors=True)
                else:
                    p.unlink()
                deleted.append(str(p))
            except Exception as e:
                debug_log(f"[Error] Reset failed for {p}: {e}")

    # Remove legacy database files from old locations
    legacy_deleted = db.cleanup_legacy_databases()
    for p in legacy_deleted:
        deleted.append(p)

    # Re-initialize to avoid crash on next actions
    db.init_db()
    save_parser_config()  # Create default config
    load_parser_config()  # Sync local PARSER_CONFIG in memory

    if DEBUG_FLAGS["system"]:
        debug_log(f"[System] Reset complete. Deleted: {', '.join(deleted)}")
    return {"status": "ok", "deleted": deleted}


@eel.expose
def update_tags(name, tags_dict):
    """
    @brief Saves customized tags for a media item in the database.
    @details Speichert angepasste Tags für ein Item in der DB.
    @param name Media record name / Datenbank-Name des Eintrags.
    @param tags_dict Dictionary of tags to update / Zu aktualisierende Tags.
    @return Status dictionary / Status-Dictionary.
    """
    if DEBUG_FLAGS["db"] or DEBUG_FLAGS["metadata"]:
        logger.debug("metadata", f"Updating tags for {name}: {tags_dict}")
    db.update_media_tags(name, tags_dict)
    return {"status": "ok"}


@eel.expose
def rename_media(old_name, new_name):
    """
    @brief Renames a media record in the database.
    @details Benennt ein Medium in der DB um.
    @param old_name Current name / Aktueller Name.
    @param new_name Target name / Neuer Name.
    @return Status dictionary / Status-Dictionary.
    """
    if not new_name or new_name.strip() == "":
        return {"status": "error", "message": "Name darf nicht leer sein"}

    logger.debug("file_ops", f"Renaming record: {old_name} -> {new_name}")

    success = db.rename_media(old_name, new_name)
    if success:
        return {"status": "ok"}
    else:
        return {"status": "error", "message": "Name bereits vorhanden oder Fehler"}


@eel.expose
def delete_media(name):
    """
    @brief Deletes a media item from the database.
    @details Löscht ein Medium aus der DB.
    @param name Media record name / Datenbank-Name.
    """
    logger.debug("file_ops", f"Deleting record: {name}")
    return db.delete_media(name)


@eel.expose
def get_db_stats():
    """
    @brief Returns statistical information about the database content.
    @details Gibt Statistiken über den Inhalt der Datenbank zurück.
    @return Stats dictionary / Statistik-Dictionary.
    """
    return db.get_db_stats()


@eel.expose
def get_default_media_dir():
    """
    @brief Returns the default media directory (absolute path).
    @details Gibt den voreingestellten Medienordner (absoluter Pfad) zurück.
    @return Path string / Pfad-String.
    """
    return SCAN_MEDIA_DIR


@eel.expose
def ensure_default_scan_dir():
    """
    @brief Ensures the default media directory is present in scan_dirs.
    @details Stellt sicher, dass der Standard-Medienordner in scan_dirs enthalten ist.
    @return Status dictionary with updated directory list / Status-Dictionary mit aktualisierter Liste.
    """
    default_dir = str(Path(SCAN_MEDIA_DIR).resolve())
    Path(default_dir).mkdir(parents=True, exist_ok=True)

    dirs = cast(list[str], PARSER_CONFIG.get("scan_dirs", []))
    normalized_dirs = [str(Path(d).resolve()) for d in dirs if isinstance(d, str) and d.strip()]

    if default_dir not in normalized_dirs:
        normalized_dirs.insert(0, default_dir)

    PARSER_CONFIG["scan_dirs"] = normalized_dirs
    save_parser_config()

    return {"status": "ok", "dirs": PARSER_CONFIG.get("scan_dirs", [])}

# Funktion, um Medien zu scannen und an die GUI zu senden


@eel.expose
def ping():
    """
    @brief Connectivity check.
    @details Gibt eine Bestätigung zurück, dass das Backend erreichbar ist.
    @return dict with status 'ok' and message 'pong'.
    """
    return {"status": "ok", "message": "pong"}

@eel.expose
def scan_media(dir_path: str | None = None, clear_db: bool = True):
    """
    @brief Scans a directory recursively and indexes audio files.
    @details Scannt rekursiv einen Ordner und indexiert Audiodateien. Optionaler Reset der DB.
    @param dir_path Optional path to scan / Optionaler Pfad zum Scannen.
    @param clear_db If True, clears the database before scanning / Falls True, leert die Datenbank vor dem Scan.
    @return Dictionary with media list and scan stats / Dictionary mit Medien-Liste und Statistiken.
    """
    start_time = time.time()
    logging.info(f"[Scan-Trace] Media Scan started at {time.strftime('%H:%M:%S', time.localtime(start_time))}")

    if hasattr(eel, 'set_db_status'):
        try:
            eel.set_db_status(True)()
        except Exception:
            pass

    # DB optional leeren
    if clear_db:
        db.clear_media()

    # Determine which directories to scan
    scan_roots = []
    if dir_path and dir_path.strip():
        scan_roots.append(Path(dir_path).resolve())
    else:
        # Use all directories from config
        config_dirs = PARSER_CONFIG.get("scan_dirs", [SCAN_MEDIA_DIR])
        for d in config_dirs:
            p = Path(d).resolve()
            if p.exists():
                scan_roots.append(p)
            else:
                debug_log(f"[Scan] Skipping non-existent directory: {d}")

    count: int = 0
    try:
        from src.parsers.format_utils import IMAGE_EXTENSIONS, DOCUMENT_EXTENSIONS, EBOOK_EXTENSIONS
        
        # Build all_exts based on configured categories
        indexed_cats = PARSER_CONFIG.get("indexed_categories")
        if not indexed_cats:
            indexed_cats = ["audio", "video", "images", "documents", "ebooks", "abbild"]
        
        all_exts = set()
        
        if "audio" in indexed_cats:
            all_exts |= AUDIO_EXTENSIONS
        if "video" in indexed_cats:
            all_exts |= VIDEO_EXTENSIONS
        if "images" in indexed_cats:
            all_exts |= IMAGE_EXTENSIONS
        if "documents" in indexed_cats:
            all_exts |= DOCUMENT_EXTENSIONS
        if "ebooks" in indexed_cats:
            all_exts |= EBOOK_EXTENSIONS
        if "abbild" in indexed_cats:
            from src.parsers.format_utils import DISK_IMAGE_EXTENSIONS
            all_exts |= DISK_IMAGE_EXTENSIONS
        
        for scan_root in scan_roots:
            logger.debug("scan", f"Starting scan of: {scan_root}")

            # Collect items to avoid sub-file duplicates
            skip_subpaths: set[Path] = set()

            # First pass: Identify "Media Folders" (DVD/BD/ISO-Folders)
            for d in scan_root.rglob('*'):
                if d.is_dir():
                    is_media_folder = (d / 'VIDEO_TS').exists() or (d / 'BDMV').exists()
                    if not is_media_folder:
                        # Check if it contains an ISO
                        if any(d.glob('*.iso')):
                            is_media_folder = True

                    if is_media_folder:
                        logger.debug("scan", f"Erkennte Medien-Ordner: {d.name}")
                        try:
                            item = MediaItem(d.name, d)
                            item_dict = item.to_dict()
                            db.insert_media(item_dict)
                            count += 1
                            skip_subpaths.add(d)
                        except Exception as e:
                            logger.debug("scan", f"Fehler bei Ordner {d.name}: {e}")

            # Second pass: Files
            for f in scan_root.rglob('*'):
                if f.is_file():
                    # Skip if parent is already a recognized media folder
                    should_skip = False
                    for p in skip_subpaths:
                        if f.is_relative_to(p):
                            should_skip = True
                            break
                    if should_skip:
                        continue

                    ext = f.suffix.lower()
                    if ext in all_exts:
                        # Überspringe den Transcoding-Cache
                        if '.cache' in f.parts:
                            continue

                        # Blacklist
                        name_lower = f.name.lower()
                        if any(x in name_lower for x in ['cover art', 'captcha', 'thumb', 'folder', 'albumart', 'al_cave']):
                            continue

                        logger.debug("scan", f"Verarbeite: {f.name}")
                        try:
                            item = MediaItem(f.name, f)
                            item_dict = item.to_dict()
                            db.insert_media(item_dict)
                            count += 1
                        except Exception as e:
                            logger.debug("scan", f"Fehler bei {f.name}: {e}")
                            continue

        elapsed = time.time() - start_time
        scanned_target = ", ".join(str(p) for p in scan_roots) if scan_roots else "none"
        logging.info(f"[Scan-Trace] Scan of {scanned_target} took {elapsed:.2f} seconds.")
        logging.info(f"[Scan-Trace] Scan complete. Processed {count} items in {elapsed:.2f} seconds.")

        # Liefere gescannten Stand direkt aus der DB zurück
        return {
            "media": db.get_all_media(),
            "stats": {"count": count, "time_seconds": elapsed}
        }
    finally:
        if hasattr(eel, 'set_db_status'):
            try:
                eel.set_db_status(False)()
            except Exception:
                pass


@eel.expose
def get_parser_config():
    """
    @brief Returns the current parser configuration to the frontend.
    @details Gibt die aktuelle Parser-Konfiguration an das Frontend zurück.
    @return Configuration dictionary / Konfigurations-Dictionary.
    """
    return PARSER_CONFIG


@eel.expose
def get_parser_mapping():
    """
    @brief Returns the parser-to-filetype mapping.
    @return Mapping dictionary / Mapping-Dictionary.
    """
    from src.parsers.media_parser import PARSER_MAPPING
    return PARSER_MAPPING

@eel.expose
def get_slow_parsers():
    """
    @brief Returns the list of parsers considered slow.
    @return List of parser IDs.
    """
    from src.parsers.format_utils import SLOW_PARSERS
    return list(SLOW_PARSERS)


@eel.expose
def update_parser_config(new_config):
    """
    @brief Updates the parser configuration and saves it to disk.
    @details Aktualisiert die Konfiguration und speichert sie auf Festplatte.
    @param new_config Dictionary with updated settings / Dictionary mit neuen Einstellungen.
    @return Status dictionary / Status-Dictionary.
    """
    PARSER_CONFIG.update(new_config)
    save_parser_config()
    return {"status": "ok"}


@eel.expose
def add_scan_dir():
    """
    @brief Opens a dialog to select a new directory for library scanning.
    @details Öffnet einen Dialog zur Auswahl eines neuen Scan-Verzeichnisses.
    @return Status dictionary with updated directory list / Status-Dictionary mit aktualisierter Liste.
    """
    new_dir = pick_folder()
    if new_dir:
        dirs = cast(list[str], PARSER_CONFIG.get("scan_dirs", []))
        if new_dir not in dirs:
            dirs.append(new_dir)
            PARSER_CONFIG["scan_dirs"] = dirs
            save_parser_config()
            return {"status": "ok", "dirs": dirs}
    return {"status": "cancel"}


@eel.expose
def remove_scan_dir(dir_path):
    """
    @brief Removes a directory from the scan list in the configuration.
    @details Entfernt ein Verzeichnis aus der Scan-Liste in der Konfiguration.
    @param dir_path Path to remove / Zu entfernender Pfad.
    @return Status dictionary / Status-Dictionary.
    """
    dirs = cast(list[str], PARSER_CONFIG.get("scan_dirs", []))
    if dir_path in dirs:
        dirs.remove(dir_path)
        PARSER_CONFIG["scan_dirs"] = dirs
        save_parser_config()
        return {"status": "ok", "dirs": dirs}
    return {"status": "error", "message": "Pfad nicht in Liste"}


@eel.expose
def play_media(path):
    """
    @brief Triggers media playback (handled client-side by the browser).
    @details Triggert die Medienwiedergabe (wird clientseitig vom Browser gehandhabt).
    @param path Media URL or path / Medien-URL oder Pfad.
    @return Confirmation dictionary / Bestätigungs-Dictionary.
    """
    if DEBUG_FLAGS["player"]:
        debug_log(f"[Debug-Player] Spiele ab: {path}")

    # Try to update browser Media Session via Eel (best-effort)
    try:
        # Prepare minimal metadata
        p = Path(path)
        title = p.stem if p.name else str(path)
        meta = {"title": title, "artist": "", "album": "", "artwork": [{"src": document.get('footer-cover') if False else ""}]}
        # Eel call (if frontend exposes `set_media_session`)
        try:
            eel.set_media_session({"title": title})()
        except Exception:
            # If Eel or JS function not available, ignore silently
            pass
    except Exception:
        pass

    return {"status": "play", "path": path}  # Bestätigung


# Playlist state (in-memory)
CURRENT_PLAYLIST: list[dict] = []
CURRENT_INDEX: int = -1


@eel.expose
def set_current_playlist(items: list, start_index: int = 0, replace: bool = True):
    """Set the active playlist. `items` is a list of media dicts or names.
    If replace is False, append to existing playlist. start_index selects initial item.
    """
    global CURRENT_PLAYLIST, CURRENT_INDEX
    # Normalize items: if list of names, convert to minimal dicts
    normalized = []
    for it in items:
        if isinstance(it, str):
            normalized.append({"name": it})
        elif isinstance(it, dict):
            normalized.append(it)
    if replace:
        CURRENT_PLAYLIST = normalized
    else:
        CURRENT_PLAYLIST.extend(normalized)

    if not CURRENT_PLAYLIST:
        CURRENT_INDEX = -1
    else:
        CURRENT_INDEX = max(0, min(len(CURRENT_PLAYLIST) - 1, int(start_index or 0)))

    return {"status": "ok", "count": len(CURRENT_PLAYLIST), "index": CURRENT_INDEX}


@eel.expose
def get_current_playlist():
    global CURRENT_PLAYLIST, CURRENT_INDEX
    return {"items": CURRENT_PLAYLIST, "index": CURRENT_INDEX}


# expose get_current_playlist to eel so frontend can refresh after reorder actions
@eel.expose
def get_current_playlist_exposed():
    return get_current_playlist()


def _play_index(idx: int):
    """Internal: play item at index if valid. Returns status dict."""
    global CURRENT_PLAYLIST, CURRENT_INDEX
    if not CURRENT_PLAYLIST:
        return {"status": "error", "message": "no playlist"}
    if idx < 0 or idx >= len(CURRENT_PLAYLIST):
        return {"status": "error", "message": "index out of range"}
    CURRENT_INDEX = idx
    item = CURRENT_PLAYLIST[CURRENT_INDEX]
    path = item.get("path") or item.get("name")
    # If path is a DB name, resolve to path via DB lookup
    try:
        if path and not Path(path).exists():
            # Attempt to find in DB by name
            all_media = db.get_all_media()
            match = next((m for m in all_media if m.get("name") == path), None)
            if match:
                path = match.get("path") or path
    except Exception:
        pass

    # Call existing play_media to trigger frontend actions
    return play_media(path)


@eel.expose
def next_in_playlist():
    global CURRENT_INDEX, CURRENT_PLAYLIST
    if not CURRENT_PLAYLIST:
        return {"status": "error", "message": "no playlist"}
    next_idx = CURRENT_INDEX + 1 if CURRENT_INDEX + 1 < len(CURRENT_PLAYLIST) else -1
    if next_idx == -1:
        return {"status": "end"}
    return _play_index(next_idx)


@eel.expose
def prev_in_playlist():
    global CURRENT_INDEX
    if not CURRENT_PLAYLIST:
        return {"status": "error", "message": "no playlist"}
    prev_idx = CURRENT_INDEX - 1 if CURRENT_INDEX - 1 >= 0 else -1
    if prev_idx == -1:
        return {"status": "start"}
    return _play_index(prev_idx)


@eel.expose
def jump_to_index(index: int):
    try:
        idx = int(index)
    except Exception:
        return {"status": "error", "message": "invalid index"}
    return _play_index(idx)


@eel.expose
def move_item_up(index: int):
    """
    Move playlist item at `index` one position up (towards start).
    Adjusts `CURRENT_INDEX` if necessary. Returns status and updated playlist.
    """
    global CURRENT_PLAYLIST, CURRENT_INDEX
    try:
        idx = int(index)
    except Exception:
        return {"status": "error", "message": "invalid index"}

    if not CURRENT_PLAYLIST:
        return {"status": "error", "message": "no playlist"}
    if idx <= 0 or idx >= len(CURRENT_PLAYLIST):
        return {"status": "error", "message": "index out of range"}

    # swap
    CURRENT_PLAYLIST[idx - 1], CURRENT_PLAYLIST[idx] = CURRENT_PLAYLIST[idx], CURRENT_PLAYLIST[idx - 1]

    # adjust current index if it was involved
    if CURRENT_INDEX == idx:
        CURRENT_INDEX = idx - 1
    elif CURRENT_INDEX == idx - 1:
        CURRENT_INDEX = idx

    return {"status": "ok", "items": CURRENT_PLAYLIST, "index": CURRENT_INDEX}


@eel.expose
def move_item_down(index: int):
    """
    Move playlist item at `index` one position down (towards end).
    Adjusts `CURRENT_INDEX` if necessary. Returns status and updated playlist.
    """
    global CURRENT_PLAYLIST, CURRENT_INDEX
    try:
        idx = int(index)
    except Exception:
        return {"status": "error", "message": "invalid index"}

    if not CURRENT_PLAYLIST:
        return {"status": "error", "message": "no playlist"}
    if idx < 0 or idx >= len(CURRENT_PLAYLIST) - 1:
        return {"status": "error", "message": "index out of range"}

    # swap
    CURRENT_PLAYLIST[idx], CURRENT_PLAYLIST[idx + 1] = CURRENT_PLAYLIST[idx + 1], CURRENT_PLAYLIST[idx]

    # adjust current index if it was involved
    if CURRENT_INDEX == idx:
        CURRENT_INDEX = idx + 1
    elif CURRENT_INDEX == idx + 1:
        CURRENT_INDEX = idx

    return {"status": "ok", "items": CURRENT_PLAYLIST, "index": CURRENT_INDEX}


@eel.expose
def move_item_up_by_key(key: str):
    """Move the first playlist item matching `key` (name or path) up by one.
    Returns the same structure as `move_item_up`.
    """
    global CURRENT_PLAYLIST
    if not CURRENT_PLAYLIST:
        return {"status": "error", "message": "no playlist"}
    if not key:
        return {"status": "error", "message": "invalid key"}
    # find index by multiple candidate fields and fallbacks
    def matches(it, key):
        if not isinstance(it, dict):
            return False
        # exact fields
        for f in ('name', 'filename', 'path', 'id'):
            v = it.get(f)
            if v and v == key:
                return True
        # tags.title
        tags = it.get('tags') or {}
        if tags.get('title') and tags.get('title') == key:
            return True
        # substring matches for path or name
        for f in ('name', 'filename', 'path'):
            v = it.get(f)
            if v and isinstance(v, str) and key in v:
                return True
        return False

    for idx, it in enumerate(CURRENT_PLAYLIST):
        if matches(it, key):
            print(f"[DEBUG] move_item_up_by_key: matched idx={idx} key={key} item={it}")
            return move_item_up(idx)

    # last resort: try matching by stringified dict values
    for idx, it in enumerate(CURRENT_PLAYLIST):
        try:
            s = ' '.join(str(x) for x in it.values())
            if key in s:
                return move_item_up(idx)
        except Exception:
            continue

    print(f"[DEBUG] move_item_up_by_key: no match for key={key}")
    return {"status": "error", "message": "item not found"}


@eel.expose
def move_item_down_by_key(key: str):
    """Move the first playlist item matching `key` (name or path) down by one.
    Returns the same structure as `move_item_down`.
    """
    global CURRENT_PLAYLIST
    if not CURRENT_PLAYLIST:
        return {"status": "error", "message": "no playlist"}
    if not key:
        return {"status": "error", "message": "invalid key"}
    def matches(it, key):
        if not isinstance(it, dict):
            return False
        for f in ('name', 'filename', 'path', 'id'):
            v = it.get(f)
            if v and v == key:
                return True
        tags = it.get('tags') or {}
        if tags.get('title') and tags.get('title') == key:
            return True
        for f in ('name', 'filename', 'path'):
            v = it.get(f)
            if v and isinstance(v, str) and key in v:
                return True
        return False

    for idx, it in enumerate(CURRENT_PLAYLIST):
        if matches(it, key):
            print(f"[DEBUG] move_item_down_by_key: matched idx={idx} key={key} item={it}")
            return move_item_down(idx)

    for idx, it in enumerate(CURRENT_PLAYLIST):
        try:
            s = ' '.join(str(x) for x in it.values())
            if key in s:
                return move_item_down(idx)
        except Exception:
            continue

    print(f"[DEBUG] move_item_down_by_key: no match for key={key}")
    return {"status": "error", "message": "item not found"}


@eel.expose
def move_item_up_by_obj(item_obj):
    """Expose: accept a JS object representing the item, extract a key and move up."""
    try:
        # item_obj comes from Eel as a dict
        key = _extract_key_from_obj(item_obj)
        if not key:
            print(f"[DEBUG] move_item_up_by_obj: could not extract key from {item_obj}")
            return {"status": "error", "message": "no key extracted"}
        return move_item_up_by_key(key)
    except Exception as e:
        print(f"[ERROR] move_item_up_by_obj exception: {e}")
        return {"status": "error", "message": str(e)}


@eel.expose
def move_item_down_by_obj(item_obj):
    """Expose: accept a JS object representing the item, extract a key and move down."""
    try:
        key = _extract_key_from_obj(item_obj)
        if not key:
            print(f"[DEBUG] move_item_down_by_obj: could not extract key from {item_obj}")
            return {"status": "error", "message": "no key extracted"}
        return move_item_down_by_key(key)
    except Exception as e:
        print(f"[ERROR] move_item_down_by_obj exception: {e}")
        return {"status": "error", "message": str(e)}


@eel.expose
def remove_playlist_item(index: int):
    """
    Remove playlist item at `index` from CURRENT_PLAYLIST.
    Adjusts CURRENT_INDEX accordingly.
    """
    global CURRENT_PLAYLIST, CURRENT_INDEX
    try:
        idx = int(index)
    except Exception:
        return {"status": "error", "message": "invalid index"}

    if not CURRENT_PLAYLIST:
        return {"status": "error", "message": "no playlist"}
    if idx < 0 or idx >= len(CURRENT_PLAYLIST):
        return {"status": "error", "message": "index out of range"}

    CURRENT_PLAYLIST.pop(idx)

    if CURRENT_INDEX == idx:
        CURRENT_INDEX = -1 
    elif CURRENT_INDEX > idx:
        CURRENT_INDEX -= 1

    return {"status": "ok", "items": CURRENT_PLAYLIST, "index": CURRENT_INDEX}


@eel.expose
def move_current_up():
    """Move the currently selected playlist item up by one position."""
    global CURRENT_INDEX
    if CURRENT_INDEX is None or CURRENT_INDEX < 0:
        return {"status": "error", "message": "no current item"}
    logging.debug(f"[Playlist] move_current_up called. CURRENT_INDEX={CURRENT_INDEX}")
    return move_item_up(CURRENT_INDEX)


@eel.expose
def move_current_down():
    """Move the currently selected playlist item down by one position."""
    global CURRENT_INDEX
    if CURRENT_INDEX is None or CURRENT_INDEX < 0:
        return {"status": "error", "message": "no current item"}
    logging.debug(f"[Playlist] move_current_down called. CURRENT_INDEX={CURRENT_INDEX}")
    return move_item_down(CURRENT_INDEX)


@eel.expose
def move_item_to(old_index: int, new_index: int):
    """
    Move an item from old_index to new_index within CURRENT_PLAYLIST.
    Adjusts CURRENT_INDEX accordingly and returns updated playlist state.
    """
    global CURRENT_PLAYLIST, CURRENT_INDEX
    try:
        o = int(old_index)
        n = int(new_index)
    except Exception:
        return {"status": "error", "message": "invalid index"}
    logging.debug(f"[Playlist] move_item_to called. old={o}, new={n}, CURRENT_INDEX={CURRENT_INDEX}")

    if not CURRENT_PLAYLIST:
        return {"status": "error", "message": "no playlist"}

    length = len(CURRENT_PLAYLIST)
    if o < 0 or o >= length or n < 0:
        return {"status": "error", "message": "index out of range"}

    # clamp new index to [0, length-1] for insertion positions (allow append at length)
    if n > length:
        n = length

    if o == n or (o == n - 1 and o < n):
        # nothing to do (moving to same place)
        return {"status": "ok", "items": CURRENT_PLAYLIST, "index": CURRENT_INDEX}

    try:
        item = CURRENT_PLAYLIST.pop(o)
        # If popping an earlier index shifts target left, insertion at n is still correct
        if n > len(CURRENT_PLAYLIST):
            n = len(CURRENT_PLAYLIST)
        CURRENT_PLAYLIST.insert(n, item)

        # Update CURRENT_INDEX
        if CURRENT_INDEX == o:
            CURRENT_INDEX = n
        else:
            if o < CURRENT_INDEX <= n:
                # item moved forward past current item -> current shifts left
                CURRENT_INDEX -= 1
            elif n <= CURRENT_INDEX < o:
                # item inserted before current -> current shifts right
                CURRENT_INDEX += 1

        return {"status": "ok", "items": CURRENT_PLAYLIST, "index": CURRENT_INDEX}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@eel.expose
def open_in_explorer(path_str):
    """
    @brief Opens a specific file or folder in the system's native file explorer.
    @details Öffnet eine Datei oder einen Ordner im nativen Datei-Explorer des Systems.
    @param path_str Absolute path / Absoluter Pfad.
    @return Status or error dictionary / Status- oder Fehler-Dictionary.
    """
    path_obj = Path(path_str)
    if not path_obj.exists():
        logging.warning("[FileExplorer] Path does not exist / Pfad existiert nicht")
        return {"error": "Nicht gefunden"}

    try:
        # Check OS and open accordingly
        if os.name == 'nt':  # Windows
            # Use getattr to satisfy mypy on non-Windows systems
            startfile = getattr(os, 'startfile', None)
            if startfile:
                startfile(path_str)
        elif sys.platform == 'darwin':  # macOS
            subprocess.run(['open', '-R', path_str])
        else:  # Linux (freedesktop)
            subprocess.run(['xdg-open', str(path_obj.parent)])
        return {"status": "ok"}
    except Exception as e:
        logging.error(f"[FileExplorer] Error opening path / Fehler beim Oeffnen: {e}")
        return {"error": str(e)}


@eel.expose
def browse_dir(dir_path=None):
    """
    @brief Lists folders and audio files for the in-app file browser.
    @details Listet Ordner und Audiodateien eines Verzeichnisses für den Datei-Browser.
    @param dir_path Directory path / Verzeichnispfad.
    @return Dictionary with path info and item list / Dictionary mit Pfad-Infos und Element-Liste.
    """
    if not dir_path:
        dir_path = BROWSER_DEFAULT_DIR

    target = Path(dir_path)
    if not target.exists() or not target.is_dir():
        return {"error": "Ordner nicht gefunden", "path": dir_path}

    items = []
    try:
        for entry in sorted(target.iterdir(), key=lambda e: (not e.is_dir(), e.name.lower())):
            if entry.name.startswith('.'):
                continue
            if entry.is_dir():
                items.append({"name": entry.name, "path": str(entry), "type": "folder"})
            elif entry.suffix.lower() in AUDIO_EXTENSIONS or entry.suffix.lower() in VIDEO_EXTENSIONS:
                size_mb = entry.stat().st_size / (1024 * 1024)
                item_type = "video" if entry.suffix.lower() in VIDEO_EXTENSIONS else "audio"
                items.append({"name": entry.name, "path": str(entry), "type": item_type, "size": f"{size_mb:.1f} MB"})
    except PermissionError:
        return {"error": "Keine Berechtigung", "path": dir_path}

    parent = str(target.parent) if target.parent != target else None
    return {"path": str(target), "parent": parent, "items": items}


@eel.expose
def pick_folder():
    """
    @brief Opens a native OS folder selection dialog using Tkinter.
    @details Öffnet einen nativen Ordner-Auswahldialog mittels Tkinter.
    @return Selected path or None / Gewählter Pfad oder None.
    """
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        folder_path = filedialog.askdirectory()
        root.destroy()
        return folder_path if folder_path else None
    except Exception as e:
        logging.error(f"[System] Folder picker failed: {e}")
        return None


@eel.expose
def add_file_to_library(file_path):
    """
    @brief Adds a single file from the browser to the library.
    @details Fügt eine einzelne Datei aus dem Datei-Browser der Bibliothek hinzu.
    @param file_path Absolute path / Absoluter Pfad.
    @return Status dictionary / Status-Dictionary.
    """
    p = Path(file_path)
    if not p.exists() or not p.is_file():
        return {"error": "Datei nicht gefunden"}
    if p.suffix.lower() not in AUDIO_EXTENSIONS and p.suffix.lower() not in VIDEO_EXTENSIONS:
        return {"error": "Kein unterstütztes Audio- oder Videoformat"}

    known = db.get_known_media_names()
    if p.name in known:
        return {"status": "exists", "name": p.name}

    item = MediaItem(p.name, p)
    item_dict = item.to_dict()
    db.insert_media(item_dict)
    return {"status": "added", "item": item_dict}

# VLC Player Instance (Global)
VLC_INSTANCE = None
VLC_PLAYER = None


@eel.expose
def play_vlc(file_path: str):
    """
    @brief Plays a media file in an external VLC window.
    @details Spielt eine Mediendatei in einem externen VLC-Fenster ab.
    """
    global VLC_INSTANCE, VLC_PLAYER
    if not HAS_VLC:
        return {"error": "python-vlc ist nicht installiert"}

    try:
        if VLC_INSTANCE is None:
            VLC_INSTANCE = vlc.Instance()
        
        if VLC_PLAYER is not None:
            VLC_PLAYER.stop()

        VLC_PLAYER = VLC_INSTANCE.media_player_new()
        media = VLC_INSTANCE.media_new(file_path)
        VLC_PLAYER.set_media(media)
        VLC_PLAYER.play()
        
        logger.get_ui_logger().info(f"VLC: Spiele {file_path}")
        return {"status": "ok"}
    except Exception as e:
        logger.get_ui_logger().error(f"VLC Fehler: {e}")
        return {"error": str(e)}


@eel.expose
def stop_vlc():
    """
    @brief Stops the VLC player.
    """
    global VLC_PLAYER
    if VLC_PLAYER:
        VLC_PLAYER.stop()
    return {"status": "ok"}


@eel.expose
def is_mkvtoolnix_available():
    """Checks if mkvmerge is available in PATH."""
    return shutil.which("mkvmerge") is not None


@eel.expose
def stream_to_vlc(file_path):
    """
    @brief Real-time streaming via mkvmerge pipe to VLC.
    @details Nutzt mkvmerge zum Remuxen und pipet den Output direkt an VLC.
    """
    logging.info(f"Direct Play: {file_path}")
    
    # ISO Handling: Native DVD playback for menus
    if file_path.lower().endswith('.iso'):
        try:
            # For ISOs, we use VLC's native dvd:// support instead of mkvmerge pipe
            # This allows menu interaction and chapter selection.
            vlc_path = shutil.which('vlc') or 'vlc'
            cmd = [vlc_path, f"dvd://{file_path}"]
            subprocess.Popen(cmd)
            return {"status": "ok", "mode": "vlc_dvd"}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    if not is_mkvtoolnix_available():
        return {"status": "error", "error": "mkvtoolnix nicht installiert"}

    try:
        # Command 1: mkvmerge to stdout
        mkvmerge_cmd = ["mkvmerge", file_path, "-o", "-"]
        # Command 2: vlc from stdin
        vlc_cmd = ["vlc", "-"]

        logging.info(f"Direct Play: {' '.join(mkvmerge_cmd)} | {' '.join(vlc_cmd)}")

        # Start pipeline
        p1 = subprocess.Popen(mkvmerge_cmd, stdout=subprocess.PIPE)
        p2 = subprocess.Popen(vlc_cmd, stdin=p1.stdout)
        
        # Allow p1 to receive a SIGPIPE if p2 exits.
        if p1.stdout:
            p1.stdout.close()

        return {"status": "ok", "message": "Streaming gestartet"}
    except Exception as e:
        logging.error(f"Direct Play Fehler: {e}")
        return {"status": "error", "error": str(e)}


@eel.expose
def remux_mkv_batch(folder_path):
    """
    @brief Fast Batch-Remux of all video files in a folder to MKV.
    """
    if not is_mkvtoolnix_available():
        return {"status": "error", "error": "mkvtoolnix nicht installiert"}

    p = Path(folder_path)
    if not p.is_dir():
        return {"status": "error", "error": "Ungültiges Verzeichnis"}

    video_files = []
    for ext in VIDEO_EXTENSIONS:
        if ext == ".mkv": continue # Skip existing MKVs
        video_files.extend(list(p.glob(f"*{ext}")))

    results = {"total": len(video_files), "success": 0, "errors": []}
    
    for vf in video_files:
        output = vf.with_suffix(".mkv")
        if output.exists():
            results["errors"].append(f"{vf.name}: Ziel existiert bereits")
            continue
            
        try:
            cmd = ["mkvmerge", str(vf), "-o", str(output)]
            subprocess.run(cmd, check=True, capture_output=True)
            results["success"] += 1
            logging.info(f"Remux Erfolg: {vf.name} -> {output.name}")
        except Exception as e:
            results["errors"].append(f"{vf.name}: {str(e)}")
            logging.error(f"Remux Fehler {vf.name}: {e}")

    return {"status": "ok", "results": results}


@eel.expose
def import_vlc_playlist(m3u_path: str):
    """
    @brief Imports a VLC playlist (m3u8/m3u/XSPF) into the library.
    @details Importiert eine VLC-Playlist (m3u8/m3u/XSPF) in die Bibliothek.
    @param m3u_path Path to the playlist file / Pfad zur Playlist-Datei.
    @return Dictionary with imported media items / Dictionary mit importierten Items.
    """
    if not HAS_M3U8:
        return {"error": "python-m3u8 Modul ist nicht installiert. Bitte installieren: pip install m3u8"}
    
    try:
        playlist_file = Path(m3u_path)
        if not playlist_file.exists():
            return {"error": "Playlist-Datei nicht gefunden"}
        
        # Load playlist
        playlist = m3u8.load(str(playlist_file))
        
        imported = []
        skipped = []
        errors = []
        
        for segment in playlist.segments:
            if not segment.uri:
                continue
                
            # Convert URI to absolute path if relative
            media_path = Path(segment.uri)
            if not media_path.is_absolute():
                media_path = playlist_file.parent / media_path
            
            if not media_path.exists():
                errors.append(f"Datei nicht gefunden: {media_path.name}")
                continue
            
            # Check if already in library
            known = db.get_known_media_names()
            if media_path.name in known:
                skipped.append(media_path.name)
                continue
            
            # Parse and add to library
            try:
                item = MediaItem(media_path.name, media_path)
                item_dict = item.to_dict()
                db.insert_media(item_dict)
                imported.append(item_dict)
            except Exception as e:
                errors.append(f"{media_path.name}: {str(e)}")
        
        if DEBUG_FLAGS["player"]:
            debug_log(f"[VLC Import] {len(imported)} importiert, {len(skipped)} übersprungen, {len(errors)} Fehler")
        
        return {
            "status": "ok",
            "imported": imported,
            "skipped": skipped,
            "errors": errors,
            "count": len(imported)
        }
    except Exception as e:
        logging.error(f"[VLC Import] Error: {e}")
        return {"error": str(e)}


@eel.expose
def export_playlist_to_vlc(media_names: list, output_path: str):
    """
    @brief Exports selected media items to a VLC-compatible m3u8 playlist.
    @details Exportiert ausgewählte Medien in eine VLC-kompatible m3u8 Playlist.
    @param media_names List of media item names from database / Liste von Medien-Namen aus der DB.
    @param output_path Target path for the .m3u8 file / Ziel-Pfad für die .m3u8-Datei.
    @return Status dictionary / Status-Dictionary.
    """
    try:
        playlist_file = Path(output_path)
        if not playlist_file.suffix:
            playlist_file = playlist_file.with_suffix('.m3u8')
        
        lines = ["#EXTM3U\n"]
        exported = 0
        missing = []
        
        # Get all media and create a lookup dict
        all_media = db.get_all_media()
        media_dict = {item['name']: item for item in all_media}
        
        for name in media_names:
            item_dict = media_dict.get(name)
            if not item_dict:
                missing.append(name)
                continue
            
            file_path = item_dict.get("path", "")
            if not file_path or not Path(file_path).exists():
                missing.append(name)
                continue
            
            # Add EXTINF metadata line (duration, title)
            duration = item_dict.get("duration", 0) or -1
            title = item_dict.get("title") or name
            artist = item_dict.get("artist", "")
            extinf_title = f"{artist} - {title}" if artist else title
            
            lines.append(f"#EXTINF:{duration},{extinf_title}\n")
            lines.append(f"{file_path}\n")
            exported += 1
        
        playlist_file.write_text("".join(lines), encoding='utf-8')
        
        if DEBUG_FLAGS["player"]:
            debug_log(f"[VLC Export] {exported} Tracks nach {playlist_file.name} exportiert")
        
        return {
            "status": "ok",
            "path": str(playlist_file),
            "exported": exported,
            "missing": missing
        }
    except Exception as e:
        logging.error(f"[VLC Export] Error: {e}")
        return {"error": str(e)}


@eel.expose
def save_playlist(media_names: list, output_path: str):
    """
    @brief Saves the current selection of media names to a JSON file.
    """
    try:
        path = Path(output_path)
        if not path.suffix:
            path = path.with_suffix('.json')
        
        import json
        path.write_text(json.dumps(media_names, indent=4), encoding='utf-8')
        return {"status": "ok", "path": str(path)}
    except Exception as e:
        logging.error(f"[Save Playlist] Error: {e}")
        return {"error": str(e)}

@eel.expose
def load_playlist(input_path: str):
    """
    @brief Loads a list of media names from a JSON file and returns full media objects.
    """
    try:
        path = Path(input_path)
        if not path.exists():
            return {"error": "Playlist file not found"}
        
        import json
        media_names = json.loads(path.read_text(encoding='utf-8'))
        
        all_media = db.get_all_media()
        media_dict = {item['name']: item for item in all_media}
        
        items = []
        for name in media_names:
            if name in media_dict:
                items.append(media_dict[name])
        
        return {"status": "ok", "items": items}
    except Exception as e:
        logging.error(f"[Load Playlist] Error: {e}")
        return {"error": str(e)}

@eel.expose
def pick_file(title="Datei auswählen", filetypes=None):
    """
    @brief Opens a native file picker dialog.
    @details Öffnet einen nativen Datei-Auswahldialog.
    @param title Dialog title / Dialog-Titel.
    @param filetypes List of (description, extension) tuples / Liste von Dateifiltern.
    @return Selected file path or None / Gewählter Pfad oder None.
    """
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        
        if filetypes:
            file_path = filedialog.askopenfilename(title=title, filetypes=filetypes)
        else:
            file_path = filedialog.askopenfilename(title=title)
        
        root.destroy()
        return file_path if file_path else None
    except Exception as e:
        logging.error(f"[System] File picker failed: {e}")
        return None


@eel.expose
def pick_save_file(title="Datei speichern", filetypes=None, default_name="playlist.m3u8"):
    """
    @brief Opens a native file save dialog.
    @details Öffnet einen nativen Datei-Speichern-Dialog.
    @param title Dialog title / Dialog-Titel.
    @param filetypes List of (description, extension) tuples / Liste von Dateifiltern.
    @param default_name Default filename / Standard-Dateiname.
    @return Selected file path or None / Gewählter Pfad oder None.
    """
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        
        if filetypes:
            file_path = filedialog.asksaveasfilename(
                title=title, 
                filetypes=filetypes,
                defaultextension=".m3u8",
                initialfile=default_name
            )
        else:
            file_path = filedialog.asksaveasfilename(
                title=title,
                initialfile=default_name
            )
        
        root.destroy()
        return file_path if file_path else None
    except Exception as e:
        logging.error(f"[System] File save picker failed: {e}")
        return None


@eel.expose
def pick_folder_cli(prompt="Ordnerpfad eingeben"):
    """
    @brief CLI-based folder picker without GUI dependencies.
    @details CLI-basierter Ordner-Picker ohne GUI-Abhängigkeiten (nur Bordmittel).
    @param prompt Input prompt text / Eingabe-Prompt-Text.
    @return Valid folder path or None / Gültiger Ordnerpfad oder None.
    """
    try:
        print(f"\n{prompt}:")
        print(f"(Standard: {Path.home()})")
        user_input = input("> ").strip()
        
        if not user_input:
            return str(Path.home())
        
        folder_path = Path(user_input).expanduser().resolve()
        
        if folder_path.exists() and folder_path.is_dir():
            return str(folder_path)
        else:
            print(f"Fehler: '{folder_path}' ist kein gültiger Ordner.")
            return None
    except (KeyboardInterrupt, EOFError):
        print("\nAbgebrochen.")
        return None
    except Exception as e:
        logging.error(f"[System] CLI folder picker failed: {e}")
        return None


@eel.expose
def pick_file_cli(prompt="Dateipfad eingeben", extensions=None):
    """
    @brief CLI-based file picker without GUI dependencies.
    @details CLI-basierter Datei-Picker ohne GUI-Abhängigkeiten (nur Bordmittel).
    @param prompt Input prompt text / Eingabe-Prompt-Text.
    @param extensions Optional list of allowed extensions / Optionale Liste erlaubter Endungen.
    @return Valid file path or None / Gültiger Dateipfad oder None.
    """
    try:
        ext_info = ""
        if extensions:
            ext_info = f" (Erlaubte Formate: {', '.join(extensions)})"
        
        print(f"\n{prompt}{ext_info}:")
        user_input = input("> ").strip()
        
        if not user_input:
            return None
        
        file_path = Path(user_input).expanduser().resolve()
        
        if not file_path.exists():
            print(f"Fehler: Datei '{file_path}' nicht gefunden.")
            return None
        
        if not file_path.is_file():
            print(f"Fehler: '{file_path}' ist keine Datei.")
            return None
        
        if extensions and file_path.suffix.lower() not in extensions:
            print(f"Fehler: Dateiformat '{file_path.suffix}' nicht erlaubt.")
            return None
        
        return str(file_path)
    except (KeyboardInterrupt, EOFError):
        print("\nAbgebrochen.")
        return None
    except Exception as e:
        logging.error(f"[System] CLI file picker failed: {e}")
        return None


@eel.expose
def pick_save_file_cli(prompt="Speicherpfad eingeben", default_name="output.txt", extensions=None):
    """
    @brief CLI-based save file dialog without GUI dependencies.
    @details CLI-basierter Speichern-Dialog ohne GUI-Abhängigkeiten (nur Bordmittel).
    @param prompt Input prompt text / Eingabe-Prompt-Text.
    @param default_name Default filename / Standard-Dateiname.
    @param extensions Optional list of allowed extensions / Optionale Liste erlaubter Endungen.
    @return Valid save path or None / Gültiger Speicherpfad oder None.
    """
    try:
        ext_info = ""
        if extensions:
            ext_info = f" (Formate: {', '.join(extensions)})"
        
        print(f"\n{prompt}{ext_info}:")
        print(f"(Standard: {default_name})")
        user_input = input("> ").strip()
        
        if not user_input:
            user_input = default_name
        
        save_path = Path(user_input).expanduser().resolve()
        
        # Add extension if missing
        if extensions and save_path.suffix.lower() not in extensions:
            save_path = save_path.with_suffix(extensions[0])
        
        # Check if parent directory exists
        if not save_path.parent.exists():
            print(f"Fehler: Verzeichnis '{save_path.parent}' existiert nicht.")
            create = input("Verzeichnis erstellen? (j/n): ").strip().lower()
            if create == 'j':
                save_path.parent.mkdir(parents=True, exist_ok=True)
            else:
                return None
        
        # Warn if file exists
        if save_path.exists():
            overwrite = input(f"Datei '{save_path.name}' existiert. Überschreiben? (j/n): ").strip().lower()
            if overwrite != 'j':
                return None
        
        return str(save_path)
    except (KeyboardInterrupt, EOFError):
        print("\nAbgebrochen.")
        return None
    except Exception as e:
        logging.error(f"[System] CLI save file picker failed: {e}")
        return None


@eel.expose
def get_test_suites():
    """
    @brief Discovers all test files in the tests/ directory and extracts metadata.
    @details Findet alle Testdateien im Verzeichnis tests/ und extrahiert deren Metadaten.
    @return List of test suite objects / Liste von Test-Suite-Objekten.
    """
    test_dir = Path(__file__).parents[2] / "tests"
    if not test_dir.exists():
        return []

    suites = []
    for f in sorted(test_dir.rglob("*.py")):
        if f.name.startswith("__"):
            continue
        # Include all .py files in tests/ as they might be utility scripts the user wants
        try:
            content = f.read_text(encoding='utf-8')
        except Exception:
            content = ""

        metadata = {
            "category": "-",
            "inputs": "-",
            "outputs": "-",
            "files": "-",
            "comment": "-"
        }

        for line in content.splitlines():
            if line.startswith("# Kategorie:"):
                metadata["category"] = line.split(":", 1)[1].strip()
            elif line.startswith("# Eingabewerte:"):
                metadata["inputs"] = line.split(":", 1)[1].strip()
            elif line.startswith("# Ausgabewerte:"):
                metadata["outputs"] = line.split(":", 1)[1].strip()
            elif line.startswith("# Testdateien:"):
                metadata["files"] = line.split(":", 1)[1].strip()
            elif line.startswith("# Kommentar:"):
                metadata["comment"] = line.split(":", 1)[1].strip()

        display_name = f.stem.replace("test_", "").replace("benchmark_", "Benchmark: ").replace("_", " ").title()
        suites.append({
            "id": str(f.relative_to(test_dir)),
            "name": display_name,
            "path": str(f),
            "metadata": metadata
        })
    return suites


@eel.expose
def update_test_metadata(filename, metadata):
    """
    @brief Updates the metadata comments in a specific test file.
    @details Aktualisiert die Metadaten-Kommentare in einer bestimmten Testdatei.
    @param filename Name of the test file / Name der Testdatei.
    @param metadata Dictionary of metadata fields / Dictionary der Metadaten-Felder.
    @return Status or error dictionary / Status- oder Fehler-Dictionary.
    """
    test_dir = Path(__file__).parents[2] / "tests"
    file_path = test_dir / filename

    if not file_path.exists():
        return {"error": "Test-Datei nicht gefunden"}

    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.splitlines()

        # Remove existing metadata lines
        new_lines = []
        for line in lines:
            if not any(line.startswith(prefix) for prefix in [
                "# Kategorie:", "# Eingabewerte:", "# Ausgabewerte:", "# Testdateien:", "# Kommentar:"
            ]):
                new_lines.append(line)

        # Prepend new metadata
        header = [
            f"# Kategorie: {metadata.get('category', '-')}",
            f"# Eingabewerte: {metadata.get('inputs', '-')}",
            f"# Ausgabewerte: {metadata.get('outputs', '-')}",
            f"# Testdateien: {metadata.get('files', '-')}",
            f"# Kommentar: {metadata.get('comment', '-')}",
            ""  # Add empty line after metadata
        ]

        # Join lines with proper newline handling
        # Skip leading empty lines if there are any after removing metadata
        while new_lines and not new_lines[0].strip():
            new_lines.pop(0)

        final_content = "\n".join(header + new_lines)
        file_path.write_text(final_content, encoding='utf-8')
        return {"status": "ok"}
    except Exception as e:
        return {"error": str(e)}


@eel.expose
def create_new_test(name):
    """
    @brief Creates a new test file based on a template.
    @details Erstellt eine neue Testdatei basierend auf einem Template.
    @param name Base name for the test / Basisname des Tests.
    @return Status or filename dictionary / Status- oder Dateinamen-Dictionary.
    """
    test_dir = Path(__file__).parents[2] / "tests"
    test_dir.mkdir(parents=True, exist_ok=True)

    # Sanitize name
    safe_name = "".join([c for c in name if c.isalnum() or c in (' ', '_', '-')]).strip().replace(' ', '_')
    if not safe_name.startswith('test_'):
        safe_name = f"test_{safe_name}"

    filename = f"{safe_name}.py"
    file_path = test_dir / filename

    if file_path.exists():
        return {"status": "error", "message": "Test existiert bereits"}

    template = f"""# Kategorie: -
# Eingabewerte: -
# Ausgabewerte: -
# Testdateien: -
# Kommentar: Neuer Test

import pytest


def {safe_name}():
    # Hier Test-Code schreiben
    assert True
"""
    try:
        file_path.write_text(template, encoding='utf-8')
        return {"status": "ok", "filename": filename}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@eel.expose
def delete_test(filename):
    """
    @brief Deletes a specific test file from the disk.
    @details Löscht eine bestimmte Testdatei von der Festplatte.
    @param filename Test file name / Name der Testdatei.
    @return Status or error dictionary / Status- oder Fehler-Dictionary.
    """
    test_dir = Path(__file__).parents[2] / "tests"
    file_path = test_dir / filename

    if not file_path.exists():
        return {"error": "Datei nicht gefunden"}

    try:
        file_path.unlink()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@eel.expose
def get_logbook_entry(feature_name, source="logbuch"):
    """
    @brief Reads a markdown file from the logbook or the README.
    @details Liest eine Markdown-Datei aus dem Logbuch oder die README ein.
    @param feature_name Entry name or 'README' / Name des Eintrags oder 'README'.
    @return Content string (Markdown) / Inhalts-String (Markdown).
    """
    root_dir = PROJECT_ROOT
    if source == "root":
        allowed_root_files = {
            "README.md",
            "DOCUMENTATION.md",
            "INSTALL.md",
            "DEPENDENCIES.md",
            "LICENSE.md",
        }
        requested = feature_name if feature_name.endswith(".md") else f"{feature_name}.md"
        if requested not in allowed_root_files:
            return f"<h1>Error</h1><p>Root entry '{feature_name}' not allowed.</p>"
        log_file = root_dir / requested
    elif feature_name.upper() == "README" or feature_name.upper() == "README.MD":
        log_file = root_dir / "README.md"
    else:
        log_dir = PROJECT_ROOT / "docs" / "logbuch"
        log_file = log_dir / f"{feature_name}.md"
        if not log_file.exists():
            # Fallback without extension just in case it was passed directly
            log_file = log_dir / feature_name

    if not log_file.exists():
        return f"<h1>Error</h1><p>Logbook entry for '{feature_name}' not found.</p>"

    try:
        content = log_file.read_text(encoding='utf-8')
        
        # Bilingual splitting: <!-- lang-split -->
        if "<!-- lang-split -->" in content:
            parts = content.split("<!-- lang-split -->")
            if len(parts) >= 2:
                current_lang = get_language()
                if current_lang.lower() == "en":
                    return parts[1].strip()
                else:
                    return parts[0].strip()
        
        # Fallback: Return original content if no split tag is present
        return content
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>"


@eel.expose
def list_logbook_entries():
    """
    @brief Returns a list of all markdown files in the logbook folder with metadata.
    @details Gibt eine Liste aller Markdown-Dateien im logbuch/ Ordner mit Metadaten zurück.
    @return List of logbook entry objects / Liste von Logbuch-Eintrag-Objekten.
    """
    log_dir = PROJECT_ROOT / "docs" / "logbuch"
    if not log_dir.exists():
        return []

    entries = []

    def _normalize_status(status_raw: str) -> str:
        s = (status_raw or "").strip().upper()
        if not s:
            return "ACTIVE"
        if any(k in s for k in ["COMPLETE", "COMPLETED", "DONE", "ABGESCHLOSSEN", "FERTIG"]):
            return "COMPLETED"
        if any(k in s for k in ["PLAN", "PLANNING", "IDEA"]):
            return "PLAN"
        if any(k in s for k in ["DOC", "DOCS", "DOCUMENTATION"]):
            return "DOCS"
        if any(k in s for k in ["BUG", "ISSUE", "FIXME"]):
            return "BUG"
        if any(k in s for k in ["ACTIVE", "IN_PROGRESS", "IN PROGRESS", "TODO", "TASK", "OPEN"]):
            return "ACTIVE"
        return s
    # Natural sort by filename
    for f in sorted(log_dir.glob("*.md")):
        try:
            with open(f, 'r', encoding='utf-8') as fp:
                lines = [fp.readline() for _ in range(20)]  # Mehr Zeilen lesen um alles zu finden
                category = "Sonstiges"
                summary = ""
                status = "ACTIVE"  # Default
                title = f.stem
                pinned = False  # Default

                title_de = ""
                title_en = ""
                summary_de = ""
                summary_en = ""

                for line in lines:
                    line = line.strip()
                    # Support both <!-- Tag: Value --> and Tag: Value formats
                    content = line
                    if "<!--" in line and "-->" in line:
                        content = line.split("<!--")[1].split("-->")[0].strip()

                    if ":" in content:
                        key, val = content.split(":", 1)
                        key = key.strip()
                        val = val.strip()

                        if key == "Category":
                            category = val
                        elif key == "Status":
                            status = val
                        elif key == "Pinned":
                            pinned = val.lower() in ["true", "yes", "1"]
                        elif key == "Title_DE":
                            title_de = val
                        elif key == "Title_EN":
                            title_en = val
                        elif key == "Summary_DE":
                            summary_de = val
                        elif key == "Summary_EN":
                            summary_en = val
                        elif key == "Summary":
                            summary = val

                    md_status_match = re.match(r'^\*\*Status:\*\*\s*(.+)$', line)
                    if md_status_match:
                        status = md_status_match.group(1).strip()

                    if line.startswith("# "):
                        title = line.replace("# ", "").strip()

                # Special case for Known Issues
                if f.name == "00_Known_Issues.md":
                    category = "Bug"
                    if status == "ACTIVE":
                        status = "BUG"

                # Fallbacks
                if not title_de:
                    title_de = title
                if not title_en:
                    title_en = title

                # Bi-directional summary fallback
                if not summary:
                    summary = summary_de or summary_en
                if not summary_de:
                    summary_de = summary
                if not summary_en:
                    summary_en = summary

                # Final Selection based on language
                current_lang = get_language().lower()
                final_title = title
                final_summary = summary

                if current_lang == "en":
                    final_title = title_en or title
                    final_summary = summary_en or summary
                else:
                    final_title = title_de or title
                    final_summary = summary_de or summary

                entries.append({
                    "name": f.stem,
                    "filename": f.name,
                    "title": final_title,
                    "title_de": title_de,
                    "title_en": title_en,
                    "category": category,
                    "summary": summary,
                    "summary_de": summary_de,
                    "summary_en": summary_en,
                    "status": _normalize_status(status),
                    "pinned": pinned,
                    "source": "logbuch",
                    "modified_ts": f.stat().st_mtime,
                    "modified_iso": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(f.stat().st_mtime)),
                })
        except Exception:
            entries.append({
                "name": f.stem,
                "filename": f.name,
                "title": f.stem,
                "category": "Fehler",
                "summary": "",
                "status": "ERROR",
                "source": "logbuch",
                "modified_ts": 0,
                "modified_iso": "",
            })

    return entries


@eel.expose
def list_feature_modal_items():
    """
    Returns feature modal items from logbook plus selected markdown files from the project root.
    """
    items = [
        item for item in list_logbook_entries()
        if item.get("filename") != "31_Project_Documentation.md"
    ]

    root_dir = Path(__file__).parent
    root_docs = [
        ("README.md", "README", "Project overview and quick start."),
        ("DOCUMENTATION.md", "Documentation", "Detailed technical documentation."),
        ("INSTALL.md", "Installation", "Installation and setup instructions."),
        ("DEPENDENCIES.md", "Dependencies", "Dependency list and runtime requirements."),
        ("LICENSE.md", "License", "License and legal information."),
    ]

    for filename, title, summary in root_docs:
        path = root_dir / filename
        if not path.exists():
            continue
        mtime = path.stat().st_mtime
        items.append({
            "name": filename,
            "filename": filename,
            "title": title,
            "title_de": title,
            "title_en": title,
            "category": "Docs",
            "summary": summary,
            "summary_de": summary,
            "summary_en": summary,
            "status": "DOCS",
            "source": "root",
            "modified_ts": mtime,
            "modified_iso": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime)),
        })

    return items


@eel.expose
def save_logbook_entry(filename, content):
    """
    @brief Saves or updates a logbook entry file.
    @details Speichert oder aktualisiert einen Logbuch-Eintrag.
    @param filename Target filename / Ziel-Dateiname.
    @param content Markdown content / Markdown-Inhalt.
    @return Status or error dictionary / Status- oder Fehler-Dictionary.
    """
    log_dir = PROJECT_ROOT / "docs" / "logbuch"
    log_dir.mkdir(parents=True, exist_ok=True)

    # Sichere den Dateinamen
    if not filename.endswith('.md'):
        filename = filename + '.md'

    # Verhindere Directory Traversal
    if '/' in filename or '\\' in filename or filename.startswith('.'):
        return {"error": "Ungültiger Dateiname"}

    file_path = log_dir / filename

    try:
        if "Status:" not in content and "<!-- Status:" not in content:
            content = f"<!-- Status: ACTIVE -->\n{content}"
        file_path.write_text(content, encoding='utf-8')
        return {"status": "ok", "filename": filename}
    except Exception as e:
        return {"error": str(e)}


@eel.expose
def delete_logbook_entry(filename):
    """
    @brief Deletes a logbook entry from the disk.
    @details Löscht einen Logbuch-Eintrag.
    @param filename Entry filename / Dateiname des Eintrags.
    @return Status or error dictionary / Status- oder Fehler-Dictionary.
    """
    log_dir = PROJECT_ROOT / "docs" / "logbuch"

    if not filename.endswith('.md'):
        filename = filename + '.md'

    # Verhindere Directory Traversal
    if '/' in filename or '\\' in filename or filename.startswith('.') or '..' in filename:
        return {"error": "Ungültiger Dateiname"}

    file_path = log_dir / filename

    if not file_path.exists():
        return {"error": "Datei nicht gefunden"}

    try:
        file_path.unlink()
        return {"status": "ok"}
    except Exception as e:
        return {"error": str(e)}


@eel.expose
def run_tests(test_files):
    """
    @brief Executes selected pytest suites and returns the results.
    @details Führt ausgewählte pytest-Suiten aus und gibt die Ergebnisse zurück.
    @param test_files List of test filenames / Liste von Test-Dateinamen.
    @return Result dictionary with passes/fails and output / Ergebnis-Dictionary.
    """
    if DEBUG_FLAGS.get("tests"):
        debug_log(f"[Tests] Running files: {test_files}")

    if not test_files:
        return {"error": "Keine Test-Suiten ausgewählt."}

    # Verify files exist
    valid_files = []
    root_dir = Path(__file__).parents[2]
    test_dir = root_dir / "tests"
    for tf in test_files:
        p = test_dir / tf
        if p.exists():
            valid_files.append(str(p))

    if not valid_files:
        return {"error": "Keine gültigen Test-Dateien gefunden."}

    # We need to set PYTHONPATH so tests can import models/parsers
    env = os.environ.copy()
    env["PYTHONPATH"] = f"{root_dir}:{root_dir}/src"
    env["MWV_DISABLE_BROWSER_OPEN"] = "1"

    # Run pytest in a subprocess to avoid issues with repeat runs/sys.modules
    # Stream output lines live to frontend for real-time refresh.
    try:
        process = subprocess.Popen(
            [sys.executable, "-m", "pytest", "-q"] + valid_files,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            env=env,
            cwd=str(root_dir),
            bufsize=1,
            universal_newlines=True,
        )

        output_lines = []
        start_time = time.time()
        timeout_seconds = 900

        while True:
            if process.stdout is None:
                break

            line = process.stdout.readline()
            if line:
                output_lines.append(line)
                try:
                    if hasattr(eel, "append_test_output"):
                        eel.append_test_output(line)()
                except Exception:
                    pass
            elif process.poll() is not None:
                break

            if time.time() - start_time > timeout_seconds:
                process.kill()
                raise RuntimeError(f"Testlauf-Timeout nach {timeout_seconds}s")

        if process.stdout is not None:
            tail = process.stdout.read()
            if tail:
                output_lines.append(tail)
                try:
                    if hasattr(eel, "append_test_output"):
                        eel.append_test_output(tail)()
                except Exception:
                    pass

        result_code = process.wait()
        output = ''.join(output_lines)
        max_output_chars = 120000
        if len(output) > max_output_chars:
            output = (
                "[Output truncated: showing last part only]\n\n"
                + output[-max_output_chars:]
            )

        # Parse output for passed/failed (supports both verbose and -q pytest formats)
        passes = 0
        fails = 0
        match = re.search(r'(\d+)\s+passed', output)
        if match:
            passes = int(match.group(1))
        match_fails = re.search(r'(\d+)\s+failed', output)
        if match_fails:
            fails = int(match_fails.group(1))

        summary = f"{passes} passed, {fails} failed"

        return {
            "exit_code": result_code,
            "output": output,
            "summary": summary,
            "passes": passes,
            "fails": fails
        }
    except Exception as e:
        return {"error": str(e)}


@eel.expose
def run_gui_tests():
    """
    @brief Placeholder for GUI tests (handled via the agent).
    @details Dummy-Funktion für GUI-Tests (da diese über den Agenten laufen).
    @return Info dictionary / Info-Dictionary.

    Best Practices:
      - In Produktion: Integriere Playwright oder Selenium für Eel-GUIs.
      - Starte den Dev-Server und teste DOM-Interaktionen via Headless-Browser.
      - Für MCP-Agenten: Nutze Inspector-Tool für Tool-Validierung und Event-Simulation.
      - Alternativen: WebDriver (Selenium), CDP (Playwright), PyAutoGUI für Desktop.
      - Eel expose() ermöglicht bidirektionale Python-JS-Calls für Test-Trigger.
    """
    logging.info("GUI-Tests: Siehe MCP-Agent oder Browser-Subagent für KlickEvents/DOM.")
    return {
        "status": "info",
        "message": "GUI-Tests müssen über den MCP-Agenten DOM / Browser Subagent / KlickEvents gestartet werden.",
        "next_steps": [
            "pip install playwright pytest",
            "playwright install",
            "Beispiel: pytest mit page.goto('http://localhost:8000') und page.click()",
            "Alternativ: selenium, pyautogui, MCP Inspector"
        ],
        "protocols": {
            "WebDriver": "REST/HTTP, Selenium, geeignet für Eel",
            "CDP": "WebSocket, Playwright/Selenium4, direkter DOM-Zugriff",
            "Eel expose": "Intern, Python-JS-Bridge, ideal für Test-Trigger",
            "PyAutoGUI": "Pixel/Screen, Desktop-Automatisierung",
            "MCP": "Agenten-basiert, Inspector für Event-Simulation"
        }
    }


@eel.expose
def ui_trace(message):
    """
    Receives frontend UI trace lines and writes them to backend logs.
    """
    try:
        logging.info(f"[UI-Trace] {message}")
    except Exception:
        pass
    return {"status": "ok"}


# Main-Funktion, die die Eel-App startet
if __name__ == "__main__":
    _ensure_project_venv_active()
    env_handler.validate_safe_startup()

    no_gui_mode = is_no_gui_mode(sys.argv)
    connectionless_browser_mode = is_connectionless_browser_mode(sys.argv)

    # Logge den Start-Befehl (für das Debug-Fenster)
    startup_cmd = f"$ {sys.executable} {' '.join(sys.argv)}"
    # Only print on startup if a debug flag is active (though usually all are False initially)
    # Append to log silently so it's visible in the debug window later
    debug_log(startup_cmd)
    if any(DEBUG_FLAGS.values()):
        debug_log(startup_cmd)

    db.init_db()

    legacy_dbs = db.list_legacy_databases()
    if legacy_dbs:
        logging.warning("[DB] Legacy database files detected (ignored by app):")
        for legacy_db in legacy_dbs:
            logging.warning(f"[DB]  - {legacy_db}")
        logging.warning("[DB] Use reset_app_data() to remove legacy DB files.")

    # Ensure default scan dir is present and all scan dirs exist
    ensure_default_scan_dir()
    config_dirs = PARSER_CONFIG.get("scan_dirs", [])
    for d in config_dirs:
        Path(d).mkdir(parents=True, exist_ok=True)

    if no_gui_mode:
        sessionless_info = run_sessionless_mode()
        logging.info("[NoGUI] Mode enabled (--ng / --no-gui / --sessionless).")
        logging.info(f"[NoGUI] Active DB: {sessionless_info['active_db']}")
        logging.info(f"[NoGUI] Library entries: {sessionless_info['total_items']}")
        logging.info(f"[NoGUI] Configured scan dirs: {sessionless_info['scan_dirs']}")
        logging.info("[NoGUI] No Eel/WebSocket/Browser started. Exiting.")
        raise SystemExit(0)

    if connectionless_browser_mode:
        mode_info = run_connectionless_browser_mode()
        logging.info("[Mode-N] Connectionless browser mode enabled (--n).")
        logging.info(f"[Mode-N] Active DB: {mode_info['active_db']}")
        logging.info(f"[Mode-N] Library entries: {mode_info['total_items']}")
        logging.info(f"[Mode-N] Opened local UI: {mode_info['app_url']}")
        logging.info("[Mode-N] No Eel/WebSocket backend started. Exiting.")
        raise SystemExit(0)

    existing_sessions = [s for s in check_running_sessions() if s.get('port')]
    current_project_root = Path(__file__).resolve().parent

    def _session_project_root(session: dict) -> Path | None:
        cmdline = str(session.get('cmdline', '') or '')
        if not cmdline:
            return None

        for token in cmdline.split():
            token_clean = token.strip("'\"")
            if token_clean.endswith('main.py'):
                try:
                    return Path(token_clean).resolve().parent
                except Exception:
                    return None
        return None

    same_project_sessions = [
        s for s in existing_sessions
        if _session_project_root(s) == current_project_root
    ]

    if existing_sessions and not same_project_sessions:
        logging.info(
            "[Session] Ignoring running sessions from other project/install paths. "
            f"Current project root: {current_project_root}"
        )

    # Check for existing sessions of this project (same root path)
    existing_sessions = same_project_sessions
    if existing_sessions and os.environ.get("MWV_FORCE_NEW_SESSION") != "1":
        existing = existing_sessions[0]
        existing_url = f"http://localhost:{existing['port']}/app.html"

        if is_session_url_reachable(existing_url, timeout=0.8):
            logging.warning(
                f"[Session] Existing session detected (PID {existing['pid']}, port {existing['port']}). "
                "Skipping new window launch."
            )
            logging.info(f"[Session] Existing session URL: {existing_url}")

            if os.environ.get("MWV_DISABLE_BROWSER_OPEN") == "1":
                logging.info("[Session] Browser launch suppressed by MWV_DISABLE_BROWSER_OPEN=1")
            else:
                try:
                    if open_session_url(existing_url):
                        logging.info("[Session] Opened existing session URL.")
                except Exception as e:
                    logging.warning(f"[Session] Failed to open existing session URL: {e}")

            raise SystemExit(0)

        logging.warning(
            f"[Session] Ignoring stale session candidate (PID {existing['pid']}, port {existing['port']}) - URL unreachable."
        )


    # Erst-Scan beim Start (alle konfigurierten Verzeichnisse)
    # In einem Thread, damit die GUI sofort erscheint
    import threading
    threading.Thread(target=lambda: scan_media(dir_path=None, clear_db=True), daemon=True).start()

    # Log environment info for GUI console
    debug_log(f"[Startup] Environment Info: {get_environment_info_dict()}")


    web_dir = str(PROJECT_ROOT / "web")
    eel.init(web_dir)
    logger.debug("websocket", f"Eel initialized with root: {web_dir}")

    # GUI Console/Debug Tab: expose APIs for frontend
    # Frontend should call get_debug_console(), get_environment_info_dict(), get_imprint_info()

    if DEBUG_FLAGS["start"]:
        debug_log("[Startup] Starting Eel UI...")
    
    # Find a free port dynamically to allow multiple sessions
    import socket
    def find_free_port():
        """Find and return a free port for this session."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port
    
    # Check for fixed port (useful for CI/Tests)
    session_port = int(os.environ.get("MWV_PORT", 0))
    if session_port == 0:
        session_port = find_free_port()
    
    # Block=False verhindert, dass eel.start() den Server sofort beendet (sys.exit),
    # wenn Chrome den neuen Tab an einen bestehenden Prozess delegiert und sich sofort schließt.
    try:
        startup_duration = time.time() - STARTUP_TIME
        logging.info(f"[Startup-Trace] System ready for UI after {startup_duration:.2f}s.")
        logger.debug("websocket", f"Starting Eel server session on port {session_port}...")
        eel.start("app.html", mode=False, size=(1450, 800), block=False, port=session_port)
        
        # Open browser explicitly after Eel starts with session-specific URL
        session_url = f"http://localhost:{session_port}/app.html"
        logging.info(f"[Session] Opening browser at {session_url}")
        
        open_session_url(session_url)
        
    except Exception as e:
        logging.error(f"[Startup-Error] Failed to start session: {e}")

    # Server am Leben halten (robust gegen temporäre Frontend-Disconnects)
    while True:
        try:
            eel.sleep(1.0)
        except KeyboardInterrupt:
            logging.info("[Shutdown] KeyboardInterrupt received. Exiting.")
            raise
        except BaseException as e:
            logging.warning(f"[WebSocket] keepalive recovered from base error: {type(e).__name__}: {e}")
            time.sleep(1.0)


    @eel.expose
    def test_pyautogui():
        """
        Simple test for pyautogui integration.
        Returns screen size and current mouse position.
        """
        try:
            import pyautogui
            screen_size = pyautogui.size()
            mouse_pos = pyautogui.position()
            return {
                "status": "ok",
                "screen_size": {"width": screen_size.width, "height": screen_size.height},
                "mouse_position": {"x": mouse_pos.x, "y": mouse_pos.y}
            }
        except Exception as e:
            return {"status": "error", "message": str(e)}
