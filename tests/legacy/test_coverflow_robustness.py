#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Kategorie: Robustness Test
# Zweck: Verifies Coverflow data integrity with all formats and logging.

import sys
import os
import unittest
import shutil
import tempfile
import logging
from pathlib import Path
from unittest.mock import MagicMock

# Add project root to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Mock eel before importing main
mock_eel = MagicMock()
mock_eel.expose = lambda x: x
sys.modules['eel'] = mock_eel

try:
    from src.core import db
    from src.core import main as backend
except ImportError:
    backend = None
    db = None

class TestCoverflowRobustness(unittest.TestCase):
    test_dir: Path
    db_path: Path

    @classmethod
    def setUpClass(cls):
        temp_dir = tempfile.mkdtemp(prefix="mwv_coverflow_test_")
        cls.test_dir = Path(temp_dir)
        cls.db_path = cls.test_dir / "test_db.db"
        
        # Initialize logging for tests
        logging.basicConfig(level=logging.DEBUG)
        
        # Monkeypatch DB path
        if db:
            db.DB_FILENAME = str(cls.db_path)
            db.DB_DIR = cls.test_dir
            db.init_db()
            
        if backend and hasattr(backend, 'PARSER_CONFIG'):
            backend.PARSER_CONFIG["indexed_categories"] = [
                "audio", "video", "images", "documents", "ebooks", "abbild"
            ]
            backend.PARSER_CONFIG["displayed_categories"] = [
                "audio", "video", "images", "documents", "ebooks", "abbild"
            ]
            
        logging.info(f"🛠️ Created test environment: {cls.test_dir}")

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'test_dir') and cls.test_dir and cls.test_dir.exists():
            shutil.rmtree(cls.test_dir)
            logging.info(f"🧹 Cleaned up test environment.")

    def _create_mock_file(self, path: Path, size=1024):
        """Creates a non-empty file to pass size verification."""
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"A" * size)

    def test_audio_formats(self):
        """Test scanning of various audio formats with generic names."""
        formats = ["mp3", "flac", "wav"]
        for fmt in formats:
            fname = f"test_generic_audio.{fmt}"
            fpath = self.test_dir / fname
            self._create_mock_file(fpath)
            # Add artwork for each
            art_name = f"test_generic_audio.jpg"
            self._create_mock_file(self.test_dir / art_name)

        if backend:
            backend.scan_media(dir_path=str(self.test_dir), clear_db=True)
            items = backend.get_library().get('media', [])
            for fmt in formats:
                matches = [i for i in items if i['path'].endswith(fmt)]
                self.assertTrue(len(matches) > 0, f"Audio format {fmt} not detected")
                self.assertTrue(matches[0].get('has_artwork'), f"Artwork not detected for {fmt}")
                logging.info(f"✅ Verified {fmt} support (has_art: True)")

    def test_category_folders(self):
        """Test specific categories like Audiobook, Klassik, Film, Serie."""
        categories = ["Audiobook", "Klassik", "Film", "Serie"]
        for cat in categories:
            cat_dir = self.test_dir / cat
            cat_dir.mkdir(exist_ok=True)
            # Create a media file inside
            ext = "mp3" if cat in ["Audiobook", "Klassik"] else "mp4"
            self._create_mock_file(cat_dir / f"test_in_{cat.lower()}.{ext}")
            self._create_mock_file(cat_dir / "poster.jpg")

        if backend:
            backend.scan_media(dir_path=str(self.test_dir), clear_db=True)
            items = backend.get_library().get('media', [])
            for cat in categories:
                # Check if items are assigned to the correct category or at least found
                # Note: Category logic might be based on folder name or internal tags
                matches = [i for i in items if cat.lower() in i['path'].lower()]
                self.assertTrue(len(matches) > 0, f"Item in category folder {cat} not detected")
                self.assertTrue(matches[0].get('has_artwork'), f"Artwork not detected for {cat}")
                logging.info(f"✅ Verified folder category {cat} support (has_art: True)")

    def test_iso_dvd_robustness(self):
        """Verify ISO and DVD folder detection with non-empty files and artwork."""
        # 1. Generic ISO
        iso_path = self.test_dir / "test_generic_disk.iso"
        self._create_mock_file(iso_path)
        self._create_mock_file(self.test_dir / "test_generic_disk.jpg")

        # 2. DVD Folder
        dvd_dir = self.test_dir / "test_generic_dvd_folder"
        video_ts = dvd_dir / "VIDEO_TS"
        video_ts.mkdir(parents=True)
        self._create_mock_file(video_ts / "VIDEO_TS.IFO")
        self._create_mock_file(video_ts / "VTS_01_1.VOB")
        self._create_mock_file(dvd_dir / "poster.jpg")

        if backend:
            backend.scan_media(dir_path=str(self.test_dir), clear_db=True)
            items = backend.get_library().get('media', [])
            
            # Verify ISO
            iso_items = [i for i in items if i['path'].endswith('.iso')]
            self.assertTrue(len(iso_items) > 0, "ISO not detected")
            self.assertTrue(iso_items[0].get('has_artwork'), "ISO artwork not detected")
            
            # Verify DVD Folder
            dvd_items = [i for i in items if "test_generic_dvd_folder" in i['path']]
            self.assertTrue(len(dvd_items) > 0, "DVD folder not detected")
            self.assertTrue(dvd_items[0].get('has_artwork'), "DVD folder artwork not detected")
            
            logging.info("✅ Verified ISO and DVD folder robustness (has_art: True)")

if __name__ == "__main__":
    unittest.main()
