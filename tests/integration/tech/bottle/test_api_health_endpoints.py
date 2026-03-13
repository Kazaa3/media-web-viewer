#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Tech / Bottle
# Eingabewerte: Bottle app instance, gevent-websocket
# Ausgabewerte: Server status (shape), WebSocket health (ping/pong)
# Testdateien: src/core/main.py, src/core/env_handler.py
# ERWEITERUNGEN (TODO): [ ] Integrationstests erweitern, [ ] Performance-Messung WebSocket
# KOMMENTAR: Prüft die API-Endpunkte auf Verfügbarkeit und WebSocket-Funktionalität.
# VERWENDUNG: pytest tests/integration/tech/bottle/test_api_health_endpoints.py

"""
KATEGORIE:
----------
Tech / Bottle

ZWECK:
------
Validiert API-Health-Endprodukte und WebSocket-Status-Verbindungen.
Prüft Bottle App Endpunkte und die WebSocket-Interaktion.

EINGABEWERTE:
-------------
- Bottle app instance
- gevent-websocket

AUSGABEWERTE:
-------------
- Server status (shape)
- WebSocket health (ping/pong)

TESTDATEIEN:
------------
- src/core/main.py
- src/core/env_handler.py

ERWEITERUNGEN (TODO):
---------------------
- [ ] Integrationstests erweitern
- [ ] Performance-Messung WebSocket

VERWENDUNG:
-----------
    pytest tests/integration/tech/bottle/test_api_health_endpoints.py
"""

import importlib
import pytest

def test_get_server_status_shape():
    try:
        import src.core.main as m  # type: ignore
    except Exception:
        pytest.skip("main not importable")
    assert hasattr(m, "get_server_status") and callable(m.get_server_status)
    status = m.get_server_status()
    assert isinstance(status, dict)
    # expected keys (must be non-breaking)
    for k in ("runtime", "ws_backend", "tools", "pid"):
        assert k in status

@pytest.mark.integration
def test_bottle_ws_health_endpoint_integration():
    # integration test (backend-only) — gated by ENABLE_INTEGRATION in CI
    import os
    if os.environ.get("ENABLE_INTEGRATION") != "1":
        pytest.skip("integration disabled")
    try:
        import src.core.env_handler as eh  # type: ignore
        importlib.reload(eh)
        from bottle import Bottle
        from gevent.pywsgi import WSGIServer
        from geventwebsocket.handler import WebSocketHandler
        import websocket
    except Exception:
        pytest.skip("integration deps missing")
    app = Bottle()
    eh.register_ws_health_route(app)
    server = WSGIServer(("127.0.0.1", 8766), app, handler_class=WebSocketHandler)
    server.start()
    import time, websocket as wsclient
    time.sleep(0.3)
    ws = wsclient.create_connection("ws://127.0.0.1:8766/ws-health", timeout=5)
    msg = ws.recv()
    assert msg == "ping"
    ws.send("pong")
    ok = ws.recv()
    assert ok == "ok"
    ws.close()
    server.stop()
    server.close()