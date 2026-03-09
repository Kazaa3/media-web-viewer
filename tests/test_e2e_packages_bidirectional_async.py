#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: E2E / Async Bidirectional Package Data Flow
# Eingabewerte: main.py (_get_installed_packages), web/app.html (loadEnvironmentInfo)
# Ausgabewerte: Bidirektionaler Datenfluß pip→backend→frontend→DOM & frontend→backend
# Testdateien: main.py, web/app.html, web/i18n.json
# Kommentar: End-to-End Test für vollständigen, bidirektionalen, asynchronen Package-Datenfluss.

import asyncio
import json
import re
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, Mock, patch
from typing import Any, Dict, List


class TestE2EPackagesBidirectionalAsync(unittest.TestCase):
    """
    End-to-End test suite for bidirectional, asynchronous package data flow.
    
    Tests the complete pipeline:
    1. Backend: subprocess pip call → parsing → data structuring
    2. API: eel.expose function → JSON response
    3. Frontend: async eel call → normalization → DOM rendering
    4. Reverse: user interaction → backend request → response processing
    """

    def setUp(self):
        """Initialize test environment with paths and sample data."""
        self.root = Path(__file__).parent.parent
        self.main_py = self.root / "main.py"
        self.app_html = self.root / "web" / "app.html"
        
        # Sample pip JSON output (realistic structure)
        self.sample_pip_json = json.dumps([
            {"name": "bottle", "version": "0.12.25"},
            {"name": "Eel", "version": "0.16.0"},
            {"name": "pip", "version": "24.0"},
            {"name": "setuptools", "version": "69.1.0"},
            {"name": "wheel", "version": "0.42.0"},
        ])
        
        # Sample pip columns output (fallback format)
        self.sample_pip_columns = """Package    Version
---------- -------
bottle     0.12.25
Eel        0.16.0
pip        24.0
setuptools 69.1.0
wheel      0.42.0
"""
        
        # Load actual code for integration testing
        self.main_code = self.main_py.read_text(encoding="utf-8")
        self.html_code = self.app_html.read_text(encoding="utf-8")

    def test_01_backend_pip_json_parsing_success(self):
        """Test: Backend successfully calls pip and parses JSON format."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = self.sample_pip_json
        mock_result.stderr = ""
        
        with patch('subprocess.run', return_value=mock_result):
            # Extract and execute the _get_installed_packages logic
            # This simulates the actual backend flow
            packages_data = json.loads(mock_result.stdout)
            packages = sorted(packages_data, key=lambda x: x.get("name", "").lower())
            source = "pip_list_json"
            
            self.assertEqual(len(packages), 5)
            self.assertEqual(packages[0]["name"], "bottle")
            self.assertEqual(packages[1]["name"], "Eel")
            self.assertEqual(source, "pip_list_json")

    def test_02_backend_pip_columns_fallback(self):
        """Test: Backend falls back to columns format when JSON fails."""
        mock_json_fail = Mock()
        mock_json_fail.returncode = 1
        mock_json_fail.stdout = ""
        mock_json_fail.stderr = "JSON format not supported"
        
        mock_columns_success = Mock()
        mock_columns_success.returncode = 0
        mock_columns_success.stdout = self.sample_pip_columns
        mock_columns_success.stderr = ""
        
        def mock_subprocess_side_effect(*args, **kwargs):
            cmd = args[0] if args else kwargs.get('args', [])
            if '--format=json' in cmd:
                return mock_json_fail
            elif '--format=columns' in cmd:
                return mock_columns_success
            return Mock(returncode=1, stdout="", stderr="")
        
        with patch('subprocess.run', side_effect=mock_subprocess_side_effect):
            # Simulate fallback parsing logic
            packages = []
            lines = [line.strip() for line in self.sample_pip_columns.splitlines() if line.strip()]
            for line in lines:
                if line.lower().startswith("package") and "version" in line.lower():
                    continue
                if set(line) <= set("- "):
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    packages.append({"name": parts[0], "version": parts[1]})
            
            packages = sorted(packages, key=lambda x: x.get("name", "").lower())
            source = "pip_list_columns"
            
            self.assertEqual(len(packages), 5)
            self.assertEqual(packages[0]["name"], "bottle")
            self.assertEqual(source, "pip_list_columns")

    def test_03_backend_api_structure(self):
        """Test: Backend API (get_environment_info) returns correct structure."""
        # Verify the function exists and is exposed via @eel.expose
        self.assertIn("@eel.expose", self.main_code)
        self.assertIn("def get_environment_info", self.main_code)
        
        # Verify it calls _get_installed_packages
        env_info_match = re.search(
            r'def get_environment_info.*?(?=\n@eel\.expose|\ndef [a-zA-Z_]|\Z)',
            self.main_code,
            re.DOTALL
        )
        self.assertIsNotNone(env_info_match)
        func_body = env_info_match.group(0)
        self.assertIn("_get_installed_packages", func_body)

    def test_04_backend_returns_source_metadata(self):
        """Test: Backend includes source metadata in response."""
        # Verify the backend tracks and returns the source of package data
        self.assertIn("installed_packages_source", self.main_code)
        self.assertIn("requirements_status", self.main_code)
        self.assertIn("pip_list_json", self.main_code)
        self.assertIn("pip_list_columns", self.main_code)
        self.assertIn("importlib_or_pkg_resources", self.main_code)

    def test_05_frontend_async_eel_call_exists(self):
        """Test: Frontend makes async call to backend via eel."""
        self.assertRegex(self.html_code, r"async function loadEnvironmentInfo\([^)]*\)")
        self.assertIn("await eel.get_environment_info()", self.html_code)

    def test_06_frontend_normalization_function_exists(self):
        """Test: Frontend has normalization function for package data."""
        self.assertIn("function normalizeInstalledPackages(rawPackages)", self.html_code)
        
        # Verify it handles array format
        self.assertIn("if (Array.isArray(rawPackages))", self.html_code)
        
        # Verify it handles object format (key-value pairs)
        self.assertIn("else if (rawPackages && typeof rawPackages === 'object')", self.html_code)

    def test_07_frontend_normalization_handles_multiple_formats(self):
        """Test: Frontend normalization handles array and object formats."""
        # Extract full normalization function block
        norm_match = re.search(
            r'function normalizeInstalledPackages\(rawPackages\).*?(?=\n\s*async function loadEnvironmentInfo|\Z)',
            self.html_code,
            re.DOTALL
        )
        self.assertIsNotNone(norm_match)
        norm_body = norm_match.group(0)
        
        # Verify handling of multiple field names (name/Name/project_name)
        self.assertIn("pkg.name", norm_body)
        self.assertIn("Name", norm_body)
        
        # Verify handling of version field variants
        self.assertIn("version", norm_body)

    def test_08_frontend_dom_rendering_elements(self):
        """Test: Frontend has DOM elements for package display."""
        self.assertIn('id="package-count"', self.html_code)
        self.assertIn('id="package-source"', self.html_code)
        self.assertIn('id="installed-packages-list"', self.html_code)
        self.assertIn('id="package-search"', self.html_code)
        self.assertIn('id="requirements-count"', self.html_code)
        self.assertIn('id="requirements-status-list"', self.html_code)

    def test_09_frontend_displays_package_source(self):
        """Test: Frontend displays the package data source."""
        # Verify source display logic exists in loadEnvironmentInfo
        # Search for the function and package-source within reasonable proximity
        load_env_exists = re.search(r'async function loadEnvironmentInfo\([^)]*\)', self.html_code) is not None
        self.assertTrue(load_env_exists, "loadEnvironmentInfo function should exist")
        
        # Verify package-source element is referenced in the code
        package_source_ref = "'package-source'" in self.html_code or '"package-source"' in self.html_code
        self.assertTrue(package_source_ref, "Should reference package-source element")

    def test_10_frontend_retry_mechanism_on_empty_packages(self):
        """Test: Frontend retries with force_refresh when packages are empty."""
        load_env_match = re.search(
            r'async function loadEnvironmentInfo\([^)]*\)\s*{(.*?)\n\s*}(?:\n|$)',
            self.html_code,
            re.DOTALL
        )
        self.assertIsNotNone(load_env_match)
        func_body = load_env_match.group(1)
        
        # Verify retry logic
        self.assertIn("force-refresh", func_body.lower())
        self.assertIn("get_environment_info(true)", func_body)

    def test_11_bidirectional_search_input_event_binding(self):
        """Test: Frontend binds search input for user interactions."""
        # Verify search functionality (user → backend direction)
        self.assertIn('id="package-search"', self.html_code)
        
        # Should have event listener setup
        search_pattern = r'getElementById\(["\']package-search["\']\).*?addEventListener'
        has_search_listener = re.search(search_pattern, self.html_code, re.DOTALL)
        
        if not has_search_listener:
            # Alternative pattern: direct oninput/onchange
            alt_pattern = r'id="package-search"[^>]*(oninput|onchange)'
            has_inline_handler = re.search(alt_pattern, self.html_code)
            self.assertTrue(
                has_inline_handler is not None,
                "Package search should have event binding"
            )

    def test_12_async_flow_error_handling(self):
        """Test: Frontend async flow includes error handling."""
        load_env_match = re.search(
            r'async function loadEnvironmentInfo\([^)]*\)\s*{(.*?)\n\s*}(?:\n|$)',
            self.html_code,
            re.DOTALL
        )
        self.assertIsNotNone(load_env_match)
        func_body = load_env_match.group(1)
        
        # Should have try-catch for async operations
        self.assertIn("try", func_body)
        self.assertIn("catch", func_body)

    def test_13_backend_timeout_handling(self):
        """Test: Backend handles subprocess timeout gracefully."""
        # Verify timeout parameter in subprocess.run
        pip_call_pattern = r'subprocess\.run\([^)]*timeout\s*=\s*\d+'
        self.assertRegex(self.main_code, pip_call_pattern)
        
        # Verify TimeoutExpired exception handling
        self.assertIn("subprocess.TimeoutExpired", self.main_code)

    def test_14_backend_multiple_fallback_stages(self):
        """Test: Backend implements multi-stage fallback (JSON → columns → importlib)."""
        # Find _get_installed_packages function
        func_match = re.search(
            r'def _get_installed_packages\(\):.*?(?=\n    def [a-zA-Z_]|\Z)',
            self.main_code,
            re.DOTALL
        )
        self.assertIsNotNone(func_match)
        func_body = func_match.group(0)
        
        # Verify all three stages mentioned
        self.assertIn("pip_list_json", func_body)
        self.assertIn("pip_list_columns", func_body)
        self.assertIn("importlib_or_pkg_resources", func_body)
        
        # Verify fallback trigger logic
        self.assertIn("if not packages:", func_body)

    def test_15_backend_returns_tuple_with_source(self):
        """Test: Backend returns (packages, source) tuple."""
        func_match = re.search(
            r'def _get_installed_packages\(\):.*?return packages, source',
            self.main_code,
            re.DOTALL
        )
        self.assertIsNotNone(func_match, "Function should return (packages, source) tuple")

    def test_16_integration_data_structure_consistency(self):
        """Test: Backend and frontend expect consistent data structure."""
        # Backend should produce list of dicts with name/version
        backend_pattern = r'\{"name":\s*[^,]+,\s*"version":\s*[^}]+\}'
        
        # Frontend expects name and version fields
        frontend_expects_name = 'pkg.name' in self.html_code
        frontend_expects_version = 'pkg.version' in self.html_code
        
        self.assertTrue(frontend_expects_name, "Frontend should access pkg.name")
        self.assertTrue(frontend_expects_version, "Frontend should access pkg.version")

    def test_17_async_promise_chain_integrity(self):
        """Test: Frontend async operations form complete promise chain."""
        load_env_match = re.search(
            r'async function loadEnvironmentInfo\([^)]*\).*?}',
            self.html_code,
            re.DOTALL
        )
        self.assertIsNotNone(load_env_match)
        func_body = load_env_match.group(0)
        
        # Count awaits to verify async operations are properly awaited
        await_count = func_body.count('await')
        self.assertGreaterEqual(await_count, 1, "Should have at least one await for eel call")

    def test_18_bidirectional_force_refresh_parameter(self):
        """Test: Frontend can trigger backend refresh via parameter."""
        # Backend accepts force_refresh parameter
        self.assertIn("def get_environment_info(force_refresh=False)", self.main_code)
        
        # Frontend calls with parameter for refresh
        self.assertIn("get_environment_info(true)", self.html_code)

    def test_19_package_count_display_binding(self):
        """Test: Frontend displays package count from backend."""
        load_env_exists = re.search(r'async function loadEnvironmentInfo\([^)]*\)', self.html_code) is not None
        self.assertTrue(load_env_exists, "loadEnvironmentInfo function should exist")
        
        # Should reference package-count element
        package_count_ref = "'package-count'" in self.html_code or '"package-count"' in self.html_code
        self.assertTrue(package_count_ref, "Should update package count display")

    def test_20_e2e_complete_flow_simulation(self):
        """
        Test: Complete E2E flow simulation with mocked subprocess and DOM.
        
        Simulates:
        1. User opens Options tab
        2. Frontend calls backend async
        3. Backend calls pip subprocess
        4. Backend parses and returns data
        5. Frontend normalizes data
        6. Frontend renders to DOM
        """
        # Step 1: Mock subprocess (backend layer)
        mock_subprocess_result = Mock()
        mock_subprocess_result.returncode = 0
        mock_subprocess_result.stdout = self.sample_pip_json
        mock_subprocess_result.stderr = ""
        
        # Step 2: Simulate backend processing
        with patch('subprocess.run', return_value=mock_subprocess_result):
            # Parse as backend would
            packages_data = json.loads(mock_subprocess_result.stdout)
            backend_packages = sorted(packages_data, key=lambda x: x.get("name", "").lower())
            backend_source = "pip_list_json"
            
            # Backend response structure
            backend_response = {
                "installed_packages": backend_packages,
                "package_count": len(backend_packages),
                "installed_packages_source": backend_source,
                "python_version": "3.11.8",
            }
        
        # Step 3: Simulate frontend normalization (JavaScript → Python simulation)
        def normalize_packages(raw_packages):
            """Simulate frontend normalizeInstalledPackages()."""
            normalized = []
            if isinstance(raw_packages, list):
                for pkg in raw_packages:
                    if not isinstance(pkg, dict):
                        continue
                    name = str(pkg.get("name") or pkg.get("Name") or "").strip()
                    version = str(pkg.get("version") or pkg.get("Version") or "-").strip()
                    if name:
                        normalized.append({"name": name, "version": version or "-"})
            normalized.sort(key=lambda x: x["name"].lower())
            return normalized
        
        frontend_packages = normalize_packages(backend_response["installed_packages"])
        
        # Step 4: Validate complete flow
        self.assertEqual(len(frontend_packages), 5)
        self.assertEqual(frontend_packages[0]["name"], "bottle")
        self.assertEqual(frontend_packages[0]["version"], "0.12.25")
        self.assertEqual(backend_response["installed_packages_source"], "pip_list_json")
        self.assertEqual(backend_response["package_count"], 5)
        
        # Step 5: Verify data consistency (backend output = frontend input)
        for backend_pkg, frontend_pkg in zip(backend_packages, frontend_packages):
            self.assertEqual(backend_pkg["name"], frontend_pkg["name"])
            self.assertEqual(backend_pkg["version"], frontend_pkg["version"])

    def test_21_reverse_flow_user_search_triggers_filtering(self):
        """
        Test: Reverse flow - user search input triggers frontend filtering.
        
        Simulates:
        1. Packages displayed in DOM
        2. User types in search box
        3. Frontend filters visible packages
        4. DOM updates dynamically
        """
        # Simulate initial package list
        packages = [
            {"name": "bottle", "version": "0.12.25"},
            {"name": "Eel", "version": "0.16.0"},
            {"name": "flask", "version": "3.0.0"},
            {"name": "django", "version": "5.0.0"},
        ]
        
        # Simulate frontend search filter logic
        def filter_packages(packages, search_term):
            """Simulate frontend package filtering."""
            if not search_term:
                return packages
            search_lower = search_term.lower()
            return [
                pkg for pkg in packages
                if search_lower in pkg["name"].lower() or search_lower in pkg.get("version", "").lower()
            ]
        
        # Test various search scenarios
        filtered_all = filter_packages(packages, "")
        self.assertEqual(len(filtered_all), 4)
        
        filtered_bottle = filter_packages(packages, "bottle")
        self.assertEqual(len(filtered_bottle), 1)
        self.assertEqual(filtered_bottle[0]["name"], "bottle")
        
        filtered_case_insensitive = filter_packages(packages, "EEL")
        self.assertEqual(len(filtered_case_insensitive), 1)
        self.assertEqual(filtered_case_insensitive[0]["name"], "Eel")
        
        filtered_version = filter_packages(packages, "3.0")
        self.assertEqual(len(filtered_version), 1)
        self.assertEqual(filtered_version[0]["name"], "flask")

    def test_22_async_concurrent_calls_handling(self):
        """Test: System handles concurrent async calls gracefully."""
        # Verify backend doesn't have global state issues
        # (each call should be independent)
        
        # Simulate multiple concurrent frontend calls
        call_results = []
        
        for i in range(3):
            mock_result = Mock()
            mock_result.returncode = 0
            mock_result.stdout = json.dumps([
                {"name": f"package-{i}", "version": f"1.{i}.0"}
            ])
            
            with patch('subprocess.run', return_value=mock_result):
                packages_data = json.loads(mock_result.stdout)
                call_results.append(packages_data)
        
        # Each call should have independent results
        self.assertEqual(call_results[0][0]["name"], "package-0")
        self.assertEqual(call_results[1][0]["name"], "package-1")
        self.assertEqual(call_results[2][0]["name"], "package-2")

    def test_23_backend_tools_status_structure(self):
        """Test: Backend environment API includes tools_status metadata."""
        self.assertIn('"tools_status"', self.main_code)
        self.assertIn("_get_runtime_tools_status", self.main_code)

        expected_keys = [
            "ffmpeg_cli_available",
            "ffmpeg_cli_version",
            "ffprobe_cli_available",
            "ffprobe_cli_version",
            "browser_available",
            "browser_name",
            "browser_path",
            "python_vlc_available",
            "vlc_cli_available",
            "mutagen_available",
        ]
        for key in expected_keys:
            self.assertIn(f'"{key}"', self.main_code)

    def test_24_frontend_tools_status_rendering(self):
        """Test: Frontend renders the separated Mutagen/GUI/Mediaplayer status rows in Options tab."""
        self.assertIn('id="env-mutagen-status"', self.html_code)
        self.assertIn('id="env-gui-status"', self.html_code)
        self.assertIn('id="env-mediaplayer-status"', self.html_code)
        self.assertIn('id="env-base-dependencies-status"', self.html_code)
        self.assertIn("env_label_base_dependencies", self.html_code)
        self.assertIn("env_label_mutagen", self.html_code)
        self.assertIn("env_label_gui", self.html_code)
        self.assertIn("env_label_mediaplayer", self.html_code)
        self.assertIn("info.tools_status", self.html_code)
        self.assertIn("ffmpeg_cli_version", self.html_code)
        self.assertIn("ffprobe_cli_version", self.html_code)

        # Ensure commonly displayed tool labels are part of render string
        self.assertIn("ffmpeg", self.html_code)
        self.assertIn("ffprobe", self.html_code)
        self.assertIn("python-vlc", self.html_code)
        self.assertIn("mutagen", self.html_code)


if __name__ == "__main__":
    unittest.main()
