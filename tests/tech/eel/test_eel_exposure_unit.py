import importlib
import sys

import pytest

def test_eel_api_functions_present():
    try:
        import src.core.main as m  # type: ignore
    except Exception:
        pytest.skip("main module not importable")
    # check presence of key API functions expected to be exposed to frontend
    for name in ("get_server_status", "handle_click", "handle_click_batch", "api_extract_metadata"):
        assert hasattr(m, name), f"{name} missing in main.py"
        assert callable(getattr(m, name))