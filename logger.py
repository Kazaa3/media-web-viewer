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
APP_DATA_DIR = Path.home() / ".media-web-viewer"
APP_DATA_DIR.mkdir(parents=True, exist_ok=True)
LOG_FILE = APP_DATA_DIR / "app.log"

# UI Log Buffer (accessible by Eel)
LOG_BUFFER: List[str] = []
MAX_BUFFER_SIZE = 1000


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

    # 2. Rotating File Handler
    try:
        file_handler = logging.handlers.RotatingFileHandler(
            LOG_FILE, maxBytes=5*1024*1024, backupCount=3, encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)
    except Exception as e:
        print(f"Failed to initialize file logger: {e}")

    # 3. UI Buffer Handler
    ui_handler = UIHandler()
    ui_handler.setFormatter(formatter)
    root_logger.addHandler(ui_handler)

    logging.info("Logging system initialized.")
    if debug_mode:
        logging.debug("Debug mode activated via command line or configuration.")


def get_logger(name: str):
    """
    Returns a logger instance for a specific module.
    """
    return logging.getLogger(f"app.{name}")


def get_ui_logs() -> List[str]:
    """
    Returns the current UI log buffer.
    """
    return LOG_BUFFER
