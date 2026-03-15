#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Debug Flags Test
# Eingabewerte: DEBUG_FLAGS dictionary
# Ausgabewerte: Flag activation status
# Testdateien: Keine (Runtime test)
# Kommentar: Testet Debug-Flag-System.
import logging
import src.core.logger as logger

def test_debug_component_filtering():
    """Verifies that logger.debug only logs if the component flag is set."""
    logger.setup_logging(debug_mode=True)
    # Reset flags
    test_flags = {"db": False, "scan": True, "system": False}
    logger.set_debug_flags(test_flags)
    
    # Clear buffer
    logger.LOG_BUFFER.clear()
    
    # This should be ignored (db is False)
    logger.debug("db", "DATABASE_SECRET_LOG")
    # This should be logged (scan is True)
    logger.debug("scan", "SCANNING_IMPORTANT_FILE")
    # This should be ignored (unknown component defaults to False unless system is True)
    logger.debug("api", "API_REQUEST_DETAILS")
    
    logs = logger.get_ui_logs()
    assert not any("DATABASE_SECRET_LOG" in log for log in logs)
    assert any("SCANNING_IMPORTANT_FILE" in log for log in logs)
    assert not any("API_REQUEST_DETAILS" in log for log in logs)

def test_system_debug_override():
    """Verifies that system flag enables all debug logs."""
    test_flags = {"db": False, "system": True}
    logger.set_debug_flags(test_flags)
    logger.LOG_BUFFER.clear()
    
    logger.debug("db", "FORCE_LOG_VIA_SYSTEM")
    
    logs = logger.get_ui_logs()
    assert any("FORCE_LOG_VIA_SYSTEM" in log for log in logs)
