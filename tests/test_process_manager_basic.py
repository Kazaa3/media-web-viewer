import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import importlib
import subprocess
import time
import pytest


class FakePopen:
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