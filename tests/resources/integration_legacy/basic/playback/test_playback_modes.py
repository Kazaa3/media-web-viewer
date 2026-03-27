import unittest
from unittest.mock import patch, MagicMock
from src.core.main import play_media

class TestPlaybackModes(unittest.TestCase):
    def setUp(self):
        pass
        
    @patch("src.core.main.PARSER_CONFIG", {"playback_mode": "chrome_native"})
    @patch("os.path.exists")
    @patch("src.core.main.subprocess.Popen")
    @patch("shutil.which")
    @patch("src.core.main.is_mkvtoolnix_available")
    def test_play_media_native_fallback(self, mock_mkv_avail, mock_which, mock_popen, mock_exists):
        mock_exists.return_value = True
        mock_which.return_value = "/usr/bin/vlc"
        mock_mkv_avail.return_value = True
        
        # Mock process 1 (ffmpeg)
        mock_p1 = MagicMock()
        mock_p1.poll.return_value = None # Still running
        mock_p1.returncode = 0
        mock_p1.stdout = MagicMock()
        mock_p1.stderr = None
        
        # Mock process 2 (vlc)
        mock_p2 = MagicMock()
        
        mock_popen.side_effect = [mock_p1, mock_p2]
        
        res = play_media("/media/test.mkv")
        
        self.assertEqual(res["status"], "ok")
        self.assertEqual(mock_popen.call_count, 2)

    @patch("src.core.main.PARSER_CONFIG", {"playback_mode": "chrome_native"})
    def test_play_media_audio_native(self):
        res = play_media("/media/test.mp3")
        self.assertEqual(res["status"], "play")
        self.assertEqual(res["mode"], "chrome_native")

    @patch("src.core.main.PARSER_CONFIG", {"playback_mode": "direct"})
    @patch("src.core.main.vlc")
    @patch("src.core.main.HAS_VLC", True)
    def test_play_media_direct(self, mock_vlc):
        mock_inst = MagicMock()
        mock_vlc.Instance.return_value = mock_inst
        res = play_media("/media/test.mp4")
        self.assertEqual(res["status"], "ok")
        mock_inst.media_player_new.assert_called()

if __name__ == "__main__":
    unittest.main()
