import sys
import os
import unittest
from unittest.mock import patch

# Füge das Hauptverzeichnis zum Pfad hinzu, um main importieren zu können
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import main
import logger

class TestCLIArgs(unittest.TestCase):
    def setUp(self):
        # Reset DEBUG_FLAGS to False before each test
        for key in main.DEBUG_FLAGS:
            main.DEBUG_FLAGS[key] = False

    def test_debug_flag_enables_all(self):
        """Verifies that --debug flag enables all DEBUG_FLAGS."""
        test_args = ["main.py", "--debug"]
        
        # Call the refactored initialization function
        main.initialize_debug_flags(test_args)
        
        # Verify all flags are True
        for key, value in main.DEBUG_FLAGS.items():
            self.assertTrue(value, f"Flag {key} should be True when --debug is passed")

    def test_no_debug_flag_leaves_defaults(self):
        """Verifies that without --debug, flags remain False (default)."""
        test_args = ["main.py"]
        
        main.initialize_debug_flags(test_args)
        
        # Verify all flags are False
        for key, value in main.DEBUG_FLAGS.items():
            self.assertFalse(value, f"Flag {key} should be False by default")

if __name__ == "__main__":
    unittest.main()
