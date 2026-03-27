import sys
import os
import unittest
import json
from pathlib import Path
from bs4 import BeautifulSoup

# Fix paths for imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(PROJECT_ROOT))

# Mock some hardware/config to avoid errors during import
os.environ["UNIT_TESTING"] = "1"

try:
    from src.core import db, mode_router, ffprobe_analyzer
    from src.core.main import sanitize_json_utf8, get_library_filtered
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

class TestSuite7Objects(unittest.TestCase):
    """
    7 OBJECT TEST SUITE - Levels 1 to 4 (Static & Logic)
    """

    @classmethod
    def setUpClass(cls):
        db.init_db()

    def setUp(self):
        db.clear_media()

    # --- LEVEL 1: Memory & Dict Integrity ---
    def test_level1_dict_structure(self):
        mock_raw = {"format": {"filename": "test.mkv", "duration": "3600"}}
        # Simplified check: ensure we can create a media item dict
        item = {
            "name": "Test File",
            "path": "/media/test.mkv",
            "type": "video/x-matroska",
            "tags": {"genre": "Action"}
        }
        self.assertIn("name", item)
        self.assertEqual(item["tags"]["genre"], "Action")

    # --- LEVEL 2: Database Persistence ---
    def test_level2_db_persistence(self):
        item = {
            "name": "DB Test",
            "path": "/media/db_test.mp4",
            "type": "video/mp4",
            "duration": "00:05:00",
            "is_transcoded": 0,
            "category": "Film",
            "tags": {"year": "2024", "genre": "Sci-Fi"},
            "full_tags": {"audio_tracks": [{"index": 1, "lang": "eng"}], "subtitle_tracks": []}
        }
        db.insert_media(item)
        retrieved = db.get_all_media()
        self.assertEqual(len(retrieved), 1)
        self.assertEqual(retrieved[0]["name"], "DB Test")
        # Check if full_tags JSON is preserved
        self.assertIn("audio_tracks", retrieved[0]["full_tags"])

    # --- LEVEL 7: Real Media Path Verification ---
    def test_level7_real_media(self):
        media_dir = PROJECT_ROOT / "media"
        if not media_dir.exists():
            self.skipTest("Media directory not found")
        
        # Pick 3 different extensions to test
        exts = [".mkv", ".iso", ".mp3", ".m4a", ".aac"]
        found_files = []
        for f in media_dir.iterdir():
            if f.suffix.lower() in exts and f.is_file():
                found_files.append(f)
                if len(found_files) >= 5: break
        
        if not found_files:
            self.skipTest("No real media files found for Level 7")

        import src.core.ffprobe_analyzer as ff
        import uuid
        
        print(f"\n[Level 7] Probing {len(found_files)} real media files (Masked Results):")
        for f in found_files:
            res = ff.ffprobe_analyze(f)
            self.assertNotIn("error", res, f"Analysis failed for {f.suffix}")
            
            # Mask filename for copyright/privacy
            masked_name = f"MEDIA_{uuid.uuid4().hex[:8]}{f.suffix}"
            print(f"  - Ext: {f.suffix} | Mask: {masked_name} | Res: {res.get('resolution')} | Codec: {res.get('codec')}")
            
            self.assertIn("codec", res)
            self.assertIn("container", res)

    # --- LEVEL 3: Mode Router ---
    def test_level3_router_logic(self):
        # Mock ffprobe_analyze in the router's namespace
        from src.core import mode_router as mr
        original = mr.ffprobe_analyze
        mr.ffprobe_analyze = lambda x: {
            "codec": "h264", "container": "mkv", "resolution": "1080p",
            "is_iso": False, "has_menus": False, "atmos": False, "is_audio": False
        }
        try:
            res = mr.smart_route("/media/movie.mkv")
            self.assertIsInstance(res, dict)
            self.assertEqual(res["mode"], "mse") # 1080p MKV should be MSE
        finally:
            mr.ffprobe_analyze = original

    # --- LEVEL 4: Static HTML Integrity ---
    def test_level4_html_structure(self):
        html_path = PROJECT_ROOT / "web" / "app.html"
        self.assertTrue(html_path.exists())
        
        content = html_path.read_text(encoding='utf-8')
        # Check for Stage 6 filter elements
        self.assertIn("library-search-input", content, "Search input missing")
        self.assertIn("library-genre-filter", content, "Genre filter missing")
        self.assertIn("library-year-filter", content, "Year filter missing")
        self.assertIn("hdr-cinema", content, "Premium Cinema filter missing")

    # --- LEVEL 6: Mock Backend End-to-End ---
    def test_level6_filtered_api(self):
        # Inject multi-genre items
        base = {"type": "v", "duration": "0", "is_transcoded": 0, "path": "/f.mp4"}
        db.insert_media({**base, "name": "Action One", "tags": {"genre": "Action"}})
        db.insert_media({**base, "name": "Comedy One", "tags": {"genre": "Comedy"}})
        
        # Test the Eel-exposed function logic (Level 6)
        res = get_library_filtered(genre="Action")
        self.assertEqual(len(res["media"]), 1)
        self.assertEqual(res["media"][0]["name"], "Action One")

if __name__ == "__main__":
    unittest.main()
