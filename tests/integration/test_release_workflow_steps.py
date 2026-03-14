#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Release Workflow Test
# Eingabewerte: .github/workflows/release.yml
# Ausgabewerte: Validierte Release-Workflow-Schritte
# Testdateien: .github/workflows/release.yml
# Kommentar: Prüft den Windows-.exe Release-Flow mit mehreren Zwischenschritten.
"""
Release Workflow Test Suite (DE/EN)
===================================

DE:
Testet den Release-Workflow für Windows- und Linux-Builds sowie die Artefakt-Validierung.

EN:
Tests the release workflow for Windows and Linux builds and artifact validation.

Autor/Author: Media Web Viewer Team
Erstellt/Created: 2026-03-13
Version: 1.0.0
"""

import re
import unittest
from pathlib import Path

class TestReleaseWorkflowSteps(unittest.TestCase):
    """
    DE:
    Validiert die einzelnen Schritte des Release-Workflows.

    EN:
    Validates each step of the release workflow.
    """
    @classmethod
    def setUpClass(cls):
        """
        DE:
        Lädt die Workflow-Datei und deren Inhalt.

        EN:
        Loads the workflow file and its content.
        """
        cls.root = Path(__file__).parents[3]
        cls.workflow_path = cls.root / ".github" / "workflows" / "release.yml"
        cls.content = cls.workflow_path.read_text(encoding="utf-8")

    def _job_block(self, job_name: str) -> str:
        """
        DE:
        Extrahiert einen Job-Block aus der Workflow-Datei.

        EN:
        Extracts a job block from the workflow file.
        Returns:
            str: Job-Block-Inhalt.
        Raises:
            AssertionError: Wenn Block nicht gefunden.
        """
        pattern = rf"^  {re.escape(job_name)}:\n(?P<body>.*?)(?=^  [a-zA-Z0-9_-]+:\n|\Z)"
        match = re.search(pattern, self.content, flags=re.MULTILINE | re.DOTALL)
        self.assertIsNotNone(match, f"Job block '{job_name}' not found")
        return match.group("body")

    def test_step_01_workflow_basics(self):
        """
        DE:
        Prüft grundlegende Workflow-Trigger und Berechtigungen.

        EN:
        Checks basic workflow triggers and permissions.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Trigger/Berechtigungen fehlen.
        """
        self.assertTrue(self.workflow_path.exists(), "release.yml does not exist")
        self.assertIn("name: Build and Release", self.content)
        self.assertIn("tags:", self.content)
        self.assertIn("- 'v*'", self.content)
        self.assertIn("permissions:", self.content)
        self.assertIn("contents: write", self.content)

    def test_step_02_windows_job_builds_exe(self):
        """
        DE:
        Prüft, ob der Windows-Job das .exe baut und als Artefakt hochlädt.

        EN:
        Checks if the Windows job builds the .exe and uploads it as artifact.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Build/Upload fehlt.
        """
        windows = self._job_block("build-windows")
        self.assertIn("runs-on: windows-latest", windows)
        self.assertIn("Build Windows Executable", windows)
        self.assertIn("python -m PyInstaller", windows)
        self.assertIn('--name "MediaWebViewer-${VERSION}-Windows"', windows)
        self.assertIn("Upload Windows Executable", windows)
        self.assertIn("path: dist/*.exe", windows)
        self.assertIn("if-no-files-found: error", windows)

    def test_step_03_release_gate_depends_on_windows_success(self):
        """
        DE:
        Prüft, ob create-release nach erfolgreichem Windows-Build läuft.

        EN:
        Checks if create-release runs after successful Windows build.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Abhängigkeit fehlt.
        """
        create = self._job_block("create-release")
        self.assertIn("needs: [build-linux, build-windows]", create)
        self.assertIn("if: ${{ always() && needs.build-windows.result == 'success' }}", create)

    def test_step_04_release_upload_is_resilient(self):
        """
        DE:
        Prüft, ob Release-Upload fehlende Artefakte toleriert und Überschreiben erlaubt.

        EN:
        Checks if release upload tolerates missing artifacts and allows overwrite.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Upload nicht resilient.
        """
        create = self._job_block("create-release")
        self.assertIn("uses: softprops/action-gh-release@v2", create)
        self.assertIn("fail_on_unmatched_files: false", create)
        self.assertIn("overwrite_files: true", create)

    def test_step_05_release_files_include_windows_asset(self):
        """
        DE:
        Prüft, ob Release-Dateien Windows-Artefakte enthalten.

        EN:
        Checks if release files include Windows artifacts.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Artefakte fehlen.
        """
        create = self._job_block("create-release")
        self.assertIn("artifacts/MediaWebViewer-Windows/*", create)

    def test_step_06_linux_job_is_non_blocking(self):
        """
        DE:
        Prüft, ob Linux-Job Fehler toleriert und Release nicht blockiert.

        EN:
        Checks if Linux job tolerates errors and does not block release.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Fehler nicht toleriert.
        """
        linux = self._job_block("build-linux")
        self.assertIn("continue-on-error: true", linux)

if __name__ == "__main__":
    unittest.main(verbosity=2)
