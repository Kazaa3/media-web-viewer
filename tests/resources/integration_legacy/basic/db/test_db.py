#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Database Integration Test
# Eingabewerte: SQLite-Datenbank (Pfad-Konfiguration)
# Ausgabewerte: Pfad-Objekte, Legacy-DB Listen
# Testdateien: src/core/db.py
# ERWEITERUNGEN (TODO): [ ] DB-Migrationstests, [ ] Pfad-Validierung unter Windows
# KOMMENTAR: Tests for database path discovery and legacy DB handling.
# VERWENDUNG: python3 tests/integration/basic/db/test_db.py

"""
KATEGORIE: Database Integration Test
ZWECK: Testet die Datenbank-Pfadfindung und das Handling von Legacy-Datenbanken.
EINGABEWERTE: SQLite-Datenbank (Pfad-Konfiguration)
AUSGABEWERTE: Pfad-Objekte, Legacy-DB Listen
TESTDATEIEN: src/core/db.py
ERWEITERUNGEN (TODO): [ ] DB-Migrationstests, [ ] Pfad-Validierung unter Windows
KOMMENTAR: Tests for database path discovery and legacy DB handling.
VERWENDUNG: python3 tests/integration/basic/db/test_db.py
"""

import unittest
import src.core.db as db
from pathlib import Path

class TestDB(unittest.TestCase):
    def test_get_active_db_path(self):
        path = db.get_active_db_path()
        self.assertIsInstance(path, Path)
        self.assertTrue(str(path).endswith("media_library.db"))

    def test_get_legacy_db_candidates(self):
        candidates = db.get_legacy_db_candidates()
        self.assertIsInstance(candidates, list)
        self.assertTrue(all(isinstance(p, Path) for p in candidates))

    def test_list_legacy_databases(self):
        existing = db.list_legacy_databases()
        self.assertIsInstance(existing, list)
        self.assertTrue(all(isinstance(p, Path) for p in existing))

    def test_cleanup_legacy_databases(self):
        deleted = db.cleanup_legacy_databases([])
        self.assertIsInstance(deleted, list)

if __name__ == '__main__':
    unittest.main()
