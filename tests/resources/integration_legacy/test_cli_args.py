#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Kategorie: CLI Arguments Test
# Eingabewerte: Command-line arguments
# Ausgabewerte: Argument parsing results
# Testdateien: test_cli_args.py
# Kommentar: Testet CLI-Argument-Parsing.
# Startbefehl: python tests/test_cli_args.py
# =============================================================================
"""
CLI Arguments Test Suite (DE/EN)
=================================

DE:
Testet das Parsing von CLI-Argumenten und die Initialisierung von Debug-Flags.

EN:
Tests CLI argument parsing and initialization of debug flags.

Autor/Author: Media Web Viewer Team
Erstellt/Created: 2026-03-13
Version: 1.0.0
"""

import sys
import os
import unittest
from unittest.mock import patch

# Füge das Hauptverzeichnis zum Pfad hinzu, um main importieren zu können

import src.core.main as main
import src.core.logger as logger

class TestCLIArgs(unittest.TestCase):
    """
    DE:
    Testet das Verhalten der Debug-Flags bei verschiedenen CLI-Argumenten.

    EN:
    Tests debug flag behavior for different CLI arguments.
    """
    def setUp(self):
        """
        DE:
        Setzt alle Debug-Flags vor jedem Test auf False.

        EN:
        Resets all debug flags to False before each test.
        """
        # Reset DEBUG_FLAGS to False before each test
        for key in main.DEBUG_FLAGS:
            main.DEBUG_FLAGS[key] = False

    def test_debug_flag_enables_all(self):
        """
        DE:
        Testet, ob --debug alle Debug-Flags aktiviert.

        EN:
        Tests if --debug enables all debug flags.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn ein Flag nicht aktiviert ist.
        """
        test_args = ["src/core/main.py", "--debug"]
        
        # Call the refactored initialization function
        main.initialize_debug_flags(test_args)
        
        # Verify all flags are True
        for key, value in main.DEBUG_FLAGS.items():
            self.assertTrue(value, f"Flag {key} should be True when --debug is passed")

    def test_no_debug_flag_leaves_defaults(self):
        """
        DE:
        Testet, ob ohne --debug alle Flags auf False bleiben.

        EN:
        Tests if all flags remain False without --debug.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn ein Flag nicht auf False bleibt.
        """
        test_args = ["src/core/main.py"]
        
        main.initialize_debug_flags(test_args)
        
        # Verify all flags are False
        for key, value in main.DEBUG_FLAGS.items():
            self.assertFalse(value, f"Flag {key} should be False by default")

if __name__ == "__main__":
    unittest.main()
