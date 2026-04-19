import sys
from unittest.mock import MagicMock

# Mocking tkinter to bypass MouseInfo dependency error on Linux (v1.46.142 Workaround)
mock_tk = MagicMock()
sys.modules["tkinter"] = mock_tk
sys.modules["tkinter.messagebox"] = MagicMock()

import pyautogui
import os

try:
    print(f"DISPLAY: {os.environ.get('DISPLAY')}")
    # Try a simple screenshot using the mock
    pyautogui.screenshot("debug_mock_test.png")
    print("SUCCESS: Screenshot saved as debug_mock_test.png")
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()
