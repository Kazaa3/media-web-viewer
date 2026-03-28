import sys
import os
import shutil
import time
from pathlib import Path
from typing import List, Dict, Any

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(PROJECT_ROOT / "src"))

# Diagnostic Base
try:
    from tests.engines.test_base import DiagnosticEngine, DiagnosticResult
except ImportError:
    from test_base import DiagnosticEngine, DiagnosticResult

class PlaylistSuiteEngine(DiagnosticEngine):
    def __init__(self) -> None:
        super().__init__(suite_name="Playlist")
        os.environ["UNIT_TESTING"] = "1"

    def level_1_m3u_export_integrity(self) -> DiagnosticResult:
        """Verifies that export_playlist_to_vlc produces a valid M3U file."""
        try:
            from src.core import main, db
            from pathlib import Path
            out_m3u = PROJECT_ROOT / "cache" / "test_export.m3u"
            out_m3u.parent.mkdir(exist_ok=True)
            
            original_get = db.get_media_by_name
            original_path_exists = Path.exists
            
            # Mock DB and Path.exists
            db.get_media_by_name = lambda n: {"path": f"/tmp/{n}", "duration": 120, "title": n}
            Path.exists = lambda x: True # Mock all Path objects as existing
            
            try:
                res = main.export_playlist_to_vlc(["track1.mp3", "track2.mp3"], str(out_m3u))
                
                success = res.get("status") == "ok" and out_m3u.exists()
                content = out_m3u.read_text() if out_m3u.exists() else ""
                valid_m3u = "#EXTM3U" in content and "track1.mp3" in content
                
                return DiagnosticResult(1, "M3U Export", "PASS" if success and valid_m3u else "FAIL", 
                                        f"File: {out_m3u.name}, Valid: {valid_m3u}")
            finally:
                db.get_media_by_name = original_get
                Path.exists = original_path_exists
        except Exception as e:
            return DiagnosticResult(1, "M3U Export", "FAIL", f"Logic error: {e}")

    def level_2_queue_reorder_logic(self) -> DiagnosticResult:
        """Verifies move_item_up correctly shifts items in the queue."""
        try:
            from src.core import main
            main.set_current_playlist([{"name": "A"}, {"name": "B"}], start_index=1)
            
            # Move index 1 (B) up
            main.move_item_up(1)
            
            success = main.CURRENT_PLAYLIST[0]["name"] == "B" and main.CURRENT_PLAYLIST[1]["name"] == "A"
            return DiagnosticResult(2, "Queue Reorder", "PASS" if success else "FAIL", 
                                    f"Order: {[i.get('name') for i in main.CURRENT_PLAYLIST]}")
        except Exception as e:
            return DiagnosticResult(2, "Queue Reorder", "FAIL", f"Logic error: {e}")

    def level_3_queue_maintenance(self) -> DiagnosticResult:
        """Verifies item removal and index bounds management."""
        try:
            from src.core import main
            main.set_current_playlist([{"name": "A"}, {"name": "B"}, {"name": "C"}], start_index=2)
            
            # Remove current item (C)
            main.remove_playlist_item(2)
            
            # Index should shift to 1 (B) or stay within bounds
            success = len(main.CURRENT_PLAYLIST) == 2 and main.CURRENT_INDEX < 2
            return DiagnosticResult(3, "Queue Maintenance", "PASS" if success else "FAIL", 
                                    f"Count: {len(main.CURRENT_PLAYLIST)}, Index: {main.CURRENT_INDEX}")
        except Exception as e:
            return DiagnosticResult(3, "Queue Maintenance", "FAIL", f"Logic error: {e}")

    def level_4_playlist_persistence_smoke(self) -> DiagnosticResult:
        """Verifies that the playlist can be saved/loaded from disk."""
        try:
            from src.core import main
            out_json = PROJECT_ROOT / "cache" / "test_playlist.json"
            
            main.save_playlist(["p1", "p2"], str(out_json))
            res = main.load_playlist(str(out_json))
            
            success = res.get("status") == "ok" and len(main.CURRENT_PLAYLIST) == 2
            return DiagnosticResult(4, "Persistence Smoke", "PASS" if success else "WARN", 
                                    f"Status: {res.get('status')}")
        except Exception as e:
            return DiagnosticResult(4, "Persistence Smoke", "WARN", f"Logic error: {e}")

    def level_5_playlist_api_alignment(self) -> DiagnosticResult:
        """Audits the playlist API endpoints in main.py for Eel exposure."""
        try:
            import eel
            exposed = getattr(eel, "_exposed_functions", [])
            required = ["set_current_playlist", "get_current_playlist_exposed", "move_item_up", "remove_playlist_item", "save_playlist", "load_playlist"]
            missing = [f for f in required if f not in exposed]
            
            return DiagnosticResult(5, "API Alignment", "PASS" if not missing else "WARN", 
                                    f"Missing exports: {missing}" if missing else "All playlist endpoints exposed.")
        except Exception as e:
            return DiagnosticResult(5, "API Alignment", "WARN", f"Audit failed: {e}")

    def run_all(self, stages: List[Any] = None) -> List[DiagnosticResult]:
        if not stages:
            stages = [
                self.level_1_m3u_export_integrity,
                self.level_2_queue_reorder_logic,
                self.level_3_queue_maintenance,
                self.level_4_playlist_persistence_smoke,
                self.level_5_playlist_api_alignment
            ]
        return super().run_all(stages)

if __name__ == "__main__":
    PlaylistSuiteEngine().run_all()
