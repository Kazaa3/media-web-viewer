import unittest
from models import MediaItem
from pathlib import Path

class TestMediaItem(unittest.TestCase):
    def test_init(self):
        item = MediaItem("test.mp3", str(Path("test.mp3")))
        self.assertEqual(item.name, "test.mp3")
        self.assertTrue(hasattr(item, "tags"))
        self.assertTrue(hasattr(item, "category"))
        self.assertTrue(hasattr(item, "logical_type"))
        self.assertTrue(hasattr(item, "file_format"))
        self.assertTrue(hasattr(item, "content_type"))
        self.assertTrue(hasattr(item, "art_path"))
        self.assertTrue(hasattr(item, "has_artwork"))
        self.assertTrue(hasattr(item, "is_missing_cover"))
        self.assertTrue(hasattr(item, "extension"))
        self.assertTrue(hasattr(item, "media_type"))
        self.assertTrue(hasattr(item, "container"))
        self.assertTrue(hasattr(item, "tag_type"))
        self.assertTrue(hasattr(item, "codec"))

if __name__ == '__main__':
    unittest.main()
