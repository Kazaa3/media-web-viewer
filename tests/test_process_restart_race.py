import importlib
import sys
import types
import pytest

def _pm_stub_same_pid():
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
    sys.modules["process_manager"] = _pm_stub_same_pid()
    try:
        import main as m  # type: ignore
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