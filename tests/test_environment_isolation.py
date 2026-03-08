#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Tests for Environment Isolation and Hygiene.
"""

import unittest
import sys
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import env_handler

class TestEnvironmentIsolation(unittest.TestCase):
    def setUp(self):
        self.manager = env_handler.EnvironmentManager()

    def test_fingerprint_generation(self):
        """Verifies that a valid fingerprint is generated."""
        fingerprint = self.manager.get_environment_fingerprint()
        self.assertIsInstance(fingerprint, str)
        self.assertGreater(len(fingerprint), 0)
        if fingerprint != "unknown":
            self.assertEqual(len(fingerprint), 12)

    @patch('sys.prefix', '/wrong/path')
    @patch('sys.base_prefix', '/base/path')
    @patch.dict(os.environ, {}, clear=True)
    def test_non_exclusive_venv_detection(self):
        """Verifies that a non-project venv is detected as non-exclusive."""
        self.assertFalse(self.manager.is_exclusive_venv())

    @patch('sys.prefix', '/tmp/.venv')
    @patch('sys.base_prefix', '/base/path')
    def test_exclusive_venv_detection(self):
        """Verifies that the project's .venv is detected as exclusive."""
        # Set the manager's venv_path to match sys.prefix
        self.manager.venv_path = Path('/tmp/.venv')
        self.assertTrue(self.manager.is_exclusive_venv())

    def test_dependency_verification_all_present(self):
        """Verifies that no errors are returned if all critical dependencies are present."""
        # Mock importlib.metadata.version to always return a version
        with patch('importlib.metadata.version', return_value="1.0.0"):
            errors = self.manager.verify_dependencies()
            self.assertEqual(len(errors), 0)

    def test_dependency_verification_missing(self):
        """Verifies that errors are returned if a critical dependency is missing."""
        from importlib.metadata import PackageNotFoundError
        with patch('importlib.metadata.version', side_effect=PackageNotFoundError):
            errors = self.manager.verify_dependencies()
            self.assertGreater(len(errors), 0)
            self.assertTrue(any("Missing critical dependency" in err for err in errors))

if __name__ == '__main__':
    unittest.main()
