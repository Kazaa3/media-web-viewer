import unittest
import db
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
