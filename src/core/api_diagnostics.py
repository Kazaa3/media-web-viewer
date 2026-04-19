from pathlib import Path
import platform
from datetime import datetime
from unittest.mock import MagicMock

# Robust Eel shell fallback
try:
    from src.core.eel_shell import eel
except ImportError:
    import eel

# [v1.53.003-R2] Defensive Dependency Safeguard
try:
    import pyautogui
except ImportError as e:
    # Use MagicMock to satisfy the symbol table without crashing the process
    # This prevents ModuleNotFoundError on systems where auto-install failed.
    import logging
    logging.getLogger("api_diagnostics").warning(f"[Audit-Pulse] pyautogui NOT FOUND: Using Mock Fallback. Reason: {e}")
    pyautogui = MagicMock()

from src.core.config_master import (
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
    Utilizes scrot fallback via mocked tkinter (v1.46.142).
    """
    try:
        # Ensure display is available for Linux
        if sys.platform.startswith('linux') and not os.environ.get('DISPLAY'):
             os.environ['DISPLAY'] = ':0' 

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"workstation_snapshot_{timestamp}.png"
        filepath = AUDIT_REPORTS_DIR / filename
        
        screenshot = pyautogui.screenshot()
        screenshot.save(str(filepath))
        
        log.info(f"[Audit] Forensic screenshot saved: {filename}")
        return {"status": "ok", "path": str(filepath), "filename": filename}
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
            "version": "v1.46.142",
            "timestamp": datetime.now().isoformat(),
            "station_id": GLOBAL_CONFIG.get("station_id", "STATION_ALPHA"),
            "inventory": inventory,
            "connectivity": liveness,
            "dom_audit": GLOBAL_CONFIG.get("last_dom_audit", "PENDING"),
            "status": "VALIDATED" if liveness["status"] == "HEALTHY" else "FAULTY"
        }
        
        report_file = AUDIT_REPORTS_DIR / f"audit_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        report_file.write_text(json.dumps(report, indent=4), encoding='utf-8')
        
        log.info(f"[Audit] Standardized Global Audit generated: {report_file.name}")
        return {"status": "ok", "report_path": str(report_file), "report": report}
    except Exception as e:
        log.error(f"[Audit] Global audit failed: {e}")
        return {"status": "error", "message": str(e)}

# --- Rescue & Recovery Operations (Migrated from main.py v1.54.018) ---

@eel.expose
def kill_stale_and_restart():
    """ Kills all project-related processes and restarts. """
    from src.core.process_manager import ProcessController
    log.info(f"[RESTART] Using ProcessController for emergency cleanup. Root: {PROJECT_ROOT}")
    pc = ProcessController(PROJECT_ROOT, Path(GLOBAL_CONFIG["storage_registry"]["data_dir"]))
    pc.kill_stale_instances(current_pid=os.getpid())
    log.warning("[RESTART] Executing os.execl...")
    python = sys.executable
    os.execl(python, python, *sys.argv)

@eel.expose
def trigger_factory_reset():
    """ Exposed wrapper to perform a database reset from the UI. """
    log.warning("[System] Factory reset triggered via Eel.")
    from src.core.db import factory_reset
    return factory_reset()

@eel.expose
def trigger_db_reconnect():
    """ Exposed wrapper to re-initialize the database connection. """
    log.warning("[System] Database Reconnect triggered via Eel.")
    from src.core.db import init_db
    init_db()
    return True

# --- Enhanced Orchestration & Diagnostics (Migrated from main.py v1.54.018) ---

@eel.expose
def rtt_ping(data):
    """ Multi-stage RTT Ping for verification. """
    size = len(json.dumps(data))
    is_heartbeat = isinstance(data, dict) and data.get("type") == "heartbeat"
    if is_heartbeat:
        GLOBAL_CONFIG["frontend_last_heartbeat"] = time.time()
    else:
        log.info(f"[RTT] Ping received ({size} bytes). Data types: {type(data).__name__}")
    
    # Sanitization wrapper is internal (simplified version here)
    return {
        "status": "pong",
        "timestamp": time.time(),
        "received_size": size,
        "echo": data,
        "is_heartbeat": is_heartbeat
    }

@eel.expose
def log_js_error(error_data):
    """ Logs JavaScript errors OR toast messages from the frontend. """
    if error_data.get('type') == 'TOAST':
        log.info(f"[JS-TOAST] {error_data.get('message')}")
    else:
        log.error(f"[JS-ERROR] {json.dumps(error_data)}")
    return {"status": "error_logged"}

@eel.expose
def run_video_transcode_diagnostic(file_path=None):
    """ Executes a real-time probe of the video transcoding/remuxing pipelines. """
    from src.core import db
    import requests
    target_path = file_path
    if not target_path:
        items = db.get_library()
        if items: target_path = items[0]['path']
        else: return {"status": "error", "error": "No media found in library to test."}

    log.info(f"[Diagnostic] Testing video pipeline for: {target_path}")
    results = []
    base_url = GLOBAL_CONFIG['network_settings'].get('api_root', f"http://{GLOBAL_CONFIG['network_settings']['host']}:{GLOBAL_CONFIG['network_settings']['port']}")
    encoded_path = requests.utils.quote(target_path)
    endpoints = [
        {"name": "Remux (Fast)", "url": f"{base_url}/video-remux-stream/{encoded_path}"},
        {"name": "Transcode (Safe)", "url": f"{base_url}/stream/via/transcode/{encoded_path}"}
    ]
    atom_cfg = GLOBAL_CONFIG.get("atom_detection", {"atoms": ["ftyp", "moof", "mdat", "moov"], "header_limit": 4096})

    for ep in endpoints:
        ep_result = {"name": ep['name'], "status": "unknown", "details": ""}
        try:
            r = requests.get(ep['url'], stream=True, timeout=15)
            if r.status_code == 200:
                chunk = next(r.iter_content(chunk_size=1024), b'')
                atoms = [a.encode() if isinstance(a, str) else a for a in atom_cfg["atoms"]]
                limit = atom_cfg["header_limit"]
                found = [a.decode() if isinstance(a, bytes) else a for a in atoms if a in chunk[:limit]]
                if found:
                    ep_result["status"] = "success"
                    ep_result["details"] = f"Valid MP4 atoms found: {', '.join(found)}"
                else:
                    ep_result["status"] = "failed"
                    ep_result["details"] = f"No valid MP4 atoms in start of stream."
            else:
                ep_result["status"] = "failed"
                ep_result["details"] = f"HTTP Error {r.status_code}"
            r.close()
        except Exception as e:
            ep_result["status"] = "error"
            ep_result["details"] = str(e)
        results.append(ep_result)
    return {"status": "complete", "results": results, "target": target_path}

@eel.expose
def get_gevent_status():
    """ Returns the status of gevent patching and version info. """
    try:
        import gevent
        from gevent import monkey
        import greenlet
        return {
            "active": True,
            "version": gevent.__version__,
            "greenlet": greenlet.__version__,
            "patched": {
                "socket": monkey.is_module_patched("socket"),
                "threading": monkey.is_module_patched("threading")
            }
        }
    except ImportError:
        return {"active": False, "error": "gevent not installed"}

@eel.expose
def get_active_video_workers():
    """ Video Health: Live Worker Audit. """
    import psutil
    workers = []
    try:
        cwd = os.getcwd()
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                name = (proc.info.get('name') or "").lower()
                cmdline = " ".join(proc.info.get('cmdline') or []).lower()
                if 'ffmpeg' in name or 'mkvmerge' in name:
                    workers.append({
                        "pid": proc.info['pid'],
                        "name": proc.info['name'],
                        "is_workspace": cwd in cmdline
                    })
            except (psutil.NoSuchProcess, psutil.AccessDenied): continue
        return {"status": "ok", "workers": workers}
    except Exception as e:
        log.error(f"[Forensic-VID] Worker Audit Failed: {e}")
        return {"status": "error", "message": str(e)}

@eel.expose
def get_hydration_stats():
    """ Forensic Hydration Sync: Returns raw counts for DB Index vs Backend Cache. """
    from src.core import db
    import sqlite3
    results = {"db_index": 0, "backend_cache": 0, "status": "ok"}
    try:
        conn = sqlite3.connect(db.DB_FILENAME)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM media")
        results["db_index"] = cursor.fetchone()[0]
        conn.close()
        items = db.get_library()
        results["backend_cache"] = len(items)
        return results
    except Exception as e:
        log.error(f"[Forensic-DBI] Audit failed: {e}")
        return {"status": "error", "error": str(e)}

@eel.expose
def set_log_level(level):
    """ Dynamically updates the application log level. """
    import logging
    valid_levels = {"DEBUG": logging.DEBUG, "INFO": logging.INFO, "WARNING": logging.WARNING, "ERROR": logging.ERROR}
    if level in valid_levels:
        logging.getLogger().setLevel(valid_levels[level])
        log.warning(f"[System] Log level changed to {level}.")
        return {"status": "success", "level": level}
    return {"status": "error", "message": f"Invalid level: {level}"}
