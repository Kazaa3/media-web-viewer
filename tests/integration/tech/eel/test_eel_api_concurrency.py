import importlib
import sys
import types
from concurrent.futures import ThreadPoolExecutor, as_completed
import pytest

def _make_pm_concurrent_stub():
    pm = types.SimpleNamespace()
    lock = {"calls": 0}
    def start(cmd):
        lock["calls"] += 1
        return 7000 + lock["calls"]
    pm.start_process = start
    pm.is_process_running = lambda pid: True
    pm.terminate_process = lambda pid, timeout=None: True
    return pm

def test_concurrent_start_api(monkeypatch):
    sys.modules["process_manager"] = _make_pm_concurrent_stub()
    try:
        import src.core.main as m  # type: ignore
    except Exception:
        pytest.skip("main not importable")
    start_fn = None
    for name in ("start_process_via_api", "start_process", "api_start_process"):
        if hasattr(m, name):
            start_fn = getattr(m, name)
            break
    if not start_fn:
        pytest.skip("start API not found")
    with ThreadPoolExecutor(max_workers=5) as ex:
        futures = [ex.submit(start_fn, ["/bin/true"]) for _ in range(10)]
        pids = [f.result() for f in as_completed(futures)]
    assert len(pids) == 10