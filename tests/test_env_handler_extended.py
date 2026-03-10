import sys
import types
import importlib

import pytest


def _make_sniffio_module(return_value):
    m = types.ModuleType("sniffio")
    m.current_async_library = lambda: return_value
    return m


def test_detect_async_runtime_variants(monkeypatch):
    # gevent
    sys.modules["sniffio"] = _make_sniffio_module("gevent")
    import env_handler as eh  # type: ignore
    importlib.reload(eh)
    assert eh.detect_async_runtime() == "gevent"

    # trio
    sys.modules["sniffio"] = _make_sniffio_module("trio")
    importlib.reload(eh)
    assert eh.detect_async_runtime() == "trio"

    # asyncio
    sys.modules["sniffio"] = _make_sniffio_module("asyncio")
    importlib.reload(eh)
    assert eh.detect_async_runtime() == "asyncio"

    # missing
    sys.modules.pop("sniffio", None)
    importlib.reload(eh)
    assert eh.detect_async_runtime() in ("missing", "none")


def test_apply_gevent_monkey_patch_safe_with_and_without_gevent(monkeypatch):
    # ensure no exception when gevent not present
    sys.modules.pop("gevent", None)
    sys.modules.pop("gevent.monkey", None)
    import env_handler as eh  # type: ignore
    importlib.reload(eh)
    eh.apply_gevent_monkey_patch_safe()  # should not raise

    # simulate gevent.monkey.patch_all exists and is called
    gm = types.ModuleType("gevent.monkey")
    def _patch_all():
        setattr(gm, "patched_flag", True)
    gm.patch_all = _patch_all
    # ensure parent package present
    sys.modules["gevent"] = types.ModuleType("gevent")
    sys.modules["gevent.monkey"] = gm

    importlib.reload(eh)
    eh.apply_gevent_monkey_patch_safe()
    assert getattr(sys.modules["gevent.monkey"], "patched_flag", False) is True


def test_register_ws_health_route_gevent_registers(monkeypatch):
    # simulate sniffio -> gevent and bottle_websocket available
    sys.modules["sniffio"] = _make_sniffio_module("gevent")
    bw = types.ModuleType("bottle_websocket")
    # websocket can be any sentinel object used in apply list
    bw.websocket = object()
    sys.modules["bottle_websocket"] = bw

    import env_handler as eh  # type: ignore
    importlib.reload(eh)

    class FakeApp:
        def __init__(self):
            self.routes = []

        def route(self, path, apply=None):
            def decorator(func):
                self.routes.append({"path": path, "apply": apply, "func": func})
                return func
            return decorator

    app = FakeApp()
    # should register without raising
    eh.register_ws_health_route(app)
    assert any(r["path"] == "/ws-health" for r in app.routes)
    # verify apply contains the websocket sentinel
    assert any(bw.websocket in (r["apply"] or []) for r in app.routes)


def test_register_ws_health_route_noop_when_missing(monkeypatch):
    # no sniffio / no websocket libs -> no exception and no routes
    sys.modules.pop("sniffio", None)
    sys.modules.pop("bottle_websocket", None)
    import env_handler as eh  # type: ignore
    importlib.reload(eh)

    class FakeApp:
        def __init__(self):
            self.routes = []

        def route(self, path, apply=None):
            def decorator(func):
                self.routes.append({"path": path, "apply": apply, "func": func})
                return func
            return decorator

    app = FakeApp()
    eh.register_ws_health_route(app)  # should not raise
    assert app.routes == []