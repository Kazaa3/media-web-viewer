import sys
import os
import json
import subprocess
import time
import re
from pathlib import Path
from typing import List, Dict, Any

from src.core.config_master import PROJECT_ROOT, DB_FILENAME, TEST_DIR, DATA_DIR
sys.path.append(str(PROJECT_ROOT))
sys.path.append(str(PROJECT_ROOT / "src"))

# Diagnostic Base
try:
    from tests.engines.test_base import DiagnosticEngine, DiagnosticResult
except ImportError:
    from test_base import DiagnosticEngine, DiagnosticResult

class MediaIntegritySuiteEngine(DiagnosticEngine):
    def __init__(self) -> None:
        super().__init__(suite_name="Integrity")
        os.environ["UNIT_TESTING"] = "1"

    def level_1_live_mkv_parse(self) -> DiagnosticResult:
        """Generates a real MKV and parses bitrate via FFmpeg (Legacy: test_mkv.py)."""
        temp_file = Path("/tmp/diag_test.mkv")
        try:
            # Create 1s silent MKV
            subprocess.run(
                ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "1", "-c:a", "libmp3lame", "-b:a", "128k", str(temp_file)],
                stderr=subprocess.PIPE, check=True, timeout=10
            )
            
            from src.core import ffprobe_analyzer as ff
            res = ff.ffprobe_analyze(temp_file)
            
            bitrate = res.get("bitrate", 0)
            success = bitrate > 0
            return DiagnosticResult(1, "Live MKV Parse", "PASS" if success else "FAIL", f"Extracted bitrate: {bitrate} bps")
        except Exception as e:
            return DiagnosticResult(1, "Live MKV Parse", "FAIL", f"Error: {e}")
        finally:
            if temp_file.exists(): temp_file.unlink()

    def level_2_mutagen_id3_sync(self) -> DiagnosticResult:
        """Verifies Mutagen tag extraction consistency (Legacy: test_mp3_tags.py)."""
        try:
            from mutagen.mp3 import MP3
            from mutagen.id3 import ID3, TPE1, TIT2
        except ImportError:
             return DiagnosticResult(2, "Mutagen ID3 Sync", "SKIP", "Mutagen not installed.")

        temp_file = Path("/tmp/diag_test.mp3")
        try:
            # Create a dummy MP3
            subprocess.run(
                ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo", "-t", "0.5", str(temp_file)],
                stderr=subprocess.PIPE, check=True
            )
            
            # Inject tags
            audio = MP3(str(temp_file), ID3=ID3)
            audio.add_tags()
            audio.tags.add(TPE1(encoding=3, text='Diag Artist'))
            audio.tags.add(TIT2(encoding=3, text='Diag Title'))
            audio.save()
            
            # Verify via our app logic (if a parser exists for mutagen)
            # For now, we manually check
            verify = MP3(str(temp_file))
            success = verify.get('TPE1') and verify['TPE1'].text[0] == 'Diag Artist'
            return DiagnosticResult(2, "Mutagen ID3 Sync", "PASS" if success else "FAIL", "Injected/Extracted 'Diag Artist' successfully.")
        except Exception as e:
            return DiagnosticResult(2, "Mutagen ID3 Sync", "FAIL", f"Error: {e}")
        finally:
            if temp_file.exists(): temp_file.unlink()

    def level_3_artwork_extraction(self) -> DiagnosticResult:
        """Verifies artwork extraction from media file headers."""
        temp_file = Path("/tmp/diag_art.mp3")
        temp_img = Path("/tmp/diag_cover.jpg")
        
        try:
            # 1. Create a dummy image
            subprocess.run(["ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=blue:s=100x100", "-frames:v", "1", str(temp_img)], check=True)
            
            # 2. Create MP3 with embedded artwork
            subprocess.run([
                "ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc", "-i", str(temp_img),
                "-map", "0:a", "-map", "1:v", "-c:a", "libmp3lame", "-c:v", "copy",
                "-id3v2_version", "3", "-metadata:s:v", 'title="Album cover"', "-t", "0.5", str(temp_file)
            ], check=True, stderr=subprocess.PIPE)
            
            # 3. Use app logic to extract
            from src.parsers.artwork_extractor import extractor as art
            from src.core.models import MediaItem
            
            # MediaItem(name, path)
            item = MediaItem(temp_file.name, temp_file)
            # extractor.extract(path, tags, logical_type)
            data_path = art.extract(temp_file, item.tags, item.logical_type)
            
            success = data_path is not None and Path(data_path).exists()
            return DiagnosticResult(3, "Artwork Extraction", "PASS" if success else "FAIL", f"Extracted artwork to: {data_path}")
        except Exception as e:
            return DiagnosticResult(3, "Artwork Extraction", "FAIL", f"Error: {e}")
        finally:
            if temp_file.exists(): temp_file.unlink()
            if temp_img.exists(): temp_img.unlink()

    def level_4_registry_audit(self) -> DiagnosticResult:
        """Verifies completeness of the media extension registry."""
        try:
            from src.parsers.format_utils import (
                AUDIO_EXTENSIONS, VIDEO_EXTENSIONS, DISK_IMAGE_EXTENSIONS,
                EBOOK_EXTENSIONS, DOCUMENT_EXTENSIONS, IMAGE_EXTENSIONS
            )
            stats = [
                len(AUDIO_EXTENSIONS), len(VIDEO_EXTENSIONS), len(DISK_IMAGE_EXTENSIONS),
                len(EBOOK_EXTENSIONS), len(DOCUMENT_EXTENSIONS), len(IMAGE_EXTENSIONS)
            ]
            total = sum(stats)
            if total < 50:
                 return DiagnosticResult(4, "Registry Audit", "FAIL", f"Registry too small: {total} extensions.")
            return DiagnosticResult(4, "Registry Audit", "PASS", f"Verified {total} extensions across 6 categories.")
        except Exception as e:
            return DiagnosticResult(4, "Registry Audit", "FAIL", str(e))

    def level_5_categorization_logic(self) -> DiagnosticResult:
        """Verifies category detection logic (Legacy: test_file_formats_suite.py)."""
        try:
            from src.parsers.format_utils import detect_file_format
            tests = [
                ("movie.mkv", "MKV"),
                ("song.flac", "FLAC"),
                ("doc.pdf", "PDF"),
                ("disc.iso", "ISO"),
                ("book.epub", "EPUB")
            ]
            failures = []
            for filename, expected in tests:
                res = detect_file_format(filename)
                if res != expected:
                    failures.append(f"{filename}->{res}")
            
            if failures:
                return DiagnosticResult(5, "Categorization Logic", "FAIL", f"Mismatches: {failures}")
            return DiagnosticResult(5, "Categorization Logic", "PASS", "Extension-to-category mapping verified.")
        except Exception as e:
            return DiagnosticResult(5, "Categorization Logic", "FAIL", str(e))

if __name__ == "__main__":
    MediaIntegritySuiteEngine().run()
