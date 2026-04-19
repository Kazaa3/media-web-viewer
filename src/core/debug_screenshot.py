import pyautogui
import os
import sys

try:
    print(f"DISPLAY: {os.environ.get('DISPLAY')}")
    # Try a simple screenshot
    pyautogui.screenshot("debug_test.png")
    print("SUCCESS: Screenshot saved as debug_test.png")
except Exception as e:
    print(f"FAILED: {e}")
    import traceback
    traceback.print_exc()
