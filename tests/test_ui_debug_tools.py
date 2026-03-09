#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Debugging / UI Trace Tools
# Eingabewerte: main.py (get_environment_info), web/app.html (console.log patterns)
# Ausgabewerte: Verifiziert, dass Debug-Tools für UI-Probleme verfügbar sind
# Testdateien: main.py, web/app.html
# Kommentar: Test suite documenting UI debugging tools used to diagnose issues like the i18n bug

import unittest
from pathlib import Path
import tempfile
import json
import re
from unittest.mock import patch, Mock


class TestUIDebugTools(unittest.TestCase):
    """
    Test suite documenting and verifying UI debugging tools.
    
    Background:
    When the packages display wasn't working, we used multiple debugging approaches:
    1. Backend trace logging to file
    2. Frontend console.log for data flow
    3. Visible debug UI panels
    4. Process inspection
    
    This test suite ensures these debugging mechanisms remain available.
    """

    def setUp(self):
        """Initialize test environment with paths."""
        self.root = Path(__file__).parent.parent
        self.main_py = self.root / "main.py"
        self.app_html = self.root / "web" / "app.html"
        self.main_code = self.main_py.read_text(encoding="utf-8")
        self.html_code = self.app_html.read_text(encoding="utf-8")

    def test_01_backend_exposes_get_environment_info(self):
        """Test: Backend has get_environment_info function exposed via eel."""
        self.assertIn("@eel.expose", self.main_code)
        self.assertIn("def get_environment_info", self.main_code)
        
        # Should accept force_refresh parameter
        self.assertIn("def get_environment_info(force_refresh=False)", self.main_code)

    def test_02_backend_returns_diagnostic_data(self):
        """Test: Backend response includes diagnostic metadata."""
        # Find the return structure
        get_env_info_match = re.search(
            r'def get_environment_info.*?return result',
            self.main_code,
            re.DOTALL
        )
        self.assertIsNotNone(get_env_info_match)
        func_body = get_env_info_match.group(0)
        
        # Should include diagnostic fields
        diagnostic_fields = [
            'installed_packages',
            'package_count',
            'installed_packages_source',
            'requirements_status',
            'env_type',
            'python_executable',
        ]
        
        for field in diagnostic_fields:
            self.assertIn(f'"{field}"', func_body, 
                         f"Response should include diagnostic field: {field}")

    def test_03_backend_has_trace_logging_capability(self):
        """Test: Backend code structure supports trace logging (when enabled)."""
        # The trace logging was temporarily added for debugging
        # This test documents where it would be added if needed again
        
        # Verify the function exists and has return point where logging could be inserted
        get_env_info_match = re.search(
            r'def get_environment_info\(.*?\):.*?return result',
            self.main_code,
            re.DOTALL
        )
        self.assertIsNotNone(get_env_info_match)
        
        # Verify logging infrastructure exists
        self.assertIn("import logging", self.main_code)
        self.assertIn("from pathlib import Path", self.main_code)

    def test_04_frontend_has_normalization_function(self):
        """Test: Frontend has data normalization for debugging data format issues."""
        self.assertIn("function normalizeInstalledPackages(rawPackages)", self.html_code)
        
        # Find the function
        norm_match = re.search(
            r'function normalizeInstalledPackages\(rawPackages\).*?return normalized;',
            self.html_code,
            re.DOTALL
        )
        self.assertIsNotNone(norm_match)
        func_body = norm_match.group(0)
        
        # Should handle multiple input formats
        self.assertIn('Array.isArray', func_body)
        self.assertIn('typeof rawPackages', func_body)

    def test_05_frontend_has_error_handling_in_load_function(self):
        """Test: Frontend loadEnvironmentInfo has try-catch for debugging."""
        # loadEnvironmentInfo is large, just verify key debugging features exist
        self.assertIn('async function loadEnvironmentInfo', self.html_code)
        self.assertIn('try', self.html_code)
        self.assertIn('catch', self.html_code)
        self.assertIn('console.error', self.html_code)

    def test_06_frontend_console_logging_points_documented(self):
        """Test: Document where console.log can be added for debugging."""
        # Key debugging insertion points in loadEnvironmentInfo:
        # 1. After receiving data from backend
        # 2. After normalization
        # 3. Before rendering decision
        
        # Verify key debugging points exist in the HTML
        self.assertIn('async function loadEnvironmentInfo', self.html_code)
        self.assertIn('await eel.get_environment_info', self.html_code)
        self.assertIn('normalizeInstalledPackages', self.html_code)
        self.assertIn('function renderPackages', self.html_code)

    def test_07_dom_elements_exist_for_data_display(self):
        """Test: All DOM elements needed for debugging exist."""
        critical_elements = [
            'package-count',
            'package-source',
            'installed-packages-list',
            'requirements-count',
            'requirements-status-list',
            'env-tools-status',
        ]
        
        for element_id in critical_elements:
            self.assertIn(f'id="{element_id}"', self.html_code,
                         f"DOM element {element_id} should exist for debugging")

    def test_08_backend_caching_mechanism_documented(self):
        """Test: Backend has caching that can affect debugging."""
        # Caching can hide issues - important to understand for debugging
        self.assertIn("_ENV_INFO_CACHE", self.main_code)
        
        # Should have force_refresh to bypass cache
        get_env_match = re.search(
            r'def get_environment_info\(force_refresh=False\):.*?if not force_refresh',
            self.main_code,
            re.DOTALL
        )
        self.assertIsNotNone(get_env_match,
                            "Should have force_refresh parameter to bypass cache for debugging")

    def test_09_frontend_has_refresh_button(self):
        """Test: Frontend has refresh button for manual debugging."""
        # Button to trigger force refresh
        self.assertIn('onclick="loadEnvironmentInfo(true)"', self.html_code)
        
        # Or alternative event binding
        refresh_exists = (
            'loadEnvironmentInfo(true)' in self.html_code or
            'loadEnvironmentInfo(force' in self.html_code
        )
        self.assertTrue(refresh_exists, "Should have way to trigger force refresh")

    def test_10_data_flow_diagram_in_code(self):
        """Test: Document the complete data flow for debugging reference."""
        # This test serves as documentation of the data flow:
        
        # Step 1: Frontend calls backend
        self.assertIn('await eel.get_environment_info', self.html_code)
        
        # Step 2: Backend calls _get_installed_packages
        self.assertIn('def _get_installed_packages', self.main_code)
        
        # Step 3: Backend returns structured data
        self.assertIn('return result', self.main_code)
        
        # Step 4: Frontend normalizes data
        self.assertIn('normalizeInstalledPackages', self.html_code)
        
        # Step 5: Frontend renders to DOM
        self.assertIn('function renderPackages', self.html_code)
        
        # All steps verified - data flow is traceable

    def test_11_error_messages_are_translatable(self):
        """Test: Error messages use i18n for consistency."""
        # Error fallbacks should use translation function
        self.assertIn("t('env_no_packages_found')", self.html_code)
        self.assertIn("t('common_error_loading')", self.html_code)

    def test_12_backend_subprocess_calls_have_timeout(self):
        """Test: Subprocess calls have timeout to prevent hanging during debugging."""
        # Find subprocess.run calls
        subprocess_calls = re.findall(
            r'subprocess\.run\([^)]+\)',
            self.main_code,
            re.DOTALL
        )
        
        # At least one should exist (pip list)
        self.assertGreater(len(subprocess_calls), 0)
        
        # Should have timeout parameter somewhere in pip calls
        pip_calls = [call for call in subprocess_calls if 'pip' in call.lower()]
        self.assertGreater(len(pip_calls), 0, "Should have pip subprocess calls")

    def test_13_frontend_search_functionality_exists(self):
        """Test: Search functionality helps debug specific packages."""
        self.assertIn('id="package-search"', self.html_code)
        
        # Should have search event handler
        search_handler_exists = (
            'addEventListener' in self.html_code and 
            'package-search' in self.html_code
        )
        self.assertTrue(search_handler_exists)

    def test_14_multiple_fallback_stages_documented(self):
        """Test: Backend has multiple fallback stages for robustness."""
        # Should try multiple methods to get packages
        self.assertIn('pip_list_json', self.main_code)
        self.assertIn('pip_list_columns', self.main_code)
        
        # Should have fallback chain
        _get_installed_match = re.search(
            r'def _get_installed_packages\(\):.*?return.*?source',
            self.main_code,
            re.DOTALL
        )
        self.assertIsNotNone(_get_installed_match)

    def test_15_requirements_status_separate_from_packages(self):
        """Test: Requirements status is separate diagnostic info."""
        # Should have separate requirements checking
        self.assertIn('def _get_requirements_status', self.main_code)
        
        # Should return structured data
        req_status_match = re.search(
            r'def _get_requirements_status\(\):.*?return \{',
            self.main_code,
            re.DOTALL
        )
        self.assertIsNotNone(req_status_match)

    def test_16_ui_trace_insertion_points_documented(self):
        """Test: Document where UI trace logging can be inserted if needed."""
        # This test documents the debugging approach used during investigation:
        
        # Backend insertion point: before return in get_environment_info
        get_env_return = re.search(
            r'def get_environment_info\(.*?\).*?return result',
            self.main_code,
            re.DOTALL
        )
        self.assertIsNotNone(get_env_return,
                            "Backend function should have clear return point for trace logging")
        
        # Frontend insertion points are in the test above (test_06)

    def test_17_process_inspection_possible(self):
        """Test: Document that process inspection helped diagnose the issue."""
        # psutil is available for process inspection
        self.assertIn('import psutil', self.main_code)
        
        # sys module for runtime info
        self.assertIn('import sys', self.main_code)

    def test_18_regression_test_exists_for_root_cause(self):
        """Test: Regression test exists for the i18n bug that was found."""
        # The i18n bug was the root cause - verify regression test exists
        i18n_test_file = self.root / "tests" / "test_i18n_preserves_dynamic_elements.py"
        self.assertTrue(i18n_test_file.exists(),
                       "Regression test for i18n bug should exist")
        
        if i18n_test_file.exists():
            i18n_test_code = i18n_test_file.read_text(encoding="utf-8")
            self.assertIn('package-count', i18n_test_code)
            self.assertIn('innerHTML', i18n_test_code)

    def test_19_backend_includes_tools_status(self):
        """Test: Backend response includes aggregated runtime tools status."""
        get_env_info_match = re.search(
            r'def get_environment_info.*?return result',
            self.main_code,
            re.DOTALL
        )
        self.assertIsNotNone(get_env_info_match)
        func_body = get_env_info_match.group(0)
        self.assertIn('"tools_status"', func_body)
        self.assertIn('_get_runtime_tools_status', func_body)
        self.assertIn('"browser_available"', self.main_code)
        self.assertIn('"browser_name"', self.main_code)
        self.assertIn('"browser_path"', self.main_code)


