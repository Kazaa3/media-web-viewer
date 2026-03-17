import unittest
import os
import shutil
import tempfile
import logging
from pathlib import Path
from unittest.mock import MagicMock, patch

# Configure logging for tests
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger("test_suite")

# Import the components to test
from src.core import main
from src.core import db
from src.core.models import MediaItem
from src.parsers.format_utils import (
    PARSER_CONFIG, 
    AUDIO_EXTENSIONS, 
    VIDEO_EXTENSIONS, 
    DISK_IMAGE_EXTENSIONS
)

class TestFileFormatsMock(unittest.TestCase):
    """
    Mock Layer: Tests logic and registry isolation using mocks.
    """
    def setUp(self):
        # Patch eel to avoid GUI issues
        self.eel_patcher = patch('eel.expose', lambda x: x)
        self.eel_patcher.start()
        
        # Mock database
        self.db_patcher = patch('src.core.db.insert_media')
        self.mock_insert = self.db_patcher.start()
        
        self.db_clear_patcher = patch('src.core.db.clear_media')
        self.mock_clear = self.db_clear_patcher.start()
        
        self.db_get_patcher = patch('src.core.db.get_all_media', return_value=[])
        self.mock_get_all = self.db_get_patcher.start()

    def tearDown(self):
        patch.stopall()

    def test_scanner_registry_completeness(self):
        """Verify that all target extensions are in the global registry."""
        required_audio = {'.mp3', '.flac', '.wav', '.m4a', '.ogg'}
        required_video = {'.mp4', '.mkv', '.avi', '.mov'}
        required_disk = {'.iso'}
        
        for ext in required_audio:
            self.assertIn(ext, AUDIO_EXTENSIONS, f"Missing audio extension: {ext}")
        for ext in required_video:
            self.assertIn(ext, VIDEO_EXTENSIONS, f"Missing video extension: {ext}")
        for ext in required_disk:
            self.assertIn(ext, DISK_IMAGE_EXTENSIONS, f"Missing disk extension: {ext}")

    @patch('src.core.main.PARSER_CONFIG')
    def test_scan_media_logic_mock(self, mock_config):
        """Test scan_media logic with mocked filesystem calls."""
        mock_config.get.side_effect = lambda k, default=None: {
            "indexed_categories": ["audio", "video", "abbild"],
            "scan_dirs": ["/tmp/mock_media"],
            "parser_mode": "lightweight"
        }.get(k, default)
        
        # Mock Path.rglob to simulate finding files
        with patch.object(Path, 'rglob') as mock_rglob:
            mock_file = MagicMock(spec=Path)
            mock_file.is_file.return_value = True
            mock_file.is_dir.return_value = False
            mock_file.suffix = '.mp3'
            mock_file.name = 'test_audio.mp3'
            mock_file.resolve.return_value = mock_file
            
            mock_rglob.return_value = [mock_file]
            
            # Mock Path.exists
            with patch.object(Path, 'exists', return_value=True):
                 # Mock MediaItem to avoid actual parsing
                 with patch('src.core.main.MediaItem') as mock_item_cls:
                     mock_item = MagicMock()
                     mock_item.to_dict.return_value = {'name': 'test_audio.mp3', 'category': 'audio', 'path': '/tmp/mock_media/test_audio.mp3'}
                     mock_item_cls.return_value = mock_item
                     
                     main.scan_media(dir_path="/tmp/mock_media", clear_db=True)
                     
                     self.mock_clear.assert_called_once()
                     self.mock_insert.assert_called()

class TestFileFormatsReal(unittest.TestCase):
    """
    Real Layer: Tests actual filesystem interaction using temporary files.
    """
    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.media_dir = os.path.join(self.test_dir, "media")
        os.makedirs(self.media_dir)
        
        # Patch DB to use a temporary SQLite in memory or just mock it to avoid file pollution
        # For "Real" layer, we want to test the full chain if possible, but safely.
        self.db_patcher = patch('src.core.db.insert_media')
        self.mock_insert = self.db_patcher.start()
        
        # Ensure categories are enabled in PARSER_CONFIG for test
        self.orig_indexed = PARSER_CONFIG.get("indexed_categories")
        PARSER_CONFIG["indexed_categories"] = ["audio", "video", "abbild", "ebooks", "documents"]

    def tearDown(self):
        shutil.rmtree(self.test_dir)
        patch.stopall()
        if self.orig_indexed:
            PARSER_CONFIG["indexed_categories"] = self.orig_indexed

    def _create_dummy_file(self, name, content=b"fake data"):
        path = os.path.join(self.media_dir, name)
        with open(path, "wb") as f:
            f.write(content)
        return path

    def test_audio_formats_detection(self):
        formats = ["test.mp3", "test.flac", "test.wav", "test.m4a", "test.ogg"]
        for fmt in formats:
            self._create_dummy_file(fmt)
            
        main.scan_media(dir_path=self.media_dir, clear_db=True)
        
        # Verify that insert_media was called for each file
        # Note: In real execution, some parsers might fail on dummy data, 
        # but the scanner should still identify them by extension.
        self.assertEqual(self.mock_insert.call_count, len(formats))

    def test_video_formats_detection(self):
        # MKV needs EBML magic for some parsers, even if we just check extension first
        mkv_magic = b"\x1a\x45\xdf\xa3"
        self._create_dummy_file("test.mkv", content=mkv_magic + b"video data")
        self._create_dummy_file("test.mp4")
        self._create_dummy_file("test.avi")
        
        main.scan_media(dir_path=self.media_dir, clear_db=True)
        self.assertEqual(self.mock_insert.call_count, 3)

    def test_specialized_categories_detection(self):
        """Verify specialized categories like Klassik, Serie, Film, Hörbuch."""
        # 1. Klassik (Classical)
        self._create_dummy_file("Beethoven - Symphony No. 9.mp3")
        # 2. Serie (Series)
        serie_dir = os.path.join(self.media_dir, "TV_Shows", "Season 1")
        os.makedirs(serie_dir, exist_ok=True)
        with open(os.path.join(serie_dir, "episode1.mkv"), "wb") as f:
            f.write(b"\x1a\x45\xdf\xa3" + b"video data")
        # 3. Film (Movie) - already tested in ISO but let's do a folder too
        movie_dir = os.path.join(self.media_dir, "MyMovie")
        os.makedirs(os.path.join(movie_dir, "VIDEO_TS"), exist_ok=True)
        with open(os.path.join(movie_dir, "VIDEO_TS", "VIDEO_TS.IFO"), "w") as f: f.write("IFO")
        # 4. Hörbuch (Audiobook)
        self._create_dummy_file("MyAudiobook.m4b")
        # 5. Klaqssik (User requested typo/string)
        self._create_dummy_file("Music_Klaqssik_Test.mp3")

        main.scan_media(dir_path=self.media_dir, clear_db=True)
        
        # Verify categories
        calls = [call[0][0] for call in self.mock_insert.call_args_list]
        cat_map = {c['name']: c['category'] for c in calls}
        
        self.assertEqual(cat_map.get("Beethoven - Symphony No. 9.mp3"), "Klassik")
        self.assertEqual(cat_map.get("episode1.mkv"), "Serie")
        self.assertEqual(cat_map.get("MyMovie"), "Film")
        self.assertEqual(cat_map.get("MyAudiobook.m4b"), "Hörbuch")
        self.assertEqual(cat_map.get("Music_Klaqssik_Test.mp3"), "Klassik")

if __name__ == "__main__":
    unittest.main()
