#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Bottle Transport Latency Test
# Eingabewerte: web/app_bottle.py health endpoint
# Ausgabewerte: HTTP 200 und lokale Roundtrip-Latenz (Median)
# Testdateien: web/app_bottle.py
# Kommentar: Separater Transporttest für Bottle-HTTP-Latenz.

import json
import socket
import threading
import time
import unittest
import urllib.request
from wsgiref.simple_server import make_server

import bottle
from web import app_bottle  # noqa: F401 (route registration side effect)

class TestBottleHealthLatency(unittest.TestCase):
    """Checks /health endpoint availability and local HTTP latency."""

    def _find_free_port(self) -> int:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(("127.0.0.1", 0))
            return int(s.getsockname()[1])

    def test_health_endpoint_roundtrip_latency(self):
        port = self._find_free_port()
        app = bottle.default_app()
        server = make_server("127.0.0.1", port, app)
        server.timeout = 0.2

        stop = threading.Event()

        def serve():
            while not stop.is_set():
                server.handle_request()

        thread = threading.Thread(target=serve, daemon=True)
        thread.start()

        try:
            latencies = []
            for _ in range(8):
                start = time.perf_counter()
                with urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=2.0) as response:
                    body = response.read().decode("utf-8")
                    data = json.loads(body)
                    self.assertEqual(response.status, 200)
                    self.assertEqual(data.get("status"), "ok")
                latencies.append((time.perf_counter() - start) * 1000.0)

            sorted_lat = sorted(latencies)
            median_ms = sorted_lat[len(sorted_lat) // 2]

            # Local loopback should remain clearly sub-second.
            self.assertLess(median_ms, 500.0)
        finally:
            stop.set()
            try:
                urllib.request.urlopen(f"http://127.0.0.1:{port}/health", timeout=1.0)
            except Exception:
                pass
            thread.join(timeout=2.0)
            server.server_close()

if __name__ == "__main__":
    unittest.main(verbosity=2)
