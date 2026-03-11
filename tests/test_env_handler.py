import os
import sys
import unittest
from pathlib import Path

# Add project root to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from env_handler import EnvironmentManager

class TestEnvironmentManager(unittest.TestCase):
    def setUp(self):
        self.manager = EnvironmentManager()

    def test_is_conda(self):
        # Test that is_conda returns a boolean
        self.assertIsInstance(self.manager.is_conda(), bool)

    def test_is_exclusive_venv(self):
        # Test that is_exclusive_venv returns a boolean
        self.assertIsInstance(self.manager.is_exclusive_venv(), bool)

    def test_get_environment_fingerprint(self):
        # Test that fingerprint is a string
        fingerprint = self.manager.get_environment_fingerprint()
        self.assertIsInstance(fingerprint, str)
        self.assertTrue(len(fingerprint) > 0)

    def test_get_missing_info(self):
        # Test that get_missing_info returns three lists
        missing_pip, missing_apt, missing_conda = self.manager.get_missing_info()
        self.assertIsInstance(missing_pip, list)
        self.assertIsInstance(missing_apt, list)
        self.assertIsInstance(missing_conda, list)

    def test_verify_dependencies(self):
        # Test that verify_dependencies returns a list
        errors = self.manager.verify_dependencies()
        self.assertIsInstance(errors, list)

if __name__ == '__main__':
    unittest.main()
