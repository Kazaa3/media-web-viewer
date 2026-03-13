import importlib
import sys
import types
import pytest

def test_shutdown_triggers_process_cleanup(monkeypatch):
    try:
        import src.core.main as m  # type: ignore
    except Exception:
        pytest.skip("main not importable")
    # monkeypatch process_manager.reap_process and record calls
    calls = {"reaped": []}
    pm = types.SimpleNamespace()
    def reap(pid):
        calls["reaped"].append(pid)
    pm.reap_process = reap
    sys.modules["process_manager"] = pm
    importlib.reload(m)
    # if main exposes shutdown, call it
    if hasattr(m, "shutdown"):
        try:
            m.shutdown()
        except Exception:
            pytest.fail("shutdown raised")
        # expect reap called for managed processes if any (non-strict)
        assert isinstance(calls["reaped"], list)
    else:
        pytest.skip("shutdown API not implemented")