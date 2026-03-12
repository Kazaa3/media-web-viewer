import unittest
from pathlib import Path
from src.core.media_format import MediaFormat

class TestMediaFormat(unittest.TestCase):
    def test_detect_type(self):
        mf = MediaFormat(Path("test.mp3"))
        self.assertEqual(mf.detect_type(), "Audio")
        mf = MediaFormat(Path("test.mp4"))
        self.assertEqual(mf.detect_type(), "Video")
        mf = MediaFormat(Path("test.iso"))
        self.assertEqual(mf.detect_type(), "ISO/Image")

    def test_to_dict(self):
        mf = MediaFormat(Path("test.mp3"))
        d = mf.to_dict()
        self.assertIn("type", d)
        self.assertIn("format", d)
        self.assertIn("content", d)
        self.assertIn("extension", d)

if __name__ == '__main__':
    unittest.main()
