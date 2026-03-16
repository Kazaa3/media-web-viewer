import unittest
import os
from unittest.mock import patch, MagicMock
from src.core.main import open_video

class TestDvdIsoPlayback(unittest.TestCase):
    def setUp(self):
        self.iso_path = "/home/xc/#Coding/gui_media_web_viewer/media/Going Raw - JUDITA_169_OPTION.ISO"

    @patch("src.core.main.subprocess.Popen")
    @patch("shutil.which")
    @patch("os.path.exists")
    def test_dvd_native_playback(self, mock_exists, mock_which, mock_popen):
        mock_exists.return_value = True
        mock_which.return_value = "/usr/bin/vlc"
        
        # Test dvd_native mode
        res = open_video(self.iso_path, "dvd_native")
        
        self.assertEqual(res["status"], "ok")
        self.assertEqual(res["mode"], "vlc_native")
        
        # Verify VLC command was called with dvd://
        args, kwargs = mock_popen.call_args
        cmd = args[0]
        self.assertIn("vlc", cmd[0])
        self.assertIn(f"dvd://{self.iso_path}", cmd[1])

    @patch("src.core.main.subprocess.Popen")
    @patch("shutil.which")
    @patch("os.path.exists")
    def test_iso_auto_detection(self, mock_exists, mock_which, mock_popen):
        mock_exists.return_value = True
        mock_which.return_value = "/usr/bin/vlc"
        
        # When using a generic 'vlc' mode but with an .ISO file
        res = open_video(self.iso_path, "vlc")
        
        self.assertEqual(res["status"], "ok")
        self.assertEqual(res["mode"], "vlc_native")
        self.assertIn(f"dvd://{self.iso_path}", mock_popen.call_args[0][0][1])

if __name__ == "__main__":
    unittest.main()
