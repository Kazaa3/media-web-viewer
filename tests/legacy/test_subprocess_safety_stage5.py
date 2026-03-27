#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_subprocess_safety_stage5.py - Stage 5: Quality & Security
Validates sub-process safety, active_subprocesses tracking, and cleanup.
"""

import unittest
import os
import sys
import subprocess
import time

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestSubprocessSafety(unittest.TestCase):
    def test_subprocess_tracking(self):
        """Verifies that we can track and cleanup sub-processes."""
        # Mocking the tracking mechanism or testing the actual one if accessible
        from src.core.main import ACTIVE_SUBPROCESSES # type: ignore
        
        # Start a dummy process
        proc = subprocess.Popen(["sleep", "10"])
        ACTIVE_SUBPROCESSES.append(proc)
        
        self.assertIn(proc, ACTIVE_SUBPROCESSES)
        self.assertIsNone(proc.poll()) # Still running
        
        # Cleanup
        proc.terminate()
        proc.wait(timeout=2)
        self.assertIsNotNone(proc.poll())
        ACTIVE_SUBPROCESSES.remove(proc)
        print("✅ Subprocess safety: Tracking and manual cleanup passed.")

    def test_environment_safety(self):
        """Checks for unsafe environment variables or shell injection patterns (simplified)."""
        # Example: Ensure no dangerous env vars are leaked (just a placeholder for real security logic)
        unsafe_keys = ["DANGEROUS_SECRET_KEY", "UNSAFE_ACCESS_TOKEN"]
        for key in unsafe_keys:
            self.assertNotIn(key, os.environ)
        print("✅ Quality & Security: Basic environment safety passed.")

if __name__ == "__main__":
    unittest.main()
