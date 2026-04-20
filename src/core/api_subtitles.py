import os
from pathlib import Path
from typing import Dict, Any, List, Optional

from src.core.eel_shell import eel
from src.core.logger import get_logger
from src.core.subtitle_processor import SubtitleProcessor

log = get_logger("api_subtitles")

@eel.expose
def extract_subtitle(filepath: str, track_index: int, output_path: Optional[str] = None):
    """ Extracts a specific subtitle track to a temp file for forensic analysis. """
    try:
        if not output_path:
            output_path = str(Path(filepath).with_suffix(f".track_{track_index}.srt"))
            
        success = SubtitleProcessor.extract_track(filepath, track_index, output_path)
        return {"status": "ok" if success else "error", "path": output_path if success else None}
    except Exception as e:
        log.error(f"[Subtitles] Extraction failed: {e}")
        return {"status": "error", "message": str(e)}

@eel.expose
def adjust_subtitle_timing(subtitle_path: str, offset_ms: int):
    """ Adjusts the timing offsets of a subtitle file. """
    try:
        success = SubtitleProcessor.adjust_timing(subtitle_path, int(offset_ms))
        return {"status": "ok" if success else "error"}
    except Exception as e:
        log.error(f"[Subtitles] Timing adjustment failed: {e}")
        return {"status": "error", "message": str(e)}

@eel.expose
def convert_subtitle_format(input_path: str, output_path: str):
    """ Converts a subtitle file to a different format (e.g., ASS to SRT). """
    try:
        success = SubtitleProcessor.convert_format(input_path, output_path)
        return {"status": "ok" if success else "error"}
    except Exception as e:
        log.error(f"[Subtitles] Conversion failed: {e}")
        return {"status": "error", "message": str(e)}

@eel.expose
def get_subtitle_info(subtitle_path: str):
    """ Returns metadata about a subtitle file. """
    try:
        return SubtitleProcessor.get_info(subtitle_path)
    except Exception as e:
        log.error(f"[Subtitles] Info probe failed: {e}")
        return {"status": "error", "message": str(e)}
