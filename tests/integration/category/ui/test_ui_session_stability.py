#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: UI Session Stability
# Eingabewerte: main.py, web/app.html
# Ausgabewerte: Validierte Schutzmechanismen gegen Session-Abbruch und Doppel-Launch
# Testdateien: main.py, web/app.html
# Kommentar: Regression-Tests für Test-Tab-Sprung, unload/SystemExit und doppelte Fenster-Launches.

import unittest
from pathlib import Path

class TestUiSessionStability(unittest.TestCase):
    """Regression tests for UI session stability and duplicate window risks."""

    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).parents[3]
        cls.main_py = (cls.root / "src/core/main.py").read_text(encoding="utf-8")
        cls.app_html = (cls.root / "web" / "app.html").read_text(encoding="utf-8")

    def test_keepalive_catches_baseexception(self):
        """Keepalive loop must recover from unload-triggered SystemExit/BaseException."""
        self.assertIn("while True:", self.main_py)
        self.assertIn("eel.sleep(1.0)", self.main_py)
        self.assertIn("except BaseException as e:", self.main_py)
        self.assertIn("keepalive recovered from base error", self.main_py)

    def test_browser_launch_has_single_popen_site(self):
        """Startup should only contain one explicit browser Popen launch site."""
        popen_count = self.main_py.count("subprocess.Popen([")
        self.assertEqual(
            popen_count,
            1,
            f"Expected exactly 1 browser Popen launch site, found {popen_count}"
        )

    def test_eel_start_disables_auto_browser_launch(self):
        """Eel auto browser launch must be disabled to avoid duplicate windows."""
        self.assertIn('eel.start("app.html", mode=False', self.main_py)

    def test_startup_has_existing_session_guard(self):
        """Startup must guard against launching a second app window/session."""
        self.assertIn("existing_sessions = [s for s in check_running_sessions() if s.get('port')]", self.main_py)
        self.assertIn("Skipping new window launch.", self.main_py)
        self.assertIn("if is_session_url_reachable(existing_url, timeout=0.8):", self.main_py)
        self.assertIn("open_session_url(existing_url)", self.main_py)
        self.assertIn("Ignoring stale session candidate", self.main_py)

    def test_ui_test_runs_disable_browser_open_side_effects(self):
        """UI-triggered pytest subprocess must suppress browser.open side effects."""
        self.assertIn('env["MWV_DISABLE_BROWSER_OPEN"] = "1"', self.main_py)
        self.assertIn('if os.environ.get("MWV_DISABLE_BROWSER_OPEN") == "1":', self.main_py)

    def test_interactive_tests_not_auto_selected(self):
        """Interactive/browser tests should be unchecked by default in Test tab."""
        self.assertIn("const isInteractiveBrowserTest = (suiteId)", self.app_html)
        self.assertIn("const checkedAttr = isInteractiveBrowserTest(suite.id) ? '' : 'checked';", self.app_html)

    def test_live_test_output_bridge_exposed(self):
        """Frontend must expose append_test_output for real-time test output streaming."""
        self.assertIn("eel.expose(append_test_output);", self.app_html)
        self.assertIn("function append_test_output(message)", self.app_html)

    def test_ui_trace_bridged_to_backend_logs(self):
        """UI trace must be forwarded from frontend to backend terminal logs."""
        self.assertIn("@eel.expose\ndef ui_trace(message):", self.main_py)
        self.assertIn("eel.ui_trace(line)()", self.app_html)

    def test_run_selected_tests_has_reentry_guard(self):
        """Test runner UI must prevent concurrent double-click runs."""
        self.assertIn("let isTestRunInProgress = false;", self.app_html)
        self.assertIn("if (isTestRunInProgress)", self.app_html)
        self.assertIn("run-selected-tests-btn", self.app_html)

if __name__ == "__main__":
    unittest.main(verbosity=2)
