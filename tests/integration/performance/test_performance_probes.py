#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Performance Diagnostics Test
# Eingabewerte: main.py, web/app.html
# Ausgabewerte: Verfügbarkeit von Backend-/Frontend-Probes und Cache-Verhalten
# Testdateien: main.py, web/app.html
# Kommentar: Verifiziert getrennte Performance-Probes für Backend, Frontend und Eel-RTT.

import unittest
import time
from pathlib import Path

import src.core.main as main

class TestPerformanceProbes(unittest.TestCase):
    """Validates latency probe endpoints and frontend diagnostic hook."""

    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).parents[3]
        cls.app_html = (cls.root / "web" / "app.html").read_text(encoding="utf-8")

    def test_api_ping_shape_and_payload_size(self):
        """api_ping must return stable fields and respect payload_size."""
        result = main.api_ping(client_ts=123456, payload_size=128)
        self.assertEqual(result.get("status"), "ok")
        self.assertEqual(result.get("client_ts"), 123456)
        self.assertEqual(result.get("payload_size"), 128)
        self.assertEqual(len(result.get("payload", "")), 128)
        self.assertIsInstance(result.get("server_ts"), int)

    def test_api_ping_payload_size_clamped(self):
        """api_ping payload must be clamped to avoid excessive transfer size."""
        result = main.api_ping(client_ts=None, payload_size=999999)
        self.assertEqual(result.get("payload_size"), 200000)
        self.assertEqual(len(result.get("payload", "")), 200000)

    def test_get_environment_info_cached_second_call_is_not_slower(self):
        """Second call should benefit from warm state and not regress badly."""
        t1 = time.perf_counter()
        first = main.get_environment_info()
        d1 = time.perf_counter() - t1

        t2 = time.perf_counter()
        second = main.get_environment_info()
        d2 = time.perf_counter() - t2

        self.assertIsInstance(first, dict)
        self.assertIsInstance(second, dict)
        self.assertIn("installed_packages", first)
        self.assertIn("installed_packages", second)

        # Guard against obvious regressions while keeping test robust on slow systems.
        self.assertLessEqual(d2, d1 * 2.0 + 0.05)

    def test_frontend_latency_diagnostics_hook_exists(self):
        """Frontend must expose runLatencyDiagnostics for separate UI measurements."""
        self.assertIn("window.runLatencyDiagnostics = async function(payloadSize = 0, samples = 5)", self.app_html)
        self.assertIn("await eel.api_ping(Date.now(), size)();", self.app_html)
        self.assertIn("await fetch('/health', { cache: 'no-store' });", self.app_html)

if __name__ == "__main__":
    unittest.main(verbosity=2)
