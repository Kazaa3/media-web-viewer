#!/usr/bin/env python3
"""
Test suite for sessionless mode (--n / --sessionless).

Category: Startup Modes
Status: Active
Version: 1.2.23

Validates the connectionless runtime mode that skips Eel/browser startup.

Test Suite Statistics:
- Total Test Classes: 2
- Total Test Cases: 6
- Focus Areas:
  1) CLI flag detection
  2) Sessionless runtime info contract
"""

import os
import sys
import unittest

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import main


class TestSessionlessFlagDetection(unittest.TestCase):
    """
    Tests: 4
    Focus: --n / --sessionless flag detection
    """

    def test_detects_short_flag(self):
        self.assertTrue(main.is_sessionless_mode(["python", "main.py", "--n"]))

    def test_detects_long_flag(self):
        self.assertTrue(main.is_sessionless_mode(["python", "main.py", "--sessionless"]))

    def test_returns_false_without_flag(self):
        self.assertFalse(main.is_sessionless_mode(["python", "main.py"]))

    def test_works_with_other_flags(self):
        self.assertTrue(main.is_sessionless_mode(["python", "main.py", "--debug", "--n"]))


class TestSessionlessRuntimeInfo(unittest.TestCase):
    """
    Tests: 2
    Focus: sessionless runtime information shape and values
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
        self.assertEqual(info["mode"], "sessionless")
        self.assertIsInstance(info["active_db"], str)
        self.assertIsInstance(info["total_items"], int)
        self.assertIsInstance(info["legacy_db_count"], int)
        self.assertIsInstance(info["scan_dirs"], list)


if __name__ == '__main__':
    print("=" * 70)
    print("SESSIONLESS MODE TEST SUITE")
    print("=" * 70)
    print("\nRunning --n / --sessionless tests...\n")
    unittest.main(verbosity=2)
