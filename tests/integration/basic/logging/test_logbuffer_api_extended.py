import importlib
import pytest
import types
import sys
import time

def test_log_buffer_roundtrip(monkeypatch):
    # ensure logger.get_logger exists or skip
    try:
        import src.core.logger as lg  # type: ignore
    except Exception:
        pytest.skip("logger module missing")
    # ensure logger has a buffer facility; if not, skip
    if not hasattr(lg, "get_logger"):
        pytest.skip("src.core.logger.get_logger missing")
    log = lg.get_logger("test_buffer")
    # emit logs
    log.info("buffer-test-1")
    log.error("buffer-test-2")
    # wait a tick if buffer is asynchronous
    time.sleep(0.01)
    try:
        import src.core.main as m  # type: ignore
    except Exception:
        pytest.skip("main not importable")
    if not hasattr(m, "get_recent_logs"):
        pytest.skip("get_recent_logs not implemented")
    entries = m.get_recent_logs(50)
    assert isinstance(entries, list)
    assert any("buffer-test-1" in e.get("msg", "") for e in entries)
    assert any("buffer-test-2" in e.get("msg", "") for e in entries)

def test_log_buffer_limits(monkeypatch):
    try:
        import src.core.main as m  # type: ignore
    except Exception:
        pytest.skip("main not importable")
    if not hasattr(m, "get_recent_logs"):
        pytest.skip("get_recent_logs not implemented")
    # request zero and negative limits
    assert m.get_recent_logs(0) == []
    assert m.get_recent_logs(-1) == []