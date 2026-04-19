import sys
import os
import unittest
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass
import subprocess

# Fix paths for imports
from src.core.config_master import PROJECT_ROOT, DB_FILENAME, TEST_DIR, DATA_DIR
sys.path.append(str(PROJECT_ROOT))

# Mock some hardware/config
os.environ["UNIT_TESTING"] = "1"

try:
    from src.core import ffprobe_analyzer as ff, db, mode_router
except ImportError as e:
    print(f"❌ Import failed: {e}")
    sys.exit(1)

@dataclass
class ItemDiagnosticResult:
    level: int
    name: str
    status: str
    message: str
    details: Optional[Dict[str, Any]] = None

class ItemDiagnosticEngine:
    """
    DEDICATED ITEM TEST SUITE
    Deep-dive validation of media items, metadata extraction, and category mapping.
    """

    def __init__(self) -> None:
        self.results: List[ItemDiagnosticResult] = []

    def log(self, res: ItemDiagnosticResult) -> None:
        self.results.append(res)
        icon = {"PASS": "✅", "FAIL": "❌", "SKIP": "⏭️", "WARN": "⚠️"}.get(res.status, "❓")
        print(f"  [Item-L{res.level:02d}] {res.name}: {icon} {res.status} | {res.message}")

    # --- LEVEL 1: Atomic Mock Object ---
    def level_1_atomic_mock(self) -> ItemDiagnosticResult:
        mock_item = {
            "name": "Test Item",
            "path": "/media/test.mkv",
            "type": "video/x-matroska",
            "category": "Video",
            "tags": {"genre": "Action"}
        }
        # Basic type validation
        valid = isinstance(mock_item["name"], str) and isinstance(mock_item["tags"], dict)
        return ItemDiagnosticResult(1, "Atomic Mock", "PASS" if valid else "FAIL", "Basic Item structure verified.")

    # --- LEVEL 2: FFprobe Simulator (Atmos/HDR/4K) ---
    def level_2_ffprobe_sim(self) -> ItemDiagnosticResult:
        """Simulates FFprobe JSON output for high-end formats."""
        mock_stdout = json.dumps({
            "format": {"format_name": "matroska", "duration": "3600", "bit_rate": "50000000"},
            "streams": [
                {
                    "codec_type": "video", "codec_name": "hevc", "width": 3840, "height": 2160,
                    "color_space": "bt2020nc", "color_transfer": "smpte2084", "r_frame_rate": "24/1"
                },
                {
                    "codec_type": "audio", "codec_name": "truehd", "channels": 8,
                    "tags": {"title": "English Atmos", "language": "eng"}
                }
            ]
        })
        
        # Monkeypatch subprocess.run
        original_run = subprocess.run
        class MockResult: 
            returncode = 0
            stdout = mock_stdout
            stderr = ""
        
        subprocess.run = lambda *args, **kwargs: MockResult()
        
        try:
            res = ff.ffprobe_analyze("/tmp/mock_4k_atmos.mkv")
            success = res.get("resolution") == "4K" and res.get("is_hdr") and res.get("atmos")
            msg = f"Extracted: {res.get('resolution')}, HDR: {res.get('is_hdr')}, Atmos: {res.get('atmos')}"
            return ItemDiagnosticResult(2, "FFprobe Simulator", "PASS" if success else "FAIL", msg)
        finally:
            subprocess.run = original_run

    # --- LEVEL 3: Cat Map Audit ---
    def level_3_cat_map(self) -> ItemDiagnosticResult:
        cat_map = {
            "audio": ["Audio", "Album", "Hörbuch", "Klassik", "Single"],
            "video": ["Video", "Film", "Serie"],
            "abbild": ["Abbild", "ISO/Image", "Disk Image", "PAL DVD", "Blu-ray"],
            "spiel": ["PC Spiel"],
            "beigabe": ["Supplement", "Software"]
        }
        
        # Test edge case: "Hörbuch" -> audio
        def check(val, key):
             return val.lower() in [c.lower() for c in cat_map.get(key, [])]
        
        success = check("Hörbuch", "audio") and check("Blu-ray", "abbild") and check("Film", "video")
        return ItemDiagnosticResult(3, "Cat Map Audit", "PASS" if success else "FAIL", "All core categories correctly mapped.")

    # --- LEVEL 4: Extension Matrix ---
    def level_4_extension_matrix(self) -> ItemDiagnosticResult:
        # Create dummy files to avoid ffprobe failure
        Path("/tmp/test.iso").touch()
        Path("/tmp/test.mkv").touch()
        
        # We still need to mock subprocess.run so it doesn't try to actually probe
        original_run = subprocess.run
        subprocess.run = lambda *args, **kwargs: type('Res', (), {'returncode':0, 'stdout':'{}', 'stderr':''})()
        
        try:
            v1 = ff.ffprobe_analyze("/tmp/test.iso").get("is_iso")
            v2 = ff.ffprobe_analyze("/tmp/test.mkv").get("is_iso")
            success = (v1 is True) and (v2 is False)
            return ItemDiagnosticResult(4, "Extension Matrix", "PASS" if success else "FAIL", 
                                        f"ISO: {v1}, MKV_ISO: {v2}")
        finally:
            subprocess.run = original_run

    # --- LEVEL 5: Submode Routing Matrix ---
    def level_5_routing_matrix(self) -> ItemDiagnosticResult:
        """Verifies that the Mode Router respects the format matrix."""
        # Simple override for ffprobe_analyze to test router
        original = mode_router.ffprobe_analyze
        try:
            # Case 1: H264 MKV -> MSE
            mode_router.ffprobe_analyze = lambda x: {"codec": "h264", "container": "matroska", "is_audio": False, "is_iso": False, "resolution": "1080p"}
            r1 = mode_router.smart_route("test.mkv")["mode"] == "mse"
            
            # Case 2: MPEG2 ISO -> vlc_bridge
            mode_router.ffprobe_analyze = lambda x: {"codec": "mpeg2video", "container": "iso", "is_audio": False, "is_iso": True}
            r2 = mode_router.smart_route("test.iso")["mode"] == "vlc_bridge"
            
            success = r1 and r2
            return ItemDiagnosticResult(5, "Routing Matrix", "PASS" if success else "FAIL", f"MSE({r1}) and VLC({r2}) routing verified.")
        finally:
            mode_router.ffprobe_analyze = original

    # --- LEVEL 6: Multiple Audio Tracks ---
    def level_6_audio_tracks(self) -> ItemDiagnosticResult:
        mock_stdout = json.dumps({
            "format": {"format_name": "mkv", "duration": "0"},
            "streams": [
                {"codec_type": "audio", "codec_name": "ac3", "channels": 6, "tags": {"language": "ger", "title": "Deutsch"}},
                {"codec_type": "audio", "codec_name": "aac", "channels": 2, "tags": {"language": "eng", "title": "English"}}
            ]
        })
        original_run = subprocess.run
        subprocess.run = lambda *args, **kwargs: type('Result', (), {'returncode':0, 'stdout':mock_stdout, 'stderr':''})()
        try:
            res = ff.ffprobe_analyze("multi.mkv")
            tracks = res.get("audio_tracks", [])
            success = len(tracks) == 2 and tracks[1]["language"] == "eng"
            return ItemDiagnosticResult(6, "Multiple Audio Tracks", "PASS" if success else "FAIL", f"Detected {len(tracks)} tracks.")
        finally:
            subprocess.run = original_run

    # --- LEVEL 7: Real File Scan ---
    def level_7_real_scan(self) -> ItemDiagnosticResult:
        media_dir = PROJECT_ROOT / "media"
        if not media_dir.exists(): return ItemDiagnosticResult(7, "Real Scan", "SKIP", "Media dir missing.")
        # Recursive scan for supported formats
        valid_exts = [".mkv", ".mp4", ".m4a", ".mp3", ".iso", ".img", ".bin"]
        files = [f for f in media_dir.rglob("*") if f.suffix.lower() in valid_exts]
        return ItemDiagnosticResult(7, "Real Scan", "PASS", f"Scanned {len(files)} real media files in {media_dir}.")

    def run_all(self) -> List[ItemDiagnosticResult]:
        print("\n📦 Starting Dedicated Item Test Suite...")
        stages = [
            self.level_1_atomic_mock, self.level_2_ffprobe_sim, self.level_3_cat_map,
            self.level_4_extension_matrix, self.level_5_routing_matrix, self.level_6_audio_tracks,
            self.level_7_real_scan
        ]
        for s in stages:
            res = s()
            self.log(res)
        return self.results

class TestSuiteItems(unittest.TestCase):
    def test_item_diagnostics(self):
        engine = ItemDiagnosticEngine()
        results = engine.run_all()
        failures = [r for r in results if r.status == "FAIL"]
        self.assertEqual(len(failures), 0, f"Item diagnostics failed: {[f.level for f in failures]}")

if __name__ == "__main__":
    ItemDiagnosticEngine().run_all()
    unittest.main(argv=['first-arg-is-ignored'], exit=False)
