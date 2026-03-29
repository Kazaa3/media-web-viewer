# =============================================================================
# Kategorie: Startup Variants Test
# Eingabewerte: Startup-Flags, Session-Parameter
# Ausgabewerte: Startup-Verhalten, Session-Status
# Testdateien: test_startup_variants.py
# Kommentar: Testet verschiedene Startup-Varianten und Session-Management.
# Startbefehl: python tests/test_startup_variants.py
# =============================================================================
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Suite for Startup Variants and Session Management

Tests all startup modes:
- Normal mode (with Eel/WebSocket)
- No-GUI mode (--ng, --no-gui, --sessionless)
- Connectionless browser mode (--n)
- Session checking and conflict detection

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
"""

import unittest
import sys
import os
import socket
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add parent directory to path

import src.core.main as main

class TestStartupModeDetection(unittest.TestCase):
    """Test detection of various startup modes."""
    
    def test_no_gui_mode_with_ng_flag(self):
        """Test that --ng flag enables no-GUI mode."""
        result = main.is_no_gui_mode(["src/core/main.py", "--ng"])
        self.assertTrue(result)
    
    def test_no_gui_mode_with_no_gui_flag(self):
        """Test that --no-gui flag enables no-GUI mode."""
        result = main.is_no_gui_mode(["src/core/main.py", "--no-gui"])
        self.assertTrue(result)
    
    def test_no_gui_mode_with_sessionless_flag(self):
        """Test that --sessionless flag enables no-GUI mode."""
        result = main.is_no_gui_mode(["src/core/main.py", "--sessionless"])
        self.assertTrue(result)
    
    def test_no_gui_mode_disabled_by_default(self):
        """Test that no-GUI mode is disabled by default."""
        result = main.is_no_gui_mode(["src/core/main.py"])
        self.assertFalse(result)
    
    def test_connectionless_mode_with_n_flag(self):
        """Test that --n flag enables connectionless mode."""
        result = main.is_connectionless_browser_mode(["src/core/main.py", "--n"])
        self.assertTrue(result)
    
    def test_connectionless_mode_disabled_by_default(self):
        """Test that connectionless mode is disabled by default."""
        result = main.is_connectionless_browser_mode(["src/core/main.py"])
        self.assertFalse(result)
    
    def test_modes_are_mutually_exclusive_in_logic(self):
        """Test that both modes can be detected but main.py handles exclusivity."""
        # Both flags present (edge case - main.py should handle priority)
        no_gui = main.is_no_gui_mode(["src/core/main.py", "--ng", "--n"])
        connectionless = main.is_connectionless_browser_mode(["src/core/main.py", "--ng", "--n"])
        # Both are detected, but startup logic should prioritize one
        self.assertTrue(no_gui or connectionless)

class TestSessionChecking(unittest.TestCase):
    """Test session checking functionality."""
    
    def test_check_running_sessions_returns_list(self):
        """Test that check_running_sessions returns a list."""
        sessions = main.check_running_sessions()
        self.assertIsInstance(sessions, list)
    
    def test_check_running_sessions_excludes_current_process(self):
        """Test that current process is excluded from session list."""
        import os
        sessions = main.check_running_sessions()
        current_pid = os.getpid()
        
        # Current process should not be in the list
        for session in sessions:
            self.assertNotEqual(session['pid'], current_pid)
    
    def test_session_info_contains_required_fields(self):
        """Test that session info contains pid, port, and cmdline."""
        sessions = main.check_running_sessions()
        
        for session in sessions:
            self.assertIn('pid', session)
            self.assertIn('port', session)
            self.assertIn('cmdline', session)
            self.assertIsInstance(session['pid'], int)
            # Port can be None if not listening
            self.assertTrue(session['port'] is None or isinstance(session['port'], int))
    
    def test_is_port_in_use_with_free_port(self):
        """Test is_port_in_use returns False for a free port."""
        # Find a free port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', 0))
            free_port = s.getsockname()[1]
        
        # Port should be free after socket closes
        result = main.is_port_in_use(free_port)
        self.assertFalse(result)
    
    def test_is_port_in_use_with_occupied_port(self):
        """Test is_port_in_use returns True for an occupied port."""
        # Create a socket and bind to a port
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('127.0.0.1', 0))
            s.listen(1)
            occupied_port = s.getsockname()[1]
            
            # Port should be in use while socket is open
            result = main.is_port_in_use(occupied_port)
            self.assertTrue(result)
        
        # Port should be free after socket closes
        result = main.is_port_in_use(occupied_port)
        self.assertFalse(result)

class TestSessionlessModeExecution(unittest.TestCase):
    """Test sessionless mode execution."""
    
    @patch('src.core.main.db.init_db')
    @patch('src.core.main.db.get_db_stats')
    @patch('src.core.main.db.list_legacy_databases')
    def test_run_sessionless_mode_returns_dict(self, mock_legacy, mock_stats, mock_init):
        """Test that run_sessionless_mode returns a dictionary."""
        mock_stats.return_value = {"total_items": 42}
        mock_legacy.return_value = []
        
        result = main.run_sessionless_mode()
        
        self.assertIsInstance(result, dict)
        self.assertIn('mode', result)
        self.assertEqual(result['mode'], 'no-gui')
    
    @patch('src.core.main.db.init_db')
    @patch('src.core.main.db.get_db_stats')
    @patch('src.core.main.db.list_legacy_databases')
    def test_sessionless_mode_contains_required_info(self, mock_legacy, mock_stats, mock_init):
        """Test that sessionless mode result contains required information."""
        mock_stats.return_value = {"total_items": 42}
        mock_legacy.return_value = []
        
        result = main.run_sessionless_mode()
        
        required_keys = ['mode', 'active_db', 'total_items', 'legacy_db_count', 'scan_dirs']
        for key in required_keys:
            self.assertIn(key, result)
    
    @patch('src.core.main.db.init_db')
    @patch('src.core.main.db.get_db_stats')
    @patch('src.core.main.db.list_legacy_databases')
    def test_sessionless_mode_initializes_db(self, mock_legacy, mock_stats, mock_init):
        """Test that sessionless mode initializes database."""
        mock_stats.return_value = {"total_items": 0}
        mock_legacy.return_value = []
        
        main.run_sessionless_mode()
        
        mock_init.assert_called_once()

class TestConnectionlessBrowserMode(unittest.TestCase):
    """Test connectionless browser mode."""
    
    @patch('src.core.main.db.init_db')
    @patch('src.core.main.db.get_db_stats')
    @patch('src.core.main.get_preferred_browser')
    def test_run_connectionless_mode_returns_dict(self, mock_browser, mock_stats, mock_init):
        """Test that run_connectionless_browser_mode returns a dictionary."""
        mock_stats.return_value = {"total_items": 42}
        mock_browser_instance = Mock()
        mock_browser.return_value = mock_browser_instance
        
        result = main.run_connectionless_browser_mode()
        
        self.assertIsInstance(result, dict)
        self.assertIn('mode', result)
        self.assertEqual(result['mode'], 'connectionless-browser')
    
    @patch('src.core.main.db.init_db')
    @patch('src.core.main.db.get_db_stats')
    @patch('src.core.main.get_preferred_browser')
    def test_connectionless_mode_opens_browser(self, mock_browser, mock_stats, mock_init):
        """Test that connectionless mode opens browser."""
        mock_stats.return_value = {"total_items": 42}
        mock_browser_instance = Mock()
        mock_browser.return_value = mock_browser_instance

        with patch.dict(os.environ, {"MWV_DISABLE_BROWSER_OPEN": "0"}):
            main.run_connectionless_browser_mode()
        
        mock_browser_instance.open.assert_called_once()
    
    @patch('src.core.main.db.init_db')
    @patch('src.core.main.db.get_db_stats')
    @patch('src.core.main.get_preferred_browser')
    def test_connectionless_mode_url_format(self, mock_browser, mock_stats, mock_init):
        """Test that connectionless mode generates proper file:// URL."""
        mock_stats.return_value = {"total_items": 42}
        mock_browser_instance = Mock()
        mock_browser.return_value = mock_browser_instance
        
        result = main.run_connectionless_browser_mode()
        
        self.assertIn('app_url', result)
        self.assertTrue(result['app_url'].startswith('file://'))
        self.assertTrue(result['app_url'].endswith('app.html'))

