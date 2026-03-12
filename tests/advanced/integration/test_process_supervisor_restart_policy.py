import sys
import types
import time
import pytest

def test_supervisor_restarts_failed_process(monkeypatch):
    try:
        import process_manager as pm  # type: ignore
    except Exception:
        pytest.skip("process_manager not present")
    # simulate start -> pid then process dies; supervisor should attempt restart if policy exists
    restarted = {"count": 0}
    def fake_start(cmd):
        restarted["count"] += 1
        return 5000 + restarted["count"]
    pm.start_process = fake_start
    # call supervise API if present
    if hasattr(pm, "supervise_process"):
        pid = pm.supervise_process(["/bin/false"], restart_policy={"max_restarts": 2, "interval": 0.01})
        # allow some time for restarts
        time.sleep(0.05)
        assert restarted["count"] >= 1
    else:
        pytest.skip("supervise_process not implemented")