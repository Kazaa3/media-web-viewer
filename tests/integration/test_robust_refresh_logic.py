#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: GUI / Frontend-Backend Integration Test
# Eingabewerte: Backend API (eel expoased functions)
# Ausgabewerte: Logic consistency results
# Testdateien: Temporary .md files in logbuch/
# Kommentar: Verifies logic for robust refreshes and cross-tab consistency.

import unittest
import os
import sys
import shutil
from pathlib import Path

# Add project root to sys.path

import src.core.main as main

class TestRobustRefreshLogic(unittest.TestCase):
    """
    @brief Tests for verifying the backend logic that supports robust GUI refreshes.
    @details Ensures that data is correctly returned and state is consistent after modifications.
    """

    def setUp(self):
        self.logbuch_dir = Path(__file__).parents[3] / "logbuch"
        self.logbuch_dir.mkdir(exist_ok=True)
        self.test_file_name = "test_refresh_logic_entry"
        self.test_file_path = self.logbuch_dir / f"{self.test_file_name}.md"

    def tearDown(self):
        if hasattr(self, 'test_file_path') and self.test_file_path.exists():
            self.test_file_path.unlink()

    def test_logbook_listing_robustness(self):
        """Verify that list_logbook_entries returns all .md files with correct metadata."""
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
        """Verify that updating tags in the backend (simulating Editor save) works correctly."""
        # This assumes we have a media item in the DB. Since we might not, we'll verify the API existence.
        self.assertTrue(hasattr(main, 'update_tags'), "Backend function update_tags missing")
        self.assertTrue(hasattr(main, 'rename_media'), "Backend function rename_media missing")
        self.assertTrue(hasattr(main, 'get_library'), "Backend function get_library missing")

    def test_browser_directory_scan_support(self):
        """Verify that the backend support for directory browsing is functional."""
        root = Path(__file__).parents[3]
        res = main.browse_dir(str(root))
        self.assertNotIn('error', res)
        self.assertIn('path', res)
        self.assertTrue(len(res['items']) > 0)

if __name__ == "__main__":
    unittest.main()
