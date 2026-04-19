import sys
from unittest.mock import MagicMock

# High-Fidelity Mocking of tkinter to bypass PyAutoGUI dependencies (v1.46.142 Workaround)
mock_tk = MagicMock()
mock_tk.TkVersion = 8.6
sys.modules["tkinter"] = mock_tk
sys.modules["tkinter.messagebox"] = MagicMock()

import pyautogui
import os

def take_screenshot():
    print("--- [Forensic Debug] Mocked PyAutoGUI Screenshot ---")
    try:
        # Use the real DISPLAY
        os.environ['DISPLAY'] = ':0'
        # PyAutoGUI.screenshot() should now use scrot internally
        pyautogui.screenshot("workstation_final_proof.png")
        if os.path.exists("workstation_final_proof.png"):
            print("SUCCESS: Screenshot captured in forensic proof mode.")
            return True
    except Exception as e:
        print(f"FAILED: {e}")
    return False

if __name__ == "__main__":
    take_screenshot()
