#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: UI / Environment Packages Element Test
# Eingabewerte: web/app.html, web/i18n.json
# Ausgabewerte: Validierung für Installed-Packages-Element, Search-Feld, Loading-Status
# Testdateien: web/app.html, web/i18n.json
# Kommentar: Testet das UI-Element "Installed Packages" inklusive Search-Input und initialem Loading-Text.

import json
import re
import unittest
from pathlib import Path


class TestInstalledPackagesUI(unittest.TestCase):
    """Validates Installed Packages UI block in Options > Environment."""

    def setUp(self):
        self.root = Path(__file__).parent.parent
        self.app_html_path = self.root / "web" / "app.html"
        self.i18n_path = self.root / "web" / "i18n.json"

        self.app_html = self.app_html_path.read_text(encoding="utf-8")
        self.i18n = json.loads(self.i18n_path.read_text(encoding="utf-8"))

    def test_installed_packages_block_exists(self):
        """Installed Packages section and key element IDs must exist."""
        self.assertIn('data-i18n="options_installed_packages"', self.app_html)
        self.assertIn('id="package-count"', self.app_html)
        self.assertIn('id="package-search"', self.app_html)
        self.assertIn('id="installed-packages-list"', self.app_html)

    def test_search_input_has_i18n_placeholder_binding(self):
        """Search input must bind placeholder via i18n key."""
        pattern = r'id="package-search"[^>]*data-i18n="\[placeholder\]packages_search_placeholder"'
        self.assertRegex(self.app_html, pattern)

    def test_loading_state_uses_common_loading_key(self):
        """Installed packages list must show common loading key initially."""
        match = re.search(
            r'id="installed-packages-list"[^>]*>(.*?)</div>',
            self.app_html,
            re.DOTALL,
        )
        if match is None:
            self.fail("installed-packages-list container not found")
        self.assertIn('data-i18n="common_loading_short"', match.group(1))

    def test_js_load_environment_info_updates_packages_section(self):
        """JS must wire package list rendering and search behavior."""
        required_snippets = [
            "const packagesList = document.getElementById('installed-packages-list');",
            "const packageCount = document.getElementById('package-count');",
            "window.allPackages = safeInstalledPackages;",
            "renderPackages(safeInstalledPackages);",
            "const searchInput = document.getElementById('package-search');",
            "searchInput.addEventListener('input', (e) => {",
            "renderPackages(window.allPackages);",
            "window.allPackages.filter(pkg =>",
            "packagesList.innerHTML = `<span style=\"color: #999;\">${t('env_no_packages_found')}</span>`;",
        ]
        for snippet in required_snippets:
            self.assertIn(snippet, self.app_html)

    def test_js_load_environment_info_has_timeout_and_error_fallback(self):
        """Environment loading must not remain stuck in Loading... on backend failure."""
        required_snippets = [
            "if (!info || typeof info !== 'object')",
            "const safeCondaEnvs = Array.isArray(info.available_conda_environments) ? info.available_conda_environments : [];",
            "const safeSystemPythons = Array.isArray(info.available_system_pythons) ? info.available_system_pythons : [];",
            "const safeLocalVenvs = Array.isArray(info.local_venvs) ? info.local_venvs : [];",
            "const safeInstalledPackages = Array.isArray(info.installed_packages) ? info.installed_packages : [];",
            "const failText = `<span style=\"color: #c62828;\">${t('common_error_loading')}</span>`;",
            "const fallbackNoData = `<span style=\"color: #999;\">${t('env_no_packages_found')}</span>`;",
            "if (packagesList) packagesList.innerHTML = fallbackNoData;",
        ]
        for snippet in required_snippets:
            self.assertIn(snippet, self.app_html)

    def test_i18n_keys_for_installed_packages_exist_de_en(self):
        """DE and EN must both include required package-related i18n keys."""
        required_keys = [
            "options_installed_packages",
            "packages_search_placeholder",
            "common_loading_short",
            "env_no_packages_found",
            "env_no_matching_packages",
            "env_table_package",
            "env_table_version",
        ]

        for lang in ("de", "en"):
            self.assertIn(lang, self.i18n, f"Missing language block: {lang}")
            for key in required_keys:
                self.assertIn(key, self.i18n[lang], f"Missing i18n key '{key}' in language '{lang}'")


if __name__ == "__main__":
    unittest.main()
