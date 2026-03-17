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
        mock_which.side_effect = lambda x: f"/usr/bin/{x}"
        
        # Test dvd_native mode
        res = open_video(self.iso_path, "vlc", "vlc_iso")
        
        self.assertEqual(res["status"], "ok")
        self.assertEqual(res["mode"], "vlc_external")
        
        # Verify cvlc command was called with direct path for ISO
        args, kwargs = mock_popen.call_args
        cmd = args[0]
        self.assertTrue(any("cvlc" in c for c in cmd))
        self.assertEqual(cmd[1], self.iso_path)

    @patch("src.core.main.subprocess.Popen")
    @patch("shutil.which")
    @patch("os.path.exists")
    def test_iso_auto_detection(self, mock_exists, mock_which, mock_popen):
        mock_exists.return_value = True
        mock_which.side_effect = lambda x: f"/usr/bin/{x}"
        
        # When using a generic 'vlc' mode but with an .ISO file via direct play fallback
        res = open_video(self.iso_path, "vlc", "vlc_iso")
        
        self.assertEqual(res["status"], "ok")
        self.assertEqual(res["mode"], "vlc_external")
        self.assertEqual(mock_popen.call_args[0][0][1], self.iso_path)

if __name__ == "__main__":
    unittest.main()
