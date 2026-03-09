#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Release Workflow Test
# Eingabewerte: .github/workflows/release.yml
# Ausgabewerte: Validierte Release-Workflow-Schritte
# Testdateien: .github/workflows/release.yml
# Kommentar: Prüft den Windows-.exe Release-Flow mit mehreren Zwischenschritten.

import re
import unittest
from pathlib import Path


class TestReleaseWorkflowSteps(unittest.TestCase):
    """Step-by-step validation for GitHub release workflow."""

    @classmethod
    def setUpClass(cls):
        cls.root = Path(__file__).parent.parent
        cls.workflow_path = cls.root / ".github" / "workflows" / "release.yml"
        cls.content = cls.workflow_path.read_text(encoding="utf-8")

    def _job_block(self, job_name: str) -> str:
        pattern = rf"^  {re.escape(job_name)}:\n(?P<body>.*?)(?=^  [a-zA-Z0-9_-]+:\n|\Z)"
        match = re.search(pattern, self.content, flags=re.MULTILINE | re.DOTALL)
        self.assertIsNotNone(match, f"Job block '{job_name}' not found")
        return match.group("body")

    def test_step_01_workflow_basics(self):
        """Step 1: Workflow exists and has required triggers/permissions."""
        self.assertTrue(self.workflow_path.exists(), "release.yml does not exist")
        self.assertIn("name: Build and Release", self.content)
        self.assertIn("tags:", self.content)
        self.assertIn("- 'v*'", self.content)
        self.assertIn("permissions:", self.content)
        self.assertIn("contents: write", self.content)

    def test_step_02_windows_job_builds_exe(self):
        """Step 2: Windows job builds .exe and uploads it as artifact."""
        windows = self._job_block("build-windows")
        self.assertIn("runs-on: windows-latest", windows)
        self.assertIn("Build Windows Executable", windows)
        self.assertIn("python -m PyInstaller", windows)
        self.assertIn('--name "MediaWebViewer-${VERSION}-Windows"', windows)
        self.assertIn("Upload Windows Executable", windows)
        self.assertIn("path: dist/*.exe", windows)
        self.assertIn("if-no-files-found: error", windows)

    def test_step_03_release_gate_depends_on_windows_success(self):
        """Step 3: create-release must run when Windows build succeeds."""
        create = self._job_block("create-release")
        self.assertIn("needs: [build-linux, build-windows]", create)
        self.assertIn("if: ${{ always() && needs.build-windows.result == 'success' }}", create)

    def test_step_04_release_upload_is_resilient(self):
        """Step 4: Release upload must tolerate missing optional artifacts and allow overwrite."""
        create = self._job_block("create-release")
        self.assertIn("uses: softprops/action-gh-release@v2", create)
        self.assertIn("fail_on_unmatched_files: false", create)
        self.assertIn("overwrite_files: true", create)

    def test_step_05_release_files_include_windows_asset(self):
        """Step 5: Release file globs must include Windows artifacts."""
        create = self._job_block("create-release")
        self.assertIn("artifacts/MediaWebViewer-Windows/*", create)

    def test_step_06_linux_job_is_non_blocking(self):
        """Step 6: Linux job errors should not block release creation."""
        linux = self._job_block("build-linux")
        self.assertIn("continue-on-error: true", linux)


if __name__ == "__main__":
    unittest.main(verbosity=2)
