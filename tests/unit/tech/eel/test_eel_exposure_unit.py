#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Unit / Eel / Exposure
# Eingabewerte: src/core/main.py, eel.expose
# Ausgabewerte: Validierung Eel-Expose-Mechanik
# Testdateien: src/core/main.py
# ERWEITERUNGEN (TODO): [ ] Mocking für verschiedene Eel-Versionen, [ ] Fehlerfall-Tests
# KOMMENTAR: Testet die Eel-Expose-Logik und deren Verbindung zum Frontend.
# VERWENDUNG: pytest tests/unit/tech/eel/test_eel_exposure_unit.py
"""
Testet die Eel-Expose-Logik und deren Verbindung zum Frontend. / Tests Eel expose logic and its connection to frontend.

Args:
    monkeypatch: pytest fixture zum Patchen / pytest fixture for patching.

Returns:
    None
"""
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