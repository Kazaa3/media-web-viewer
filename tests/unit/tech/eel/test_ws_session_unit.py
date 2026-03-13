#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Unit / Eel / WebSocket
# Eingabewerte: src/core/env_handler.py, bottle_websocket, sniffio
# Ausgabewerte: Validierung WebSocket-Health-Handler
# Testdateien: src/core/env_handler.py
# ERWEITERUNGEN (TODO): [ ] Mocking für verschiedene WS-Backends, [ ] Timeout-Tests
# KOMMENTAR: Testet die Registrierung und Funktion des WebSocket-Health-Handlers.
# VERWENDUNG: pytest tests/unit/tech/eel/test_ws_session_unit.py
import importlib
import sys
import types

import pytest

def _make_sniffio_module(rv):
    m = types.ModuleType("sniffio")
    m.current_async_library = lambda: rv
    return m

class _FakeWS:
    def __init__(self, recv_value="pong"):
        self.sent = []
        self._recv = recv_value

    def send(self, msg):
        self.sent.append(msg)

    def receive(self, timeout=None):
        return self._recv

def test_ws_health_handler_registers_and_handles_ping(monkeypatch):
    """
    Testet die Registrierung und Funktion des WebSocket-Health-Handlers. / Tests registration and function of WebSocket health handler.

    Args:
        monkeypatch: pytest fixture zum Patchen / pytest fixture for patching.

    Returns:
        None
    """
    sys.modules["sniffio"] = _make_sniffio_module("gevent")
    bw = types.ModuleType("bottle_websocket")
    bw.websocket = object()
    sys.modules["bottle_websocket"] = bw

    import src.core.env_handler as eh  # type: ignore
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
    eh.register_ws_health_route(app)

    # find registered handler
    handlers = [r for r in app.routes if r["path"] == "/ws-health"]
    assert handlers, "ws-health not registered"
    handler = handlers[0]["func"]

    # call handler with fake websocket that returns "pong"
    fake_ws = _FakeWS(recv_value="pong")
    handler(fake_ws)
    assert fake_ws.sent[0] == "ping"
    assert "ok" in fake_ws.sent