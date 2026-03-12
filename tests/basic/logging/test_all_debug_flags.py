#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: All Debug Flags Test
# Eingabewerte: All DEBUG_FLAGS
# Ausgabewerte: Comprehensive validation
# Testdateien: Keine
# Kommentar: Testet alle Debug-Flags.
import unittest
import sys
from pathlib import Path

# Add project root to path

import src.core.main as main
import src.core.logger as logger
import logging

class TestAllDebugFlags(unittest.TestCase):
    def setUp(self):
        # Initialize logging for test
        logger.setup_logging(debug_mode=True)
        # Reset debug flags
        for key in main.DEBUG_FLAGS:
            main.DEBUG_FLAGS[key] = False
        logger.set_debug_flags(main.DEBUG_FLAGS)
        logger.LOG_BUFFER.clear()

    def test_flag_definitions(self):
        """Verify all expected flags are present."""
        expected_flags = [
            "system", "ui", "lib", "browser", "edit", "options", 
            "start", "parser", "scan", "player", "db", "tests",
            "api", "web", "i18n", "websocket", "performance",
            "metadata", "transcode", "file_ops", "network"
        ]
        for flag in expected_flags:
            self.assertIn(flag, main.DEBUG_FLAGS, f"Missing flag: {flag}")

    def test_log_triggering(self):
        """Verify that setting a flag enables logging for that component."""
        for flag in main.DEBUG_FLAGS:
            with self.subTest(flag=flag):
                logger.LOG_BUFFER.clear()
                main.DEBUG_FLAGS[flag] = True
                logger.set_debug_flags(main.DEBUG_FLAGS)
                
                test_msg = f"TEST_LOG_{flag.upper()}"
                logger.debug(flag, test_msg)
                
                # Check if message is in buffer
                found = any(test_msg in log for log in logger.LOG_BUFFER)
                self.assertTrue(found, f"Logger did not capture message for flag: {flag}")
                
                # Disable and check again
                logger.LOG_BUFFER.clear()
                main.DEBUG_FLAGS[flag] = False
                logger.set_debug_flags(main.DEBUG_FLAGS)
                logger.debug(flag, test_msg)
                
                found = any(test_msg in log for log in logger.LOG_BUFFER)
                self.assertFalse(found, f"Logger captured message even though flag was disabled: {flag}")

    def test_system_flag_override(self):
        """Verify that 'system' flag enables all logging."""
        main.DEBUG_FLAGS["system"] = True
        logger.set_debug_flags(main.DEBUG_FLAGS)
        
        for flag in main.DEBUG_FLAGS:
            if flag == "system": continue
            logger.LOG_BUFFER.clear()
            test_msg = f"SYSTEM_OVERRIDE_{flag.upper()}"
            logger.debug(flag, test_msg)
            
            found = any(test_msg in log for log in logger.LOG_BUFFER)
            self.assertTrue(found, f"System flag did not override flag: {flag}")

if __name__ == '__main__':
    unittest.main()
