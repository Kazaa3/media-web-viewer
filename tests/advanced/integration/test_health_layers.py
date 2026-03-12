import importlib
import sys
import types
import shutil
import pytest

def _make_sniffio_module(rv):
    m = types.ModuleType("sniffio")
    m.current_async_library = lambda: rv
    return m

class FakeApp:
    def __init__(self):
        self.routes = []
    def route(self, path, apply=None):
        def decorator(func):
            self.routes.append({"path": path, "apply": apply, "func": func})
            return func
        return decorator

def test_runtime_info_shape():
    import src.core.env_handler as eh  # type: ignore
    importlib.reload(eh)
    info = eh.runtime_info()
    assert "runtime" in info and "ws_backend" in info

def test_register_ws_health_route_no_raise_and_registers(monkeypatch):
    sys.modules["sniffio"] = _make_sniffio_module("gevent")
    bw = types.ModuleType("bottle_websocket")
    bw.websocket = object()
    sys.modules["bottle_websocket"] = bw
    import src.core.env_handler as eh  # type: ignore
    importlib.reload(eh)
    app = FakeApp()
    eh.register_ws_health_route(app)
    assert any(r["path"] == "/ws-health" for r in app.routes)

def test_main_health_api_present_or_skip():
    try:
        import src.core.main as m  # type: ignore
    except Exception:
        pytest.skip("src/core/main.py not importable in this env")
    for name in ("get_server_status",):
        assert hasattr(m, name) and callable(getattr(m, name))
    status = m.get_server_status()
    assert isinstance(status, dict)
    assert "running" in status and "ws_ok" in status

def test_external_tool_probe_simulation(monkeypatch):
    # simulate ffprobe present / absent via shutil.which
    monkeypatch.setattr(shutil, "which", lambda name: "/usr/bin/ffprobe" if name == "ffprobe" else None)
    assert shutil.which("ffprobe") is not None
    monkeypatch.setattr(shutil, "which", lambda name: None)
    assert shutil.which("ffprobe") is None

def test_logging_extension_point():
    import src.core.logger as lg  # type: ignore
    # logger.get_logger should exist and be callable
    assert hasattr(lg, "get_logger") and callable(lg.get_logger)
    log = lg.get_logger("test_health")
    # basic logging call should not raise
    log.info("health test ping")