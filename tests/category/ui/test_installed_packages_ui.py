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
        self.root = Path(__file__).parents[3]
        self.app_html_path = self.root / "web" / "app.html"
        self.i18n_path = self.root / "web" / "i18n.json"

        self.app_html = self.app_html_path.read_text(encoding="utf-8")
        self.i18n = json.loads(self.i18n_path.read_text(encoding="utf-8"))

    def test_installed_packages_block_exists(self):
        """Installed Packages section and key element IDs must exist."""
        self.assertIn('data-i18n="options_installed_packages"', self.app_html)
        self.assertIn('id="package-count"', self.app_html)
        self.assertIn('id="package-source"', self.app_html)
        self.assertIn('id="package-search"', self.app_html)
        self.assertIn('id="installed-packages-list"', self.app_html)
        self.assertIn('data-i18n="options_requirements_status"', self.app_html)
        self.assertIn('data-i18n="options_requirements_refresh"', self.app_html)
        self.assertIn('id="requirements-count"', self.app_html)
        self.assertIn('id="requirements-last-checked"', self.app_html)
        self.assertIn('id="requirements-status-list"', self.app_html)
        self.assertIn('id="system-python-global-list"', self.app_html)
        self.assertIn('id="system-python-local-list"', self.app_html)
        self.assertIn('id="env-mutagen-status"', self.app_html)
        self.assertIn('id="env-ffmpeg-status"', self.app_html)
        self.assertIn('id="env-ffprobe-status"', self.app_html)
        self.assertIn('id="env-gui-status"', self.app_html)
        self.assertIn('id="env-mediaplayer-status"', self.app_html)
        self.assertIn('id="env-core-packages-status"', self.app_html)
        self.assertIn('id="env-test-tools-status"', self.app_html)
        self.assertIn('id="env-dev-tools-status"', self.app_html)
        self.assertIn('id="env-build-tools-status"', self.app_html)
        self.assertIn('id="env-requirements-list"', self.app_html)
        self.assertIn('id="env-base-dependencies-status"', self.app_html)

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
        if match is None:
            self.fail("installed-packages-list container not found")
        self.assertIn('data-i18n="common_loading_short"', match.group(1))

    def test_js_load_environment_info_updates_packages_section(self):
        """JS must wire package list rendering and search behavior."""
        required_snippets = [
            "const packagesList = document.getElementById('installed-packages-list');",
            "const packageCount = document.getElementById('package-count');",
            "const packageSource = document.getElementById('package-source');",
            "const sourceText = String(info.installed_packages_source || 'unknown');",
            "if (packageSource) packageSource.textContent = `[source: ${sourceText}]`;",
            "window.allPackages = safeInstalledPackages;",
            "window.allPackagesSearch = safeInstalledPackages.map(pkg => ({",
            "renderPackages(safeInstalledPackages);",
            "const requirementsCount = document.getElementById('requirements-count');",
            "const requirementsLastChecked = document.getElementById('requirements-last-checked');",
            "const requirementsStatusList = document.getElementById('requirements-status-list');",
            "const envMutagenStatusEl = document.getElementById('env-mutagen-status');",
            "const envFfmpegStatusEl = document.getElementById('env-ffmpeg-status');",
            "const envFfprobeStatusEl = document.getElementById('env-ffprobe-status');",
            "const envGuiStatusEl = document.getElementById('env-gui-status');",
            "const envMediaplayerStatusEl = document.getElementById('env-mediaplayer-status');",
            "const envBaseDependenciesStatusEl = document.getElementById('env-base-dependencies-status');",
            "const envCorePackagesStatusEl = document.getElementById('env-core-packages-status');",
            "const ffmpegVer = toolsStatus.ffmpeg_cli_version || '';",
            "const ffprobeVer = toolsStatus.ffprobe_cli_version || '';",
            "const browserVer = toolsStatus.browser_version || '';",
            "const corePackages = [",
            "['bottle', 'bottle']",
            "['bottle-websocket', 'bottle-websocket']",
            "['eel', 'Eel']",
            "['m3u8', 'm3u8']",
            "['gevent', 'gevent']",
            "['greenlet', 'greenlet']",
            "const testPackages = [",
            "const vlcCliVer = toolsStatus.vlc_cli_version || '';",
            "['pytest', 'pytest']",
            "['pytest-cov', 'pytest-cov']",
            "['coverage', 'coverage']",
            "['pyautogui', 'PyAutoGUI']",
            "const devPackages = [",
            "['mypy', 'mypy']",
            "['flake8', 'flake8']",
            "['pycodestyle', 'pycodestyle']",
            "const buildPackages = [",
            "['pyinstaller', 'PyInstaller']",
            "['wheel', 'wheel']",
            "['setuptools', 'setuptools']",
            "['packaging', 'packaging']",
            "['psutil', 'psutil']",
            "const categorizedKeys = new Set([",
            "const baseDependencies = safeInstalledPackages",
            "const baseDependenciesText = baseDependencies.length > 0",
            "const requirementsListText = requirementsStatusPreview?.available",
            "const requirementsStatus = info.requirements_status && typeof info.requirements_status === 'object'",
            "requirementsCount.textContent = `(${installedCount}/${total})`;",
            "requirementsLastChecked.textContent = `${t('env_requirements_last_checked')}: ${now.toLocaleTimeString()}`;",
            "onclick=\"loadEnvironmentInfo(true)\"",
            "const requestForceRefresh = !!forceRefresh;",
            "const searchInput = document.getElementById('package-search');",
            "searchInput.addEventListener('input', (e) => {",
            "if (packageSearchTimer) clearTimeout(packageSearchTimer);",
            "renderPackages(window.allPackages);",
            ".filter(row => row.nameLc.includes(searchTerm) || row.versionLc.includes(searchTerm))",
            "const globalPythonList = document.getElementById('system-python-global-list');",
            "const localPythonList = document.getElementById('system-python-local-list');",
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
            "const safeInstalledPackages = normalizeInstalledPackages(info.installed_packages);",
            "function normalizeInstalledPackages(rawPackages) {",
            "const failText = `<span style=\"color: #c62828;\">${t('common_error_loading')}</span>`;",
            "const fallbackNoData = `<span style=\"color: #999;\">${t('env_no_packages_found')}</span>`;",
            "if (packageSource) packageSource.textContent = '[source: error]';",
            "if (requirementsCount) requirementsCount.textContent = '(0/0)';",
            "if (requirementsLastChecked) requirementsLastChecked.textContent = t('env_requirements_last_checked_error');",
            "if (requirementsStatusList) requirementsStatusList.innerHTML = failText;",
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
            "options_requirements_status",
            "options_requirements_refresh",
            "env_requirements_not_found",
            "env_requirements_all_present",
            "env_requirements_missing",
            "env_requirements_last_checked",
            "env_requirements_last_checked_never",
            "env_requirements_last_checked_error",
            "env_label_mutagen",
            "env_label_ffmpeg",
            "env_label_ffprobe",
            "env_label_gui",
            "env_label_mediaplayer",
            "env_label_core_packages",
            "env_label_test_tools",
            "env_label_dev_tools",
            "env_label_build_tools",
            "env_label_requirements_list",
            "env_label_base_dependencies",
            "env_table_package",
            "env_table_version",
        ]

        for lang in ("de", "en"):
            self.assertIn(lang, self.i18n, f"Missing language block: {lang}")
            for key in required_keys:
                self.assertIn(key, self.i18n[lang], f"Missing i18n key '{key}' in language '{lang}'")

if __name__ == "__main__":
    unittest.main()
