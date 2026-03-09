#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Debug / HTML Instrumentation
# Eingabewerte: web/app.html, packaging/opt/media-web-viewer/web/app.html
# Ausgabewerte: Validierung, dass Debug-Logs in loadEnvironmentInfo injiziert werden können
# Testdateien: web/app.html, packaging/opt/media-web-viewer/web/app.html
# Kommentar: Dauerhafter Test für reproduzierbare Debug-Instrumentierung der HTML-UI.

import unittest
from pathlib import Path


DEBUG_SNIPPET = """
                console.log('[DEBUG] loadEnvironmentInfo: Starting...');
                console.log('[DEBUG] loadEnvironmentInfo: Received info:', info);
                console.log('[DEBUG] installed_packages type:', typeof info?.installed_packages, 'isArray:', Array.isArray(info?.installed_packages));
                console.log('[DEBUG] installed_packages length:', info?.installed_packages?.length);
""".strip("\n")


def inject_debug_logs_into_html(html_text: str) -> str:
    """Inject debug logs into loadEnvironmentInfo() in an idempotent way."""
    anchor = "                let info = await eel.get_environment_info()();"
    if anchor not in html_text:
        return html_text

    if "[DEBUG] loadEnvironmentInfo: Starting..." in html_text:
        return html_text

    return html_text.replace(anchor, f"{anchor}\n{DEBUG_SNIPPET}", 1)


class TestHtmlDebugLogInjection(unittest.TestCase):
    """Tests that debug instrumentation can be inserted into both UI HTML files safely."""

    def setUp(self):
        self.root = Path(__file__).parent.parent
        self.app_html_path = self.root / "web" / "app.html"
        self.packaging_app_html_path = self.root / "packaging" / "opt" / "media-web-viewer" / "web" / "app.html"
        self.app_html = self.app_html_path.read_text(encoding="utf-8")
        self.packaging_app_html = self.packaging_app_html_path.read_text(encoding="utf-8")

    def test_injects_debug_logs_after_eel_call(self):
        """Injection should place debug logs directly after eel response assignment."""
        injected = inject_debug_logs_into_html(self.app_html)

        self.assertIn("[DEBUG] loadEnvironmentInfo: Starting...", injected)
        self.assertIn("[DEBUG] installed_packages length:", injected)

        anchor_index = injected.find("let info = await eel.get_environment_info()();")
        debug_index = injected.find("[DEBUG] loadEnvironmentInfo: Starting...")
        self.assertGreater(debug_index, anchor_index)

    def test_injection_is_idempotent(self):
        """Running injection multiple times must not duplicate log lines."""
        once = inject_debug_logs_into_html(self.app_html)
        twice = inject_debug_logs_into_html(once)

        self.assertEqual(
            once.count("[DEBUG] loadEnvironmentInfo: Starting..."),
            1,
            "Debug marker should exist exactly once after first injection",
        )
        self.assertEqual(
            twice.count("[DEBUG] loadEnvironmentInfo: Starting..."),
            1,
            "Debug marker should still exist exactly once after second injection",
        )

    def test_injection_works_for_packaging_html(self):
        """Injection should also work for packaged app.html copy."""
        injected = inject_debug_logs_into_html(self.packaging_app_html)

        self.assertIn("[DEBUG] loadEnvironmentInfo: Starting...", injected)
        self.assertIn("[DEBUG] installed_packages length:", injected)

    def test_injection_is_idempotent_for_packaging_html(self):
        """Running injection multiple times must not duplicate log lines in packaging HTML."""
        once = inject_debug_logs_into_html(self.packaging_app_html)
        twice = inject_debug_logs_into_html(once)

        self.assertEqual(
            once.count("[DEBUG] loadEnvironmentInfo: Starting..."),
            1,
            "Debug marker should exist exactly once after first injection (packaging)",
        )
        self.assertEqual(
            twice.count("[DEBUG] loadEnvironmentInfo: Starting..."),
            1,
            "Debug marker should still exist exactly once after second injection (packaging)",
        )

    def test_optionally_apply_debug_injection_to_file(self):
        """
        Optional integration mode: writes debug logs into real app.html targets if explicitly requested.

        Activate with environment variable:
            MWV_APPLY_HTML_DEBUG_INJECTION=1
        """
        import os

        if os.environ.get("MWV_APPLY_HTML_DEBUG_INJECTION") != "1":
            self.skipTest("Set MWV_APPLY_HTML_DEBUG_INJECTION=1 to apply injection to web/app.html")

        original_main = self.app_html_path.read_text(encoding="utf-8")
        original_packaging = self.packaging_app_html_path.read_text(encoding="utf-8")
        try:
            injected_main = inject_debug_logs_into_html(original_main)
            injected_packaging = inject_debug_logs_into_html(original_packaging)

            self.app_html_path.write_text(injected_main, encoding="utf-8")
            self.packaging_app_html_path.write_text(injected_packaging, encoding="utf-8")

            updated_main = self.app_html_path.read_text(encoding="utf-8")
            updated_packaging = self.packaging_app_html_path.read_text(encoding="utf-8")
            self.assertIn("[DEBUG] loadEnvironmentInfo: Starting...", updated_main)
            self.assertIn("[DEBUG] loadEnvironmentInfo: Starting...", updated_packaging)
        finally:
            # Keep repository clean after optional write-mode test
            self.app_html_path.write_text(original_main, encoding="utf-8")
            self.packaging_app_html_path.write_text(original_packaging, encoding="utf-8")


if __name__ == "__main__":
    unittest.main()