class TestBrowserPreference(unittest.TestCase):
    """Test browser preference detection."""
    
    @patch('shutil.which')
    @patch('webbrowser.get')
    def test_get_preferred_browser_prefers_chrome(self, mock_get, mock_which):
        """Test that Chrome is preferred when available."""
        mock_which.side_effect = lambda cmd: '/usr/bin/google-chrome' if cmd == 'google-chrome' else None
        mock_get.return_value = Mock()
        
        result = main.get_preferred_browser()
        
        # Chrome should be attempted first
        mock_which.assert_any_call('google-chrome')
    
    @patch('shutil.which')
    def test_get_preferred_browser_fallback(self, mock_which):
        """Test browser fallback when preferred browsers not available."""
        mock_which.return_value = None  # No browsers found
        
        result = main.get_preferred_browser()

        import webbrowser
        
        # Should return default webbrowser module
        self.assertIs(result, webbrowser)

class TestCommandLineUsage(unittest.TestCase):
    """Test command-line usage examples."""
    
    def test_normal_startup_detection(self):
        """Test normal startup (no special flags)."""
        args = ["src/core/main.py"]
        self.assertFalse(main.is_no_gui_mode(args))
        self.assertFalse(main.is_connectionless_browser_mode(args))
    
    def test_help_flag_does_not_trigger_modes(self):
        """Test that --help doesn't trigger special modes."""
        args = ["src/core/main.py", "--help"]
        self.assertFalse(main.is_no_gui_mode(args))
        self.assertFalse(main.is_connectionless_browser_mode(args))
    
    def test_multiple_flags_detection(self):
        """Test detection with multiple flags present."""
        args = ["src/core/main.py", "--ng", "--verbose", "--debug"]
        self.assertTrue(main.is_no_gui_mode(args))

def run_tests():
    """Run all tests with detailed output."""
    print("=" * 70)
    print("  STARTUP VARIANTS & SESSION MANAGEMENT TEST SUITE")
    print("=" * 70)
    print()
    print("Testing startup mode detection and session management...")
    print()
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestStartupModeDetection))
    suite.addTests(loader.loadTestsFromTestCase(TestSessionChecking))
    suite.addTests(loader.loadTestsFromTestCase(TestSessionlessModeExecution))
    suite.addTests(loader.loadTestsFromTestCase(TestConnectionlessBrowserMode))
    suite.addTests(loader.loadTestsFromTestCase(TestBrowserPreference))
    suite.addTests(loader.loadTestsFromTestCase(TestCommandLineUsage))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print()
    print("=" * 70)
    if result.wasSuccessful():
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ SOME TESTS FAILED")
    print("=" * 70)
    
    return 0 if result.wasSuccessful() else 1

if __name__ == "__main__":
    sys.exit(run_tests())
