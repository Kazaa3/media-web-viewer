# logger.py - Centralized logging system for dict.
#dict - Desktop Media Player and Library Manager v1.34
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
        "timestamp": datetime.utcnow().isoformat(),
        "type": error_type,
        "message": message,
        "context": context or {}
    }
    try:
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

# Setup paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
LOCAL_LOG_DIR = PROJECT_ROOT / "logs"

if LOCAL_LOG_DIR.exists() or not (Path.home() / ".media-web-viewer").exists():
    LOCAL_LOG_DIR.mkdir(parents=True, exist_ok=True)
    APP_DATA_DIR = LOCAL_LOG_DIR
    LOG_FILE = APP_DATA_DIR / "app.log"
    DEBUG_LOG_FILE = APP_DATA_DIR / "debug.log"
else:
    APP_DATA_DIR = Path.home() / ".media-web-viewer"
    APP_DATA_DIR.mkdir(parents=True, exist_ok=True)
    LOG_FILE = APP_DATA_DIR / "app.log"
    DEBUG_LOG_FILE = PROJECT_ROOT / "logs" / "debug.log"

# UI Log Buffer (accessible by Eel)
LOG_BUFFER: List[str] = []
MAX_BUFFER_SIZE = 10000

# Reference to DEBUG_FLAGS from main (initialized during setup)
_debug_flags = {}

def set_debug_flags(flags: dict):
    """Update internal reference to debug flags."""
    global _debug_flags
    _debug_flags = flags


class UIHandler(logging.Handler):
    """
    Custom logging handler to feed the UI log buffer.
    """
    def emit(self, record):
        try:
            msg = self.format(record)
            
            # Avoid recursion if msg already contains UI-Trace tag
            if "[UI-Trace]" in msg:
                return

            LOG_BUFFER.append(msg)

            # Keep buffer size manageable
            if len(LOG_BUFFER) > MAX_BUFFER_SIZE:
                LOG_BUFFER.pop(0)
            
            # Real-time UI tracing if Eel is initialized and has a connection
            import eel
            if hasattr(eel, 'appendUiTrace') and getattr(eel, '_websocket', None):
                try:
                    eel.appendUiTrace(msg) # Asynchronous push, don't wait for return
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
    
    # Identify environment target (from venv path)
    venv_path = sys.prefix
    target = "unknown"
    if ".venv_run" in venv_path or ".venv_core" in venv_path:
        target = "core"
    elif ".venv_dev" in venv_path:
        target = "dev"
    elif ".venv" == os.path.basename(venv_path):
        target = "full"
    elif ".venv_test" in venv_path:
        target = "test"
    elif ".venv_selenium" in venv_path:
        target = "selenium"
    elif ".venv_build" in venv_path:
        target = "build"

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


def setup_logging(debug_mode: bool = False, level: Optional[int] = None):
    """
    Initializes the centralized logging system.
    @param debug_mode If True, additional debug file loggers are activated.
    @param level Optional explicit logging level (e.g. logging.DEBUG, logging.INFO).
    """
    root_logger = logging.getLogger()
    
    # Clear existing handlers if any (useful for re-init)
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    if level is None:
        level = logging.DEBUG if debug_mode else logging.INFO
    root_logger.setLevel(level)

    # Format
    # In debug mode, we include more technical details (file, line, thread)
    force_debug = os.environ.get("MWV_DEBUG_FORCE") == "1"
    if debug_mode or force_debug:
        format_str = '%(asctime)s [%(levelname).4s] [%(name)s] [%(threadName)s] [%(filename)s:%(lineno)d] %(message)s'
    else:
        format_str = '%(asctime)s [%(levelname).4s] [%(name)s] %(message)s'

    formatter = logging.Formatter(format_str, datefmt='%H:%M:%S')

    # 1. Console Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # 2. Rotating File Handler (User Data)
    try:
        file_handler = logging.handlers.RotatingFileHandler(
            LOG_FILE, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    except Exception as e:
        logging.error(f"Failed to initialize file logger: {e}")

    # 3. Project-Local Debug File Handler (only if debug_mode is True)
    if debug_mode:
        try:
            DEBUG_LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
            debug_file_handler = logging.handlers.RotatingFileHandler(
                DEBUG_LOG_FILE, maxBytes=10*1024*1024, backupCount=1, encoding='utf-8'
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
def stall_watchdog(task_name: str, threshold: float = 2.0):
    """
    Context manager to monitor for stalls in backend functions.
    Logs start, duration, and warnings if threshold is exceeded.
    """
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
