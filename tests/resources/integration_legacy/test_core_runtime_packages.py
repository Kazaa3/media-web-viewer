#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import importlib.util
import re
import sys
import unittest
from pathlib import Path

class TestCoreRuntimePackages(unittest.TestCase):
    """Regression checks for core runtime packages requested by user."""

    def setUp(self):
        self.root = Path(__file__).parents[3]
        self.requirements_path = self.root / "requirements.txt"
        self.main_path = self.root / "src/core/main.py"
        self.requirements_text = self.requirements_path.read_text(encoding="utf-8")
        self.main_code = self.main_path.read_text(encoding="utf-8")
        self.core_packages = [
            "bottle",
            "bottle-websocket",
            "eel",
            "m3u8",
            "gevent",
            "gevent-websocket",
        ]

    @classmethod
    def setUpClass(cls):
        root = Path(__file__).parents[3]
        main_path = root / "src/core/main.py"
        spec = importlib.util.spec_from_file_location("main", str(main_path))
        module = importlib.util.module_from_spec(spec)
        sys.modules["main"] = module
        spec.loader.exec_module(module)
        cls.env_info = module.get_environment_info(True)

    def test_01_requirements_contains_core_packages(self):
        """Ensure requirements.txt contains the requested core packages."""
        normalized = self.requirements_text.lower()
        for package_name in self.core_packages:
            pattern = rf"^\s*{re.escape(package_name)}\s*(?:[<>=!~]|$)"
            self.assertIsNotNone(
                re.search(pattern, normalized, re.MULTILINE),
                msg=f"requirements.txt should contain {package_name}"
            )

    def test_02_runtime_requirements_status_reports_core_packages(self):
        """Ensure get_environment_info().requirements_status reports all core packages."""
        result = self.__class__.env_info
        req_status = result.get("requirements_status") or {}
        installed = [str(x).lower() for x in (req_status.get("installed") or [])]
        missing = [str(x).lower() for x in (req_status.get("missing") or [])]
        seen = set(installed + missing)

        for package_name in self.core_packages:
            self.assertIn(
                package_name,
                seen,
                msg=f"requirements_status should include {package_name} in installed or missing"
            )

    def test_03_runtime_has_no_missing_core_packages(self):
        """Ensure core packages are currently installed in the active runtime."""
        result = self.__class__.env_info
        req_status = result.get("requirements_status") or {}
        missing = {str(x).lower() for x in (req_status.get("missing") or [])}

        for package_name in self.core_packages:
            self.assertNotIn(
                package_name,
                missing,
                msg=f"core package should be installed but is missing: {package_name}"
            )

if __name__ == "__main__":
    unittest.main()