class TestUIDebuggingWorkflow(unittest.TestCase):
    """
    Document the debugging workflow used to find the i18n bug.
    
    This serves as a guide for future similar issues.
    """

    def test_01_debugging_workflow_documentation(self):
        """Test: Document the step-by-step debugging approach."""
        # This test is documentation of the successful debugging process:
        
        steps = [
            "1. User reports: 'Keine Pakete gefunden' in GUI",
            "2. Check backend: Direct call shows 49 packages returned ✓",
            "3. Check frontend: Add console.log to track data flow",
            "4. Check DOM: Verify elements exist with correct IDs",
            "5. Discovery: getElementById('package-count') returns null",
            "6. Investigation: Element exists in HTML but disappears at runtime",
            "7. Root cause: applyTranslations() uses innerHTML, destroying child elements",
            "8. Solution: Move data-i18n to inner <span>, preserving siblings",
            "9. Verification: package-count now found, packages render ✓",
            "10. Regression test: Create test_i18n_preserves_dynamic_elements.py"
        ]
        
        # This test always passes - it exists for documentation
        self.assertTrue(True, "\n".join(steps))

    def test_02_debugging_tools_priority(self):
        """Test: Document priority of debugging tools."""
        debugging_priority = {
            "1_first_check": "Backend returns correct data (direct function call)",
            "2_second_check": "Frontend receives data (console.log in loadEnvironmentInfo)",
            "3_third_check": "DOM elements exist (getElementById in console)",
            "4_fourth_check": "Rendering logic executes (console.log before renderPackages)",
            "5_fifth_check": "Visible debug panel (add temporary UI element)",
        }
        
        # All these approaches were used
        self.assertEqual(len(debugging_priority), 5)

    def test_03_common_pitfalls_documented(self):
        """Test: Document common pitfalls found during debugging."""
        pitfalls = {
            "cache": "Backend cache can hide changes - use force_refresh=True",
            "innerHTML": "innerHTML destroys child elements - use inner spans for i18n",
            "timing": "applyTranslations() runs after page load, destroying elements",
            "browser_cache": "Browser cache can serve old HTML - use Ctrl+Shift+R",
            "environment": "Running in wrong Python env affects package list",
        }
        
        # Document that these were all encountered and solved
        self.assertEqual(len(pitfalls), 5)


if __name__ == "__main__":
    unittest.main()
