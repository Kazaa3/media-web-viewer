#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Sessionless Mode Test
# Eingabewerte: --ng, --n flags
# Ausgabewerte: No-GUI mode validation
# Testdateien: Keine
# Kommentar: Testet Sessionless/No-GUI Mode.
#!/usr/bin/env python3
"""
Test suite for no-GUI and connectionless browser modes (--ng / --n).

Category: Startup Modes
Status: Active
Version: 1.2.23

Validates startup mode split:
- --ng: no GUI at all
- --n: browser UI without Eel/WebSocket backend

Test Suite Statistics:
- Total Test Classes: 2
- Total Test Cases: 10
- Focus Areas:
    1) CLI flag detection
    2) No-GUI runtime info contract
    3) Browser connectionless mode contract
"""

import os
import sys
import unittest

# Ensure project root is in path

import src.core.main as main

class TestSessionlessFlagDetection(unittest.TestCase):
    """
    Tests: 6
    Focus: --ng / --n / --sessionless flag detection
    """

    def test_detects_no_gui_short_flag(self):
        self.assertTrue(main.is_no_gui_mode(["python", "src.core.main.py", "--ng"]))

    def test_detects_no_gui_long_flag(self):
        self.assertTrue(main.is_no_gui_mode(["python", "src.core.main.py", "--sessionless"]))

    def test_no_gui_returns_false_without_flag(self):
        self.assertFalse(main.is_no_gui_mode(["python", "src.core.main.py"]))

    def test_detects_connectionless_browser_mode(self):
        self.assertTrue(main.is_connectionless_browser_mode(["python", "src.core.main.py", "--n"]))

    def test_connectionless_browser_returns_false_without_flag(self):
        self.assertFalse(main.is_connectionless_browser_mode(["python", "src.core.main.py"]))

    def test_no_gui_and_n_are_distinct(self):
        self.assertFalse(main.is_no_gui_mode(["python", "src.core.main.py", "--n"]))
        self.assertFalse(main.is_connectionless_browser_mode(["python", "src.core.main.py", "--ng"]))

class TestSessionlessRuntimeInfo(unittest.TestCase):
    """
    Tests: 2
    Focus: no-GUI runtime information shape and values
    """

    def test_run_sessionless_mode_returns_expected_keys(self):
        info = main.run_sessionless_mode()
        expected_keys = {
            "mode",
            "active_db",
            "total_items",
            "legacy_db_count",
            "scan_dirs",
        }
        self.assertTrue(expected_keys.issubset(set(info.keys())))

    def test_run_sessionless_mode_values_types(self):
        info = main.run_sessionless_mode()
        self.assertEqual(info["mode"], "no-gui")
        self.assertIsInstance(info["active_db"], str)
        self.assertIsInstance(info["total_items"], int)
        self.assertIsInstance(info["legacy_db_count"], int)
        self.assertIsInstance(info["scan_dirs"], list)

class TestConnectionlessBrowserRuntimeInfo(unittest.TestCase):
    """
    Tests: 2
    Focus: browser-based connectionless runtime info contract
    """

    def test_run_connectionless_browser_mode_returns_expected_keys(self):
        from unittest.mock import patch

        with patch.object(main, "get_preferred_browser") as mock_browser_fn:
            mock_browser = mock_browser_fn.return_value
            mock_browser.open.return_value = True
            info = main.run_connectionless_browser_mode()

        expected_keys = {
            "mode",
            "active_db",
            "total_items",
            "app_url",
            "scan_dirs",
        }
        self.assertTrue(expected_keys.issubset(set(info.keys())))

    def test_run_connectionless_browser_mode_values_types(self):
        from unittest.mock import patch

        with patch.object(main, "get_preferred_browser") as mock_browser_fn:
            mock_browser = mock_browser_fn.return_value
            mock_browser.open.return_value = True
            info = main.run_connectionless_browser_mode()

        self.assertEqual(info["mode"], "connectionless-browser")
        self.assertIsInstance(info["active_db"], str)
        self.assertIsInstance(info["total_items"], int)
        self.assertIsInstance(info["app_url"], str)
        self.assertTrue(info["app_url"].startswith("file://"))
        self.assertIsInstance(info["scan_dirs"], list)

if __name__ == '__main__':
    print("=" * 70)
    print("STARTUP MODES TEST SUITE")
    print("=" * 70)
    print("\nRunning --ng / --n mode tests...\n")
    unittest.main(verbosity=2)
