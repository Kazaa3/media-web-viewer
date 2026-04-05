import unittest
from unittest.mock import patch, MagicMock
import os
from pathlib import Path
from src.core.main import resolve_media_path

class TestPathResolution(unittest.TestCase):
    @patch("os.path.exists")
    def test_absolute_path_exists(self, mock_exists):
        # Case: Real absolute path that exists
        mock_exists.side_effect = lambda p: p == "/media/test_video.mp4"
        path = "/media/test_video.mp4"
        resolved = resolve_media_path(path)
        self.assertIn("test_video.mp4", str(resolved))
        # Note: resolve() will return real path if it exists, otherwise it might stay relative or absolute
        # Given we mock exists to True, it should work.

    @patch("os.path.exists")
    @patch("src.core.main.db")
    def test_encoded_url_path_stripping(self, mock_db, mock_exists):
        # Case: Encoded URL path that doesn't exist initially, but exists after stripping /media/
        mock_exists.side_effect = lambda p: p == "/home/xc/test video.mp4"
        mock_db.get_media_path.return_value = None
        
        path = "/media/%2Fhome%2Fxc%2Ftest%20video.mp4"
        resolved = resolve_media_path(path)
        self.assertEqual(str(resolved), "/home/xc/test video.mp4")

    @patch("os.path.exists")
    def test_media_prefix_stripping_fallback(self, mock_exists):
        # Case: Virtual /media/ path that doesn't exist on disk anywhere
        mock_exists.return_value = False
        path = "media/test.mp4"
        resolved = resolve_media_path(path)
        # It currently returns the original decoded path if no resolution found
        self.assertEqual(resolved, "media/test.mp4")

    @patch("os.path.exists")
    def test_complex_encoded_path(self, mock_exists):
        mock_exists.side_effect = lambda p: "D:\\Videos\\test.mkv" in p
        path = "/media/D%3A%5CVideos%5Ctest.mkv"
        resolved = resolve_media_path(path)
        self.assertIn("D:", str(resolved))

if __name__ == "__main__":
    unittest.main()
