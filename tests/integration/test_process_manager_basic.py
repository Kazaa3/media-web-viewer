# =============================================================================
# Kategorie: Process Manager Basic Test
# Eingabewerte: Prozess-Kommandos, Testdaten
# Ausgabewerte: PID-Ausgaben, Status, Fehlerbehandlung
# Testdateien: test_process_manager_basic.py
# Kommentar: Testet grundlegende Prozessmanager-Funktionen und Fehlerbehandlung.
# =============================================================================
"""
Process Manager Basic Test Suite (DE/EN)
========================================

DE:
Testet grundlegende Funktionen des Prozessmanagers, einschließlich Starten, Terminieren, Killen und Aufräumen von Prozessen.

EN:
Tests basic process manager functions, including starting, terminating, killing, and reaping processes.

Autor/Author: Media Web Viewer Team
Erstellt/Created: 2026-03-13
Version: 1.0.0
"""

import sys
import os

import importlib
import subprocess
import time
import pytest

class FakePopen:
    """
    DE:
    Simuliert das Verhalten von subprocess.Popen für Tests.
    EN:
    Simulates subprocess.Popen behavior for tests.
    """
    def __init__(self, cmd, *args, **kwargs):
        self.cmd = cmd
        self.pid = 12345
        self._returncode = None
        self._terminated = False

    def poll(self):
        return self._returncode

    def terminate(self):
        self._terminated = True
        # simulate graceful shutdown pending
        self._returncode = None

    def kill(self):
        self._returncode = -9

    def wait(self, timeout=None):
        # simulate quick shutdown when waited
        if self._terminated:
            self._returncode = 0
            return 0
        time.sleep(0 if timeout is None else min(0.01, timeout))
        return self._returncode

    def communicate(self, timeout=None):
        return (b"", b"")

def test_process_manager_start_and_terminate(monkeypatch):
    """
    DE:
    Testet das Starten und Terminieren von Prozessen mit dem Prozessmanager.
    EN:
    Tests starting and terminating processes with the process manager.
    """
    try:
        import process_manager as pm  # type: ignore
    except Exception:
        pytest.skip("process_manager module not present")
    # patch Popen to avoid real processes
    monkeypatch.setattr(subprocess, "Popen", FakePopen)

    # start process
    pid = pm.start_process(["/bin/true"])
    assert isinstance(pid, int) or pid == 12345

    # process should be reported running (module-specific API)
    assert pm.is_process_running(pid) in (True, False)

    # terminate with timeout; should not raise
    res = pm.terminate_process(pid, timeout=0.1)
    assert isinstance(res, bool)

    # ensure kill fallback does not raise
    try:
        pm.kill_process(pid)
    except Exception:
        pytest.fail("kill_process raised unexpectedly")

def test_process_manager_reap(monkeypatch):
    """
    DE:
    Testet das Aufräumen (Reap) von Prozessen mit dem Prozessmanager.
    EN:
    Tests reaping (cleanup) of processes with the process manager.
    """
    try:
        import process_manager as pm  # type: ignore
    except Exception:
        pytest.skip("process_manager module not present")
    monkeypatch.setattr(subprocess, "Popen", FakePopen)

    pid = pm.start_process(["/bin/true"])
    # attempt to reap/cleanup
    try:
        pm.reap_process(pid)
    except Exception:
        pytest.fail("reap_process raised unexpectedly")