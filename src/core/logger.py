#dict - Desktop Media Player and Library Manager v1.41.00
# # logger.py - Centralized logging system for dict.
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
# logger.py - Centralized Logging System

Dieses Modul stellt ein zentrales Logging-System für das dict-Projekt bereit.

Features:
- Logging für Backend, UI und Tests
- Logbuffer-Unterstützung für Session- und Fehleranalyse
- File- und Stream-Handler für CI/CD und lokale Entwicklung
- Integration mit Logbuffer API und UI-Logzugriff

Verwendung:
- Für Desktop- und CI/CD-Integrationen, nicht für Browser-Frontend.

"""

import json

def log_frontend_error(error_type: str, message: str, context: dict = None):
    """
    Log a structured frontend error to logs/frontend_errors.log
    :param error_type: Type/category of error (e.g. JS, UI, Network)
    :param message: Error message
    :param context: Additional context as dict (optional)
    """
    from datetime import datetime
    log_path = LOCAL_LOG_DIR / "frontend_errors.log"
    entry = {
        "timestamp": datetime.now().isoformat(),
        "type": error_type,
        "message": message,
        "context": context or {}
    }
    try:
        log_path.parent.mkdir(parents=True, exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    except Exception as e:
        logging.error(f"Failed to write frontend error log: {e}")




import logging
import logging.handlers
import os
import time
import contextlib
from pathlib import Path
from typing import List, Optional, Any

# --- Environment Integration (v1.41.00 Centralized) ---
from src.core.config_master import GLOBAL_CONFIG, PROJECT_ROOT, APP_DATA_DIR

# --- Module Exports (v1.41.00) ---
# Ensure other modules can access these via logger.XXX
APP_DATA_DIR = APP_DATA_DIR 

REGISTRY = GLOBAL_CONFIG.get("logging_registry", {})
LOCAL_LOG_DIR = Path(REGISTRY.get("log_root", str(PROJECT_ROOT / "logs")))
LOG_FILE = Path(REGISTRY.get("main_log", str(LOCAL_LOG_DIR / "app.log")))
DEBUG_LOG_FILE = Path(LOCAL_LOG_DIR / "debug.log")

if not LOCAL_LOG_DIR.exists():
    LOCAL_LOG_DIR.mkdir(parents=True, exist_ok=True)

# UI Log Buffer (accessible by Eel)
LOG_BUFFER: List[str] = []
MAX_BUFFER_SIZE = REGISTRY.get("max_buffer_size", 10000)

_debug_flags = {}
_last_ui_broadcast = 0.0
UI_BROADCAST_COOLDOWN = 0.02 # Max 50 messages/sec (v1.41.00)

def set_debug_flags(flags: dict):
    """Update internal reference to debug flags."""
    global _debug_flags
    _debug_flags = flags


class UIHandler(logging.Handler):
    """
    Custom logging handler to feed the UI log buffer.
    """
    def emit(self, record):
        global _last_ui_broadcast
        try:
            msg = self.format(record)
            
            # [Echo Guard] v1.41.00: Do not send logs back that originated from the UI!
            # [Blind-Mute] v1.41.00: Silence heavy render-traces to prevent UI freezing
            if "[UI-Trace]" in msg or "[BD-AUDIT]" in msg or "[JS-NAV]" in msg or "[UI-INPUT]" in msg \
               or "[UI-RENDER]" in msg or "[DOM-UI]" in msg:
                return

            LOG_BUFFER.append(msg)

            # Keep buffer size manageable
            if len(LOG_BUFFER) > MAX_BUFFER_SIZE:
                LOG_BUFFER.pop(0)
            
            # Real-time UI tracing with Rate Limiting (v1.41.00)
            now = time.time()
            if (now - _last_ui_broadcast) < UI_BROADCAST_COOLDOWN:
                return

            import eel
            # Round 5.5: Skip if no browser is connected to prevent hangs
            websockets = getattr(eel, '_websockets', [])
            if not websockets or len(websockets) == 0:
                return

            if hasattr(eel, 'appendUiTrace'):
                try:
                    eel.appendUiTrace(msg)
                    _last_ui_broadcast = now
                except Exception:
                    pass
        except Exception:
            self.handleError(record)


def log_system_diagnostics():
    """Logs detailed system and environment information for debugging."""
    import sys
    import platform
    import eel
    from datetime import datetime
    
    # Identify environment target (from venv path) (SSOT v1.35.92)
    venv_path = sys.prefix
    target = "unknown"
    mapping = REGISTRY.get("venv_mapping", {})
    
    # Check for direct folder name match (e.g. .venv)
    folder_name = os.path.basename(venv_path)
    if folder_name in mapping:
        target = mapping[folder_name]
    else:
        # Fallback to substring matching for robustness
        for key, val in mapping.items():
            if key in venv_path:
                target = val
                break

    logging.debug("--- [SYSTEM DIAGNOSTICS] START ---")
    logging.debug(f"Timestamp: {datetime.utcnow().isoformat()}")
    logging.debug(f"OS: {platform.system()} {platform.release()} ({platform.machine()})")
    logging.debug(f"Python: {sys.version}")
    logging.debug(f"Executable: {sys.executable}")
    logging.debug(f"Venv Path: {venv_path}")
    logging.debug(f"Runtime Target: {target}")
    logging.debug(f"Eel Version: {getattr(eel, '__version__', 'unknown')}")
    
    # Log critical env vars
    for key in ["MWV_DEBUG_FORCE", "PATH"]:
        if key in os.environ:
            logging.debug(f"Env Var {key}: {os.environ[key]}")
    
    logging.debug("--- [SYSTEM DIAGNOSTICS] END ---")


def setup_logging(debug_mode: bool = False, level: Optional[int] = None, session_id: Optional[str] = None):
    """
    Initializes the centralized logging system.
    @param debug_mode If True, additional debug file loggers are activated.
    @param level Optional explicit logging level (e.g. logging.DEBUG, logging.INFO).
    @param session_id If provided, creates a unique session log file in logs/.
    """
    root_logger = logging.getLogger()
    
    # Clear existing handlers if any (useful for re-init)
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    if level is None:
        level = logging.DEBUG if debug_mode else logging.INFO
    root_logger.setLevel(level)

    # Determine session-specific log file
    session_log_path = None
    if session_id:
        session_log_path = REGISTRY.get("session_log") or str(LOCAL_LOG_DIR / f"session_{session_id}.log")
        logging.info(f"Session-specific logging enabled: {session_log_path}")

    # In debug mode, we include more technical details (file, line, thread, function)
    force_debug = REGISTRY.get("debug_force", False)
    if debug_mode or force_debug:
        format_str = '%(asctime)s [%(levelname)s] [%(name)s] [%(threadName)s] [%(funcName)s] [%(filename)s:%(lineno)d] %(message)s'
    else:
        format_str = '%(asctime)s [%(levelname)s] [%(name)s] %(message)s'

    date_fmt = REGISTRY.get("log_datefmt", "%H:%M:%S")
    formatter = logging.Formatter(format_str, datefmt=date_fmt)

    # 1. Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # 2. Rotating File Handler (User Data)
    try:
        max_bytes = REGISTRY.get("max_size_mb", 10) * 1024 * 1024
        backup_count = REGISTRY.get("backup_count", 3)
        file_handler = logging.handlers.RotatingFileHandler(
            LOG_FILE, maxBytes=max_bytes, backupCount=backup_count, encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    except Exception as e:
        logging.error(f"Failed to initialize file logger: {e}")

    # 2b. Session-Specific File Handler
    if session_log_path:
        try:
            session_file_handler = logging.FileHandler(session_log_path, encoding='utf-8')
            session_file_handler.setFormatter(formatter)
            root_logger.addHandler(session_file_handler)
            logging.info(f"Session log initialized at: {session_log_path}")
        except Exception as e:
            logging.error(f"Failed to initialize session logger: {e}")

    # 3. Project-Local Debug File Handler (only if debug_mode is True)
    if debug_mode:
        try:
            DEBUG_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
            d_max_bytes = REGISTRY.get("debug_max_size_mb", 10) * 1024 * 1024
            d_backup_count = REGISTRY.get("debug_backup_count", 1)
            debug_file_handler = logging.handlers.RotatingFileHandler(
                DEBUG_LOG_FILE, maxBytes=d_max_bytes, backupCount=d_backup_count, encoding='utf-8'
            )
            debug_file_handler.setFormatter(formatter)
            root_logger.addHandler(debug_file_handler)
            logging.info(f"Project-local debug log initialized at: {DEBUG_LOG_FILE}")
        except Exception as e:
            logging.error(f"Failed to initialize project-local debug logger: {e}")

    # 4. UI Buffer Handler
    ui_handler = UIHandler()
    ui_handler.setFormatter(formatter)
    root_logger.addHandler(ui_handler)

    # Suppress noisy third-party logs
    logging.getLogger("geventwebsocket.handler").setLevel(logging.WARNING)

    logging.info("Logging system initialized.")
    if debug_mode:
        logging.debug("Debug mode activated via command line or configuration.")
        log_system_diagnostics()


def get_logger(name: str):
    """
    Returns a logger instance for a specific module.
    Automatically prefixes with 'app.' to allow global filtering.
    """
    if name.startswith("src.core."):
        name = name.replace("src.core.", "")
    return logging.getLogger(f"app.{name}")


# --- Convenience Wrappers (SCR-004 fix) ---
def info(msg: str):
    logging.info(msg)

def error(msg: str):
    logging.error(msg)

def warning(msg: str):
    logging.warning(msg)

def exception(msg: str):
    logging.exception(msg)


def debug(component: str, message: str):
    """
    Log a message if the corresponding DEBUG_FLAGS component is active.
    @param component Key in DEBUG_FLAGS (e.g. 'scan', 'db')
    @param message The log message.
    """
    if _debug_flags.get(component) or _debug_flags.get("system"):
        logging.debug(f"[{component}] {message}")


def get_ui_logs() -> List[str]:
    """
    Returns the current UI log buffer.
    """
    return LOG_BUFFER

def progress_update(task: str, percent: int, status: str = "active"):
    """
    Pushes a progress update to the UI via Eel.
    @param task Name of the current operation.
    @param percent Completion percentage (0-100).
    @param status 'active', 'complete', or 'error'.
    """
    import eel
    msg = f"[PROGRESS] {task}: {percent}% ({status})"
    logging.info(msg)
    if hasattr(eel, 'update_progress') and getattr(eel, '_websocket', None):
        try:
            eel.update_progress({"task": task, "percent": percent, "status": status})()
        except Exception:
            pass

@contextlib.contextmanager
def stall_watchdog(task_name: str, threshold: float = None):
    """
    Context manager to monitor for stalls in backend functions.
    Logs start, duration, and warnings if threshold is exceeded.
    """
    if threshold is None:
        threshold = REGISTRY.get("watchdog_threshold", 2.0)
    start_time = time.time()
    logging.info(f"[WATCHDOG] START: {task_name}")
    progress_update(task_name, 0, "active")
    try:
        yield
    finally:
        duration = time.time() - start_time
        logging.info(f"[WATCHDOG] FINISH: {task_name} (took {duration:.2f}s)")
        if duration > threshold:
            logging.warning(f"[STALL] Task '{task_name}' exceeded threshold: {duration:.2f}s > {threshold}s")
        progress_update(task_name, 100, "complete")
