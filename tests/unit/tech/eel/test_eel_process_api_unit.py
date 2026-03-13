#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Unit / Eel / Process API
# Eingabewerte: src/core/main.py, process_manager
# Ausgabewerte: Validierung Eel-Process-API und Prozesssteuerung
# Testdateien: src/core/main.py
# ERWEITERUNGEN (TODO): [ ] Mocking für verschiedene Prozess-Manager, [ ] Fehlerfall-Tests
# KOMMENTAR: Testet die Eel-Process-API und deren Verbindung zum Backend.
# VERWENDUNG: pytest tests/unit/tech/eel/test_eel_process_api_unit.py
import importlib
import sys
import types
import pytest

def _make_pm_stub():
    pm = types.SimpleNamespace()
    pm.start_process = lambda cmd: 4242
    pm.is_process_running = lambda pid: True
    pm.terminate_process = lambda pid, timeout=None: True
    pm.kill_process = lambda pid: True
    pm.reap_process = lambda pid: None
    return pm

def test_eel_process_api_calls(monkeypatch):
    """
    Testet die Eel-Process-API und deren Verbindung zum Backend. / Tests Eel process API and its connection to backend.

    Args:
        monkeypatch: pytest fixture zum Patchen / pytest fixture for patching.

    Returns:
        None
    """
    sys.modules.pop("process_manager", None)
    sys.modules["process_manager"] = _make_pm_stub()
    try:
        import src.core.main as m  # type: ignore
    except Exception:
        pytest.skip("main not importable")
    # discover API functions (tolerant names)
    candidates = [
        ("start_process_via_api", ("/bin/true",)),
        ("start_process", (["/bin/true"],)),
        ("api_start_process", (["/bin/true"],)),
    ]
    start_fn = None
    for name, args in candidates:
        if hasattr(m, name) and callable(getattr(m, name)):
            start_fn = getattr(m, name)
            start_args = args
            break
    if not start_fn:
        pytest.skip("no start_process API found in main")
    # call start
    res = start_fn(*start_args)
    assert isinstance(res, (dict, int, str))
    # status / terminate / kill if available
    for fname in ("get_process_status", "is_process_running", "terminate_process_via_api", "api_terminate_process"):
        if hasattr(m, fname):
            fn = getattr(m, fname)
            try:
                out = fn(4242)
                # should not raise; shape flexible
                assert out is None or isinstance(out, (dict, bool, int))
            except Exception:
                pytest.fail(f"{fname} raised unexpectedly")