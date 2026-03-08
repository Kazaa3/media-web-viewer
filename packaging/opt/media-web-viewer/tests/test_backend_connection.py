import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Ensure project root is in path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import main

class TestBackendConnection(unittest.TestCase):
    """
    @test Verify the backend's responsiveness.
    @details Confirms that the exposed ping function returns the expected response.
    """

    def test_ping_response(self):
        """
        @test Verify the backend's ping function.
        @details Ensures that main.ping() returns {'status': 'ok', 'message': 'pong'}.
        """
        # We need to make sure ping exists in main.py
        if hasattr(main, 'ping'):
            response = main.ping()
            self.assertEqual(response.get('status'), 'ok')
            self.assertEqual(response.get('message'), 'pong')
        else:
            self.fail("main.py does not have a ping function yet.")

if __name__ == '__main__':
    print("Running Backend Connection Tests...")
    unittest.main()
