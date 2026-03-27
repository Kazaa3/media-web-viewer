# Kategorie: Performance
# Eingabewerte: Video-Dateien, Verschiedene Playback-Modi
# Ausgabewerte: Startzeit-Metriken, Backend-Latenz
# Testdateien: abc.mkv, sample.mp4
# Kommentar: Benchmark für Video-Initalisierungszeiten und Backend-Overhead

import pytest
import time
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.core import main
import db

class TestVideoPerformance:
    """Benchmark Tests für Video-Playback-Initialisierung"""
    
    def setup_method(self):
        """Setup: Dummy DB"""
        db.init_db()
        self.test_file_mkv = str(Path(__file__).parent.parent / "media" / "abc.mkv")
        # Ensure media dir exists for simulated tests
        Path(self.test_file_mkv).parent.mkdir(parents=True, exist_ok=True)
        if not Path(self.test_file_mkv).exists():
            # Create a small dummy file if it doesn't exist for path validation tests
            Path(self.test_file_mkv).write_bytes(b"\x00" * 1024)

    def test_backend_exposure_latency(self):
        """Misst die Latenz beim Aufruf von eel exposed functions für Video"""
        start = time.time()
        # Simulate local exposure call (as eel would do)
        res = main.stream_to_vlc(self.test_file_mkv)
        duration = time.time() - start
        
        print(f"\nBackend stream_to_vlc latency: {duration*1000:.2f}ms")
        assert duration < 1.0  # Sollte unter 1 Sekunde initialisieren
        assert res["status"] == "ok"

    def test_mode_switching_logic(self):
        """Verifiziert, dass die Modus-Logik korrekt zwischen den APIs unterscheidet"""
        # Test basic mode return structures
        res_vlc = main.play_vlc(self.test_file_mkv)
        assert "status" in res_vlc or "error" in res_vlc
        
        # Test stream to vlc
        res_stream = main.stream_to_vlc(self.test_file_mkv)
        assert res_stream["status"] == "ok"

    @pytest.mark.performance
    def test_parser_overhead_for_video(self):
        """Benchmark: Overhead des Parsers beim Laden von Video-Metadaten"""
        from src.parsers import pymediainfo_parser
        
        if Path(self.test_file_mkv).stat().st_size > 1024: # Only real files
            start = time.time()
            tags = pymediainfo_parser.parse(self.test_file_mkv, "mkv", {})
            duration = time.time() - start
            print(f"PyMediaInfo parse duration for {Path(self.test_file_mkv).name}: {duration*1000:.2f}ms")
            assert duration < 5.0 # Video parsing can be slow, but > 5s is too much for simple metadata

if __name__ == '__main__':
    pytest.main([__file__, '-v'])
