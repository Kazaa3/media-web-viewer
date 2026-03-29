import sys
import os
import unittest
from pathlib import Path

# Fix imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))

from src.core import db
from src.core.main import get_library, get_library_filtered

class TestDynamicLoading(unittest.TestCase):
    def setUp(self):
        db.init_db()
        db.clear_media()

    def test_library_updates_on_insert(self):
        """Verifies that get_library correctly reflects new items after insertion."""
        # 1. Initially empty
        lib = get_library()
        self.assertEqual(len(lib['media']), 0, "Library should be empty initially")

        # 2. Insert one item
        mock_item = {
            'name': 'Dynamic Test Video',
            'path': '/tmp/test.mp4',
            'type': 'video/mp4',
            'duration': '00:10:00',
            'is_transcoded': 0,
            'category': 'Film',
            'tags': {'genre': 'Test', 'year': '2024'}
        }
        db.insert_media(mock_item)
        
        # 3. Verify item exists in library
        lib = get_library()
        self.assertEqual(len(lib['media']), 1, "Library should have 1 item after insertion")
        self.assertEqual(lib['media'][0]['name'], 'Dynamic Test Video')

    def test_advanced_filtering(self):
        """Verifies server-side filtering logic."""
        # Insert two items
        base = {'type': 'video/mp4', 'duration': '00:10:00', 'is_transcoded': 0}
        db.insert_media({**base, 'name': 'Alpha', 'path': '/tmp/a.mp4', 'category': 'Film', 'tags': {'genre': 'Action', 'year': '2020'}})
        db.insert_media({**base, 'name': 'Beta', 'path': '/tmp/b.mp4', 'category': 'Film', 'tags': {'genre': 'Comedy', 'year': '2022'}})
        
        # Filter by Genre
        lib = get_library_filtered(genre='Action')
        self.assertEqual(len(lib['media']), 1)
        self.assertEqual(lib['media'][0]['name'], 'Alpha')
        
        # Filter by Year
        lib = get_library_filtered(year='2022')
        self.assertEqual(len(lib['media']), 1)
        self.assertEqual(lib['media'][0]['name'], 'Beta')
        
        # Search query
        lib = get_library_filtered(search='BET')
        self.assertEqual(len(lib['media']), 1)
        self.assertEqual(lib['media'][0]['name'], 'Beta')

if __name__ == "__main__":
    unittest.main()
