import pytest


def test_pyautogui_import_and_api():
    try:
        import pyautogui
    except Exception:
        pytest.skip("pyautogui not installed")
    # Basic API presence checks — do not perform real GUI actions in unit tests
    assert hasattr(pyautogui, "click")
    assert hasattr(pyautogui, "write") or hasattr(pyautogui, "typewrite")
    assert hasattr(pyautogui, "FAILSAFE")
