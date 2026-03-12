#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import importlib.util
import re
import sys
import unittest
from pathlib import Path

class TestCorePackagesFourTargeted(unittest.TestCase):
    """Focused checks for the 4 requested core packages."""

    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).parents[3]
        cls.requirements_path = cls.root / "requirements.txt"
        cls.requirements_text = cls.requirements_path.read_text(encoding="utf-8")

        main_path = cls.root / "src.core.main.py"
        spec = importlib.util.spec_from_file_location("main", str(main_path))
        module = importlib.util.module_from_spec(spec)
        sys.modules["main"] = module
        spec.loader.exec_module(module)
        cls.env_info = module.get_environment_info(True)

        cls.target_packages = [
            "bottle",
            "bottle-websocket",
            "eel",
            "m3u8",
        ]

    def test_01_requirements_contains_exact_targets(self):
        """requirements.txt must include all four requested packages."""
        normalized = self.__class__.requirements_text.lower()
        for package_name in self.__class__.target_packages:
            pattern = rf"^\s*{re.escape(package_name)}\s*(?:[<>=!~]|$)"
            self.assertIsNotNone(
                re.search(pattern, normalized, re.MULTILINE),
                msg=f"requirements.txt should contain {package_name}",

    def test_02_backend_requirements_status_mentions_targets(self):
        """Backend requirements_status must mention each target package."""
        req_status = (self.__class__.env_info or {}).get("requirements_status") or {}
        installed = [str(item).lower() for item in (req_status.get("installed") or [])]
        missing = [str(item).lower() for item in (req_status.get("missing") or [])]

        def package_seen(package_name: str) -> bool:
            return any(entry.startswith(package_name) for entry in installed + missing)

        for package_name in self.__class__.target_packages:
            self.assertTrue(
                package_seen(package_name),
                msg=f"requirements_status should include {package_name}",

    def test_03_backend_has_no_missing_targets(self):
        """All four requested packages should currently be installed."""
        req_status = (self.__class__.env_info or {}).get("requirements_status") or {}
        missing = [str(item).lower() for item in (req_status.get("missing") or [])]

        for package_name in self.__class__.target_packages:
            self.assertFalse(
                any(entry.startswith(package_name) for entry in missing),
                msg=f"target package should not be missing: {package_name}",

if __name__ == "__main__":
    unittest.main()
