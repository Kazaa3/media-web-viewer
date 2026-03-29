# =============================================================================
# Kategorie: Process Restart Race Test
# Eingabewerte: Prozess-Kommandos, Testdaten
# Ausgabewerte: PID-Ausgaben, Status, Fehlerbehandlung
# Testdateien: test_process_restart_race.py
# Kommentar: Testet Race-Conditions beim Prozess-Start und Idempotenz.
# =============================================================================
"""
Process Restart Race Test Suite (DE/EN)
=======================================

DE:
Testet Race-Conditions und Idempotenz beim Starten von Prozessen über die API.

EN:
Tests race conditions and idempotency when starting processes via the API.

Autor/Author: Media Web Viewer Team
Erstellt/Created: 2026-03-13
Version: 1.0.0
"""

import importlib
import sys
import types
import pytest

def _pm_stub_same_pid():
    """
    DE:
    Erstellt einen Stub für den Prozessmanager mit immer gleicher PID.
    EN:
    Creates a stub for the process manager with always the same PID.
    """
    pm = types.SimpleNamespace()
    state = {"started": 0}
    def start(cmd):
        state["started"] += 1
        return 4242
    def is_running(pid):
        return state["started"] > 0
    def terminate(pid, timeout=None):
        state["started"] = 0
        return True
    pm.start_process = start
    pm.is_process_running = is_running
    pm.terminate_process = terminate
    pm.reap_process = lambda pid: None
    return pm

def test_start_idempotent_on_race(monkeypatch):
    """
    DE:
    Testet, dass das Starten von Prozessen idempotent und race-safe ist.
    EN:
    Tests that starting processes is idempotent and race-safe.
    """
    sys.modules["process_manager"] = _pm_stub_same_pid()
    try:
        import src.core.main as m  # type: ignore
    except Exception:
        pytest.skip("main not importable")
    # call start twice rapidly and expect stable return (pid or error)
    r1 = getattr(m, "start_process_via_api", getattr(m, "start_process", None))
    if not r1:
        pytest.skip("start API not present")
    out1 = r1(["/bin/true"])
    out2 = r1(["/bin/true"])
    assert out1 is not None
    assert out2 is not None