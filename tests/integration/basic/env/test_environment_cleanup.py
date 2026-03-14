#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Environment Cleanup Test
# Eingabewerte: Legacy database locations
# Ausgabewerte: Cleanup results
# Testdateien: ~/.media-web-viewer/media_library.db
# Kommentar: Testet Environment-Cleanup.
#!/usr/bin/env python3
"""
Test suite for environment cleanliness and database isolation.

Category: Environment & Database Hygiene
Status: Active
Version: 1.2.23

Ensures no stale local/legacy databases pollute the active environment,
and validates scan directory sanitization.

Test Suite Statistics:
- Total Test Classes: 2
- Total Test Cases: 7
- Focus Areas:
  1) Legacy DB detection/cleanup
  2) Scan directory sanitization
"""

import os
import sys
import tempfile
import unittest
from pathlib import Path

# Ensure project root is in path

import src.core.db as db
from src.parsers.format_utils import sanitize_scan_dirs, get_default_scan_dir

class TestDatabaseHygiene(unittest.TestCase):
    """
    Tests: 4
    Focus: Active DB isolation and legacy DB cleanup
    """

    def test_active_db_is_user_data_path(self):
        """Active DB must be in ~/.media-web-viewer/media_library.db."""
        active = db.get_active_db_path()
        expected = (Path.home() / ".media-web-viewer" / "media_library.db").resolve()
        self.assertEqual(active, expected)

    def test_list_legacy_databases_excludes_active(self):
        """Legacy DB list must never include the active DB."""
        active = db.get_active_db_path()
        active.parent.mkdir(parents=True, exist_ok=True)
        if not active.exists():
            active.touch()

        with tempfile.TemporaryDirectory() as tmp:
            legacy = Path(tmp) / "media_library.db"
            legacy.touch()
            found = db.list_legacy_databases(candidates=[active, legacy])
            self.assertIn(legacy.resolve(), found)
            self.assertNotIn(active.resolve(), found)

    def test_cleanup_legacy_databases_removes_only_legacy(self):
        """Cleanup should delete legacy DB files but keep active DB untouched."""
        active = db.get_active_db_path()
        active.parent.mkdir(parents=True, exist_ok=True)
        if not active.exists():
            active.touch()

        with tempfile.TemporaryDirectory() as tmp:
            legacy = Path(tmp) / "media_library.db"
            legacy.touch()

            deleted = db.cleanup_legacy_databases(candidates=[active, legacy])
            self.assertIn(str(legacy.resolve()), deleted)
            self.assertTrue(active.exists())
            self.assertFalse(legacy.exists())

    def test_get_legacy_db_candidates_contains_common_paths(self):
        """Candidate generation should include common historical DB locations."""
        with tempfile.TemporaryDirectory() as home_tmp, tempfile.TemporaryDirectory() as proj_tmp:
            candidates = db.get_legacy_db_candidates(
                home_dir=Path(home_tmp),
                project_root=Path(proj_tmp),
                cwd=Path(proj_tmp),
            )
            as_set = {str(p) for p in candidates}
            self.assertIn(str((Path(home_tmp) / "media_library.db").resolve()), as_set)
            self.assertIn(str((Path(proj_tmp) / "media_library.db").resolve()), as_set)
            self.assertIn(str((Path(proj_tmp) / "dist" / "media_library.db").resolve()), as_set)

class TestScanDirectorySanitization(unittest.TestCase):
    """
    Tests: 3
    Focus: Prevent internal/project folders from being scanned as media sources
    """

    def test_sanitize_scan_dirs_removes_invalid_entries(self):
        """Non-existing and empty scan dirs must be removed."""
        with tempfile.TemporaryDirectory() as tmp:
            valid_dir = Path(tmp) / "music"
            valid_dir.mkdir(parents=True, exist_ok=True)
            sanitized = sanitize_scan_dirs(["", "   ", str(valid_dir), str(Path(tmp) / "missing")])
            self.assertIn(str(valid_dir.resolve()), sanitized)
            self.assertNotIn(str((Path(tmp) / "missing").resolve()), sanitized)

    def test_sanitize_scan_dirs_deduplicates_entries(self):
        """Duplicate scan dirs should only appear once."""
        with tempfile.TemporaryDirectory() as tmp:
            valid_dir = Path(tmp) / "audio"
            valid_dir.mkdir(parents=True, exist_ok=True)
            sanitized = sanitize_scan_dirs([str(valid_dir), str(valid_dir)])
            self.assertEqual(sanitized.count(str(valid_dir.resolve())), 1)

    def test_sanitize_scan_dirs_blocks_internal_project_dirs(self):
        """Project internal dirs like logbuch/dist must be filtered out."""
        project_root = Path(__file__).parents[3].parent
        logbuch_dir = project_root / "logbuch"
        dist_dir = project_root / "dist"

        input_dirs = [str(logbuch_dir), str(dist_dir)]
        sanitized = sanitize_scan_dirs(input_dirs)
        self.assertNotIn(str(logbuch_dir.resolve()), sanitized)
        self.assertNotIn(str(dist_dir.resolve()), sanitized)
        self.assertIn(str(get_default_scan_dir()), sanitized)

if __name__ == '__main__':
    print("=" * 70)
    print("ENVIRONMENT CLEANUP TEST SUITE")
    print("=" * 70)
    print("\nRunning database hygiene and scan-dir sanitization tests...\n")
    unittest.main(verbosity=2)
