import os
import subprocess
from pathlib import Path
from typing import Optional, List, Dict, Any

from src.core.logger import get_logger
log = get_logger("subtitle_processor")

try:
    import pysubs2
except ImportError:
    pysubs2 = None

try:
    import pysrt
except ImportError:
    pysrt = None

class SubtitleProcessor:
    """
    Handles extraction, timing adjustment, and format conversion for subtitles.
    Supports SRT, ASS, VTT, and embedded tracks via ffmpeg/pysubs2/pysrt.
    """
    
    @staticmethod
    def extract_track(media_path: str, track_index: int, output_path: str) -> bool:
        """
        Extracts a subtitle track from a media container using ffmpeg.
        """
        try:
            # Command: ffmpeg -i input -map 0:s:{track_index} -c:s copy output
            # Note: track_index from ffprobe is usually absolute (e.g. 2 if it's the 3rd stream)
            # We use absolute index directly with -map 0:{track_index}
            cmd = [
                "ffmpeg", "-y",
                "-i", media_path,
                "-map", f"0:{track_index}",
                "-c:s", "srt", # Default to SRT for widest compatibility
                output_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                log.info(f"[Subtitle] Extracted track {track_index} to {output_path}")
                return True
            else:
                log.error(f"[Subtitle] Extraction failed: {result.stderr}")
                return False
        except Exception as e:
            log.error(f"[Subtitle] Error extracting track {track_index}: {e}")
            return False

    @staticmethod
    def adjust_timing(file_path: str, offset_ms: int) -> bool:
        """
        Adjusts subtitle timing (shift) using pysubs2 or pysrt.
        """
        if not os.path.exists(file_path):
            return False
            
        try:
            if pysubs2:
                subs = pysubs2.load(file_path)
                subs.shift(ms=offset_ms)
                subs.save(file_path)
                log.info(f"[Subtitle] Shifted {file_path} by {offset_ms}ms (pysubs2)")
                return True
            elif pysrt:
                subs = pysrt.open(file_path)
                subs.shift(milliseconds=offset_ms)
                subs.save(file_path)
                log.info(f"[Subtitle] Shifted {file_path} by {offset_ms}ms (pysrt)")
                return True
            else:
                log.warning("[Subtitle] No timing library (pysubs2/pysrt) found for adjustment.")
                return False
        except Exception as e:
            log.error(f"[Subtitle] Error adjusting timing for {file_path}: {e}")
            return False

    @staticmethod
    def convert_format(input_path: str, output_path: str) -> bool:
        """
        Converts between subtitle formats using pysubs2.
        """
        if not pysubs2:
            log.warning("[Subtitle] pysubs2 missing. Conversion skipped.")
            return False
            
        try:
            subs = pysubs2.load(input_path)
            subs.save(output_path)
            log.info(f"[Subtitle] Converted {input_path} to {output_path}")
            return True
        except Exception as e:
            log.error(f"[Subtitle] Conversion failed: {e}")
            return False

    @staticmethod
    def get_info(file_path: str) -> Dict[str, Any]:
        """
        Returns basic info about a subtitle file (event count, format).
        """
        if not os.path.exists(file_path):
            return {"error": "File not found"}
            
        try:
            if pysubs2:
                subs = pysubs2.load(file_path)
                return {
                    "format": subs.format,
                    "event_count": len(subs),
                    "duration_ms": subs[-1].end if subs else 0
                }
            return {"status": "present", "engine": "fallback"}
        except Exception as e:
            return {"error": str(e)}
