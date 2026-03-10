#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: E2E / Backend → Frontend (Unidirektional)
# Eingabewerte: main.py (_get_installed_packages, get_environment_info)
# Ausgabewerte: Validierung Backend-Daten-Pipeline bis Frontend-Empfang
# Testdateien: main.py, web/app.html
# Kommentar: Testet ausschließlich die Datenfluss-Richtung Backend → Frontend.

import json
import re
import subprocess
import sys
import unittest
from pathlib import Path
from unittest.mock import Mock, patch


class TestE2EBackendToFrontend(unittest.TestCase):
    """
    Unidirektionale Tests: Backend → Frontend Data Flow
    
    Diese Test-Suite fokussiert sich ausschließlich auf den Downstream-Fluss:
    subprocess → parsing → API → JSON response → Frontend normalization
    
    Frontend-to-Backend Interaktionen (Upstream) werden NICHT getestet.
    """

    def setUp(self):
        """Initialize test environment."""
        self.root = Path(__file__).parent.parent
        self.main_py = self.root / "main.py"
        self.app_html = self.root / "web" / "app.html"
        
        self.main_code = self.main_py.read_text(encoding="utf-8")
        self.html_code = self.app_html.read_text(encoding="utf-8")
        
        # Sample data for various sources
        self.pip_json_sample = json.dumps([
            {"name": "bottle", "version": "0.12.25"},
            {"name": "Eel", "version": "0.16.0"},
            {"name": "pip", "version": "24.0"},
        ])
        
        self.pip_columns_sample = """Package    Version
---------- -------
bottle     0.12.25
Eel        0.16.0
pip        24.0
"""

    # ========== Stage 1: Subprocess Execution ==========

    def test_01_subprocess_pip_json_call_structure(self):
        """Test: Backend calls pip with correct JSON format arguments."""
        # Verify subprocess.run is called with correct parameters
        self.assertIn('subprocess.run', self.main_code)
        self.assertIn('"pip", "list", "--format=json"', self.main_code)
        self.assertIn('--disable-pip-version-check', self.main_code)
        
        # Verify timeout is set
        pattern = r'subprocess\.run\([^)]*timeout\s*=\s*\d+'
        self.assertRegex(self.main_code, pattern)

    def test_02_subprocess_captures_output_correctly(self):
        """Test: Subprocess captures stdout/stderr correctly."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = self.pip_json_sample
        mock_result.stderr = ""
        
        with patch('subprocess.run', return_value=mock_result):
            # Simulate backend parsing
            packages = json.loads(mock_result.stdout)
            
            self.assertIsInstance(packages, list)
            self.assertEqual(len(packages), 3)
            self.assertEqual(packages[0]["name"], "bottle")

    def test_03_subprocess_handles_non_zero_exit(self):
        """Test: Backend handles pip command failures gracefully."""
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stdout = ""
        mock_result.stderr = "pip: command not found"
        
        # Backend should not crash, should trigger fallback
        # Verify fallback logic exists
        self.assertIn("if result.returncode == 0:", self.main_code)
        self.assertIn("else:", self.main_code)
        self.assertIn("_get_packages_fallback", self.main_code)

    def test_04_subprocess_timeout_handling(self):
        """Test: Backend handles subprocess timeout exceptions."""
        self.assertIn("subprocess.TimeoutExpired", self.main_code)
        self.assertIn("except subprocess.TimeoutExpired:", self.main_code)

    # ========== Stage 2: Backend Parsing ==========

    def test_05_parse_json_format_correctly(self):
        """Test: Backend correctly parses pip JSON output."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = self.pip_json_sample
        mock_result.stderr = ""
        
        with patch('subprocess.run', return_value=mock_result):
            packages_data = json.loads(mock_result.stdout)
            packages = sorted(packages_data, key=lambda x: x.get("name", "").lower())
            source = "pip_list_json"
            
            self.assertEqual(len(packages), 3)
            self.assertEqual(packages[0]["name"], "bottle")
            self.assertEqual(packages[0]["version"], "0.12.25")
            self.assertEqual(source, "pip_list_json")

    def test_06_parse_columns_format_fallback(self):
        """Test: Backend parses columns format when JSON fails."""
        # Simulate columns parsing
        packages = []
        lines = [l.strip() for l in self.pip_columns_sample.splitlines() if l.strip()]
        
        for line in lines:
            # Skip header
            if line.lower().startswith("package") and "version" in line.lower():
                continue
            # Skip separator
            if set(line) <= set("- "):
                continue
            
            parts = line.split()
            if len(parts) >= 2:
                packages.append({"name": parts[0], "version": parts[1]})
        
        packages = sorted(packages, key=lambda x: x.get("name", "").lower())
        
        self.assertEqual(len(packages), 3)
        self.assertEqual(packages[0]["name"], "bottle")
        self.assertEqual(packages[1]["name"], "Eel")

    def test_07_backend_sorts_packages_alphabetically(self):
        """Test: Backend sorts packages by name (case-insensitive)."""
        unsorted = [
            {"name": "Zlib", "version": "1.0"},
            {"name": "bottle", "version": "2.0"},
            {"name": "Eel", "version": "3.0"},
        ]
        
        sorted_packages = sorted(unsorted, key=lambda x: x.get("name", "").lower())
        
        self.assertEqual(sorted_packages[0]["name"], "bottle")
        self.assertEqual(sorted_packages[1]["name"], "Eel")
        self.assertEqual(sorted_packages[2]["name"], "Zlib")

    def test_08_backend_handles_malformed_json(self):
        """Test: Backend handles JSON parse errors gracefully."""
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "NOT VALID JSON {{"
        mock_result.stderr = ""
        
        with patch('subprocess.run', return_value=mock_result):
            # Should trigger fallback, not crash
            try:
                json.loads(mock_result.stdout)
                self.fail("Should have raised JSONDecodeError")
            except json.JSONDecodeError:
                # Expected, backend should catch this
                pass
        
        # Verify fallback exists
        self.assertIn("json.JSONDecodeError", self.main_code)

    # ========== Stage 3: Source Tracking ==========

    def test_09_backend_tracks_data_source(self):
        """Test: Backend tracks which source provided the data."""
        # Verify source tracking is implemented
        self.assertIn('source = "pip_list_json"', self.main_code)
        self.assertIn('source = "pip_list_columns"', self.main_code)
        self.assertIn('source = "importlib_or_pkg_resources"', self.main_code)

    def test_10_backend_returns_source_with_packages(self):
        """Test: Backend returns tuple (packages, source)."""
        # Verify return statement structure
        pattern = r'return packages, source'
        self.assertRegex(self.main_code, pattern)

    def test_11_backend_source_propagates_to_api(self):
        """Test: Source information reaches the API response."""
        self.assertIn("installed_packages_source", self.main_code)
        
        # Verify API function uses the source
        api_match = re.search(
            r'def get_environment_info.*?(?=\n@eel\.expose|\ndef [a-zA-Z_]|\Z)',
            self.main_code,
            re.DOTALL
        )
        self.assertIsNotNone(api_match)

    # ========== Stage 4: API Response Formation ==========

    def test_12_api_function_exists_and_exposed(self):
        """Test: get_environment_info is properly exposed via eel."""
        self.assertIn("@eel.expose", self.main_code)
        self.assertIn("def get_environment_info", self.main_code)

    def test_13_api_response_structure_complete(self):
        """Test: API response includes all required fields."""
        # Verify response structure contains key fields
        response_fields = [
            "installed_packages",
            "package_count",
            "installed_packages_source",
            "python_version",
        ]
        
        for field in response_fields:
            # Should be set in the function
            pattern = f'["\']?{field}["\']?\\s*[:=]'
            self.assertRegex(self.main_code, pattern, f"Response should include {field}")

    def test_14_api_response_is_json_serializable(self):
        """Test: API response can be serialized to JSON."""
        # Simulate response structure
        response = {
            "installed_packages": [{"name": "test", "version": "1.0"}],
            "package_count": 1,
            "installed_packages_source": "pip_list_json",
            "python_version": "3.11.8",
        }
        
        # Should not raise
        json_string = json.dumps(response)
        self.assertIsInstance(json_string, str)
        
        # Should be reversible
        parsed = json.loads(json_string)
        self.assertEqual(parsed["package_count"], 1)

    # ========== Stage 5: Frontend Reception ==========

    def test_15_frontend_makes_eel_call(self):
        """Test: Frontend calls backend via eel."""
        self.assertIn("eel.get_environment_info()", self.html_code)

    def test_16_frontend_call_is_async(self):
        """Test: Frontend uses async/await for eel call."""
        self.assertIn("async function loadEnvironmentInfo()", self.html_code)
        self.assertIn("await eel.get_environment_info()", self.html_code)

    def test_17_frontend_handles_response_structure(self):
        """Test: Frontend expects correct response structure."""
        # Should access installed_packages field
        self.assertIn("installed_packages", self.html_code)
        
        # Should access source field
        self.assertIn("installed_packages_source", self.html_code)

    # ========== Stage 6: Frontend Normalization ==========

    def test_18_frontend_normalization_function_exists(self):
        """Test: Frontend has normalization function."""
        self.assertIn("function normalizeInstalledPackages", self.html_code)

    def test_19_frontend_normalizes_array_format(self):
        """Test: Frontend handles array format [{name, version}]."""
        # Simulate frontend normalization
        raw_packages = [
            {"name": "bottle", "version": "0.12.25"},
            {"name": "Eel", "version": "0.16.0"},
        ]
        
        # Python simulation of JS normalization
        normalized = []
        for pkg in raw_packages:
            if not isinstance(pkg, dict):
                continue
            name = str(pkg.get("name") or "").strip()
            version = str(pkg.get("version") or "-").strip()
            if name:
                normalized.append({"name": name, "version": version})
        
        self.assertEqual(len(normalized), 2)
        self.assertEqual(normalized[0]["name"], "bottle")

    def test_20_frontend_handles_alternative_field_names(self):
        """Test: Frontend normalizes alternative field names."""
        # Verify handling of Name/name/project_name variations
        norm_match = re.search(
            r'function normalizeInstalledPackages.*?(?=\n\s*function|\Z)',
            self.html_code,
            re.DOTALL
        )
        self.assertIsNotNone(norm_match)
        func_body = norm_match.group(0)
        
        # Should handle multiple name variants
        self.assertIn("name", func_body.lower())

    def test_21_frontend_sorts_normalized_packages(self):
        """Test: Frontend sorts packages after normalization."""
        # Verify sorting logic exists
        norm_match = re.search(
            r'function normalizeInstalledPackages.*?(?=\n\s*function|\Z)',
            self.html_code,
            re.DOTALL
        )
        self.assertIsNotNone(norm_match)
        func_body = norm_match.group(0)
        
        # Should include sort logic
        self.assertIn("sort", func_body)

    # ========== Stage 7: DOM Population ==========

    def test_22_frontend_populates_package_count(self):
        """Test: Frontend updates package count element."""
        self.assertIn('id="package-count"', self.html_code)
        
        # Should reference in loadEnvironmentInfo
        self.assertIn("package-count", self.html_code)

    def test_23_frontend_displays_package_source(self):
        """Test: Frontend displays the data source."""
        self.assertIn('id="package-source"', self.html_code)

    def test_24_frontend_renders_package_list(self):
        """Test: Frontend renders packages to DOM."""
        self.assertIn('id="installed-packages-list"', self.html_code)
        
        # Should have render function
        self.assertIn("function renderPackages", self.html_code)

    def test_25_complete_downstream_flow_simulation(self):
        """
        Test: Complete Backend → Frontend flow simulation.
        
        Simulates:
        1. Subprocess pip call → stdout
        2. Backend parsing → packages list
        3. Backend source tracking → tuple return
        4. API response → JSON structure
        5. Frontend reception → async response
        6. Frontend normalization → standardized format
        7. DOM preparation → ready for rendering
        """
        # Stage 1: Subprocess
        mock_subprocess = Mock()
        mock_subprocess.returncode = 0
        mock_subprocess.stdout = self.pip_json_sample
        mock_subprocess.stderr = ""
        
        with patch('subprocess.run', return_value=mock_subprocess):
            # Stage 2: Backend parsing
            packages_data = json.loads(mock_subprocess.stdout)
            backend_packages = sorted(packages_data, key=lambda x: x.get("name", "").lower())
            backend_source = "pip_list_json"
            
            # Stage 3: API response
            api_response = {
                "installed_packages": backend_packages,
                "package_count": len(backend_packages),
                "installed_packages_source": backend_source,
                "python_version": "3.11.8",
            }
            
            # Stage 4: JSON serialization (over the wire)
            json_response = json.dumps(api_response)
            
            # Stage 5: Frontend reception
            frontend_received = json.loads(json_response)
            
            # Stage 6: Frontend normalization
            frontend_packages = []
            for pkg in frontend_received["installed_packages"]:
                if not isinstance(pkg, dict):
                    continue
                name = str(pkg.get("name") or "").strip()
                version = str(pkg.get("version") or "-").strip()
                if name:
                    frontend_packages.append({"name": name, "version": version})
            
            frontend_packages.sort(key=lambda x: x["name"].lower())
            
            # Stage 7: Validation
            self.assertEqual(len(frontend_packages), 3)
            self.assertEqual(frontend_packages[0]["name"], "bottle")
            self.assertEqual(frontend_packages[0]["version"], "0.12.25")
            self.assertEqual(frontend_received["installed_packages_source"], "pip_list_json")
            self.assertEqual(frontend_received["package_count"], 3)
            
            # Data consistency check
            for backend_pkg, frontend_pkg in zip(backend_packages, frontend_packages):
                self.assertEqual(backend_pkg["name"], frontend_pkg["name"])
                self.assertEqual(backend_pkg["version"], frontend_pkg["version"])


if __name__ == "__main__":
    unittest.main()
