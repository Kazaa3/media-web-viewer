#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_pyautogui_automation_stage4.py - Stage 4: E2E & Automation
Validates PyAutoGUI integration and screen hardware access.
"""

import unittest
import os
import sys

# Ensure project root is in path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestPyAutoGUI(unittest.TestCase):
    def test_hardware_access(self):
        """Verifies that pyautogui can access screen information."""
        try:
            import pyautogui
            size = pyautogui.size()
            self.assertGreater(size.width, 0)
            self.assertGreater(size.height, 0)
            
            pos = pyautogui.position()
            self.assertGreaterEqual(pos.x, 0)
            self.assertGreaterEqual(pos.y, 0)
            print(f"✅ PyAutoGUI: Screen {size.width}x{size.height}, Mouse at ({pos.x}, {pos.y})")
        except ImportError:
            self.skipTest("pyautogui not installed")
        except Exception as e:
            self.fail(f"PyAutoGUI hardware access failed: {e}")

if __name__ == "__main__":
    unittest.main()
