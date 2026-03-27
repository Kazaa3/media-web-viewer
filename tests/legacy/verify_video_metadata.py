
import sys
import os
import json
import subprocess
import unittest
from unittest.mock import patch, MagicMock
from pathlib import Path

# Fix sys.path for absolute imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from src.core.main import get_video_metadata

class TestVideoMetadata(unittest.TestCase):
    @patch("subprocess.run")
    def test_get_video_metadata_h264_mp4(self, mock_run):
        # Mock ffprobe output
        mock_stdout = json.dumps({
            "streams": [
                {"codec_type": "video", "codec_name": "h264", "width": 1920, "height": 1080}
            ],
            "format": {"format_name": "mov,mp4,m4a,3gp,3g2,mj2", "duration": "120.5"}
        })
        mock_run.return_value = MagicMock(returncode=0, stdout=mock_stdout)
        
        meta = get_video_metadata("/fake/video.mp4")
        
        self.assertEqual(meta["codec"], "h264")
        self.assertEqual(meta["container"], "mov") # first part of mov,mp4...
        self.assertEqual(meta["width"], 1920)
        self.assertEqual(meta["height"], 1080)
        self.assertAlmostEqual(meta["duration"], 120.5)

    @patch("subprocess.run")
    def test_get_video_metadata_hevc_mkv(self, mock_run):
        mock_stdout = json.dumps({
            "streams": [
                {"codec_type": "video", "codec_name": "hevc", "width": 3840, "height": 2160}
            ],
            "format": {"format_name": "matroska,webm", "duration": "60.0"}
        })
        mock_run.return_value = MagicMock(returncode=0, stdout=mock_stdout)
        
        meta = get_video_metadata("/fake/video.mkv")
        
        self.assertEqual(meta["codec"], "hevc")
        self.assertEqual(meta["container"], "matroska")
        self.assertEqual(meta["duration"], 60.0)

    @patch("subprocess.run")
    def test_get_video_metadata_error(self, mock_run):
        mock_run.return_value = MagicMock(returncode=1, stderr="Error")
        
        meta = get_video_metadata("/fake/broken.mp4")
        
        self.assertEqual(meta, {})

if __name__ == "__main__":
    unittest.main()
