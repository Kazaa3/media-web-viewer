#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Logging System Test
# Eingabewerte: logger.py module
# Ausgabewerte: Log formatting, File/Console output
# Testdateien: logs/*.log
# Kommentar: Testet Logging-System.
import logging
import logger
from pathlib import Path

# Mock main.debug_log for bridge test if needed, or just test logger directly

PROJECT_ROOT = Path(__file__).parent.parent
DEBUG_LOG_PATH = PROJECT_ROOT / "logs" / "debug.log"

def test_logging_setup():
    """Verifies that logging is correctly initialized."""
    logger.setup_logging(debug_mode=True)
    root_logger = logging.getLogger()
    assert root_logger.level == logging.DEBUG
    assert len(root_logger.handlers) >= 3  # Console, File, UI

def test_logging_file_persistence():
    """Verifies that logs are written to the file."""
    logger.setup_logging(debug_mode=True)
    test_msg = "LOGGING_TEST_PERSISTENCE_MESSAGE"
    logging.info(test_msg)
    
    log_file = logger.LOG_FILE
    assert log_file.exists()
    
    with open(log_file, "r", encoding='utf-8') as f:
        content = f.read()
    assert test_msg in content

def test_ui_buffer_integration():
    """Verifies that logs appear in the UI buffer."""
    logger.setup_logging(debug_mode=False)
    test_msg = "LOGGING_TEST_UI_MESSAGE"
    logging.info(test_msg)
    
    ui_logs = logger.get_ui_logs()
    assert any(test_msg in log for log in ui_logs)

def test_component_loggers():
    """Verifies that specialized loggers work."""
    web_log = logger.get_logger("web")
    test_msg = "LOGGING_TEST_WEB_COMPONENT"
    web_log.info(test_msg)
    
    ui_logs = logger.get_ui_logs()
    assert any(test_msg in log and "[app.web]" in log for log in ui_logs)


def test_ui_log_buffer_limit():
    """Verifies that the UI log buffer doesn't grow indefinitely."""
    logger.setup_logging(debug_mode=False)
    for i in range(logger.MAX_BUFFER_SIZE + 50):
        logging.info(f"Test message {i}")
    
    ui_logs = logger.get_ui_logs()
    assert len(ui_logs) == logger.MAX_BUFFER_SIZE


def test_project_debug_log_file():
    """Verifies that debug logs are written to logs/debug.log in debug mode."""
    # Ensure logs directory exists for the test
    DEBUG_LOG_PATH.parent.mkdir(exist_ok=True)
    if DEBUG_LOG_PATH.exists():
        DEBUG_LOG_PATH.unlink()

    logger.setup_logging(debug_mode=True)
    test_msg = "LOGGING_TEST_PROJECT_DEBUG_MESSAGE"
    logging.debug(test_msg)

    assert DEBUG_LOG_PATH.exists()
    with open(DEBUG_LOG_PATH, "r", encoding='utf-8') as f:
        content = f.read()
    assert test_msg in content


def test_gevent_log_suppression():
    """Verifies that geventwebsocket logs are suppressed (set to WARNING)."""
    logger.setup_logging(debug_mode=False)
    gevent_logger = logging.getLogger("geventwebsocket.handler")
    assert gevent_logger.level == logging.WARNING
