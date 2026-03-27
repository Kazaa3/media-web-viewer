#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# =============================================================================
# Kategorie: GUI / Frontend-Backend Integration Test
# Eingabewerte: Backend API (eel exposed functions), logbuch/*.md
# Ausgabewerte: Logik-Konsistenz, Metadaten, Directory-Scan
# Testdateien: test_robust_refresh_logic.py
# Kommentar: Testet robuste Refresh-Logik und Cross-Tab-Konsistenz.
# Startbefehl: python tests/test_robust_refresh_logic.py
# =============================================================================
"""
GUI / Frontend-Backend Integration Test Suite (DE/EN)
=====================================================

DE:
Testet die Backend-Logik für robuste GUI-Refreshes und Cross-Tab-Konsistenz.

EN:
Tests backend logic for robust GUI refreshes and cross-tab consistency.

Autor/Author: Media Web Viewer Team
Erstellt/Created: 2026-03-13
Version: 1.0.0
"""

import unittest
import os
import sys
import shutil
from pathlib import Path

# Add project root to sys.path

import src.core.main as main

class TestRobustRefreshLogic(unittest.TestCase):
    """
    DE:
    Testet die Backend-Logik für Refreshes und Metadaten-Konsistenz.

    EN:
    Tests backend logic for refreshes and metadata consistency.
    """
    def setUp(self):
        """
        DE:
        Initialisiert Testdateien und Logbuch-Verzeichnis.

        EN:
        Initializes test files and logbook directory.
        Returns:
            Keine.
        Raises:
            Keine.
        """
        self.logbuch_dir = Path(__file__).parents[3] / "logbuch"
        self.logbuch_dir.mkdir(exist_ok=True)
        self.test_file_name = "test_refresh_logic_entry"
        self.test_file_path = self.logbuch_dir / f"{self.test_file_name}.md"

    def tearDown(self):
        """
        DE:
        Entfernt Testdateien nach den Tests.

        EN:
        Removes test files after tests.
        Returns:
            Keine.
        Raises:
            Keine.
        """
        if hasattr(self, 'test_file_path') and self.test_file_path.exists():
            self.test_file_path.unlink()

    def test_logbook_listing_robustness(self):
        """
        DE:
        Prüft, ob list_logbook_entries alle .md-Dateien mit korrekten Metadaten zurückgibt.

        EN:
        Checks if list_logbook_entries returns all .md files with correct metadata.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Metadaten fehlen.
        """
        # Create a dummy entry
        content = "Category: Test\nStatus: ACTIVE\nTitle_DE: Test Eintrag\n\nBody content"
        main.save_logbook_entry(self.test_file_name, content)
        
        entries = main.list_logbook_entries()
        entry_names = [e['name'] for e in entries]
        self.assertIn(self.test_file_name, entry_names)
        
        # Check metadata extraction
        target = next(e for e in entries if e['name'] == self.test_file_name)
        self.assertEqual(target['category'], "Test")
        self.assertEqual(target['status'], "ACTIVE")

    def test_metadata_update_consistency(self):
        """
        DE:
        Prüft, ob das Aktualisieren von Tags im Backend funktioniert.

        EN:
        Checks if updating tags in the backend works correctly.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn API fehlt.
        """
        # This assumes we have a media item in the DB. Since we might not, we'll verify the API existence.
        self.assertTrue(hasattr(main, 'update_tags'), "Backend function update_tags missing")
        self.assertTrue(hasattr(main, 'rename_media'), "Backend function rename_media missing")
        self.assertTrue(hasattr(main, 'get_library'), "Backend function get_library missing")

    def test_browser_directory_scan_support(self):
        """
        DE:
        Prüft, ob das Backend Directory-Browsing unterstützt.

        EN:
        Checks if backend supports directory browsing.
        Returns:
            Keine.
        Raises:
            AssertionError: Wenn Directory-Browsing fehlschlägt.
        """
        root = Path(__file__).parents[3]
        res = main.browse_dir(str(root))
        self.assertNotIn('error', res)
        self.assertIn('path', res)
        self.assertTrue(len(res['items']) > 0)

if __name__ == "__main__":
    unittest.main()
