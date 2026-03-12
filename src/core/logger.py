#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
logger.py - Centralized logging system for Media Web Viewer.
"""

import logging
import logging.handlers
import os
from pathlib import Path
from typing import List

# Setup paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
LOCAL_LOG_DIR = PROJECT_ROOT / "data" / "logs"

if LOCAL_LOG_DIR.exists():
    APP_DATA_DIR = LOCAL_LOG_DIR
    LOG_FILE = APP_DATA_DIR / "app.log"
    DEBUG_LOG_FILE = APP_DATA_DIR / "debug.log"
else:
    APP_DATA_DIR = Path.home() / ".media-web-viewer"
    APP_DATA_DIR.mkdir(parents=True, exist_ok=True)
    LOG_FILE = APP_DATA_DIR / "app.log"
    DEBUG_LOG_FILE = Path(__file__).parent / "logs" / "debug.log"

# UI Log Buffer (accessible by Eel)
LOG_BUFFER: List[str] = []
MAX_BUFFER_SIZE = 1000

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
            LOG_BUFFER.append(msg)
            # Keep buffer size manageable
            if len(LOG_BUFFER) > MAX_BUFFER_SIZE:
                LOG_BUFFER.pop(0)
        except Exception:
            self.handleError(record)


def setup_logging(debug_mode: bool = False):
    """
    Initializes the centralized logging system.
    @param debug_mode If True, sets the root logger level to DEBUG.
    """
    root_logger = logging.getLogger()
    
    # Clear existing handlers if any (useful for re-init)
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    level = logging.DEBUG if debug_mode else logging.INFO
    root_logger.setLevel(level)

    # Format
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] [%(name)s] %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

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
        print(f"Failed to initialize file logger: {e}")

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
            print(f"Failed to initialize project-local debug logger: {e}")

    # 4. UI Buffer Handler
    ui_handler = UIHandler()
    ui_handler.setFormatter(formatter)
    root_logger.addHandler(ui_handler)

    # Suppress noisy third-party logs
    logging.getLogger("geventwebsocket.handler").setLevel(logging.WARNING)

    logging.info("Logging system initialized.")
    if debug_mode:
        logging.debug("Debug mode activated via command line or configuration.")


def get_logger(name: str):
    """
    Returns a logger instance for a specific module.
    """
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
