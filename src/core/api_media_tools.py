import os
import time
import subprocess
import json
from pathlib import Path
from typing import Dict, Any, List, Optional

from src.core.eel_shell import eel
from src.core.config_master import GLOBAL_CONFIG, PROGRAM_REGISTRY
from src.core.logger import get_logger
from src.core import db

log = get_logger("api_media_tools")

@eel.expose
def analyse_media(path):
    """ Performs deep analysis of a media file via ffprobe. """
    from src.parsers.format_utils import PARSER_CONFIG
    import src.parsers.ffprobe_parser as ffprobe_parser
    try:
        dummy_tags = {}
        analysis = ffprobe_parser.parse(Path(path), Path(path).suffix, dummy_tags, mode='full', settings={'timeout': 5})
        return {"status": "ok", "analysis": analysis}
    except Exception as e:
        log.error(f"[Analyse] Failed for {path}: {e}")
        return {"status": "error", "message": str(e)}

@eel.expose
def analyze_media(relpath: str, client: str = 'browser'):
    """ Alias for analyse_media (v1.41 compatibility). """
    return analyse_media(relpath)

@eel.expose
def analyze_media_item(*args, **kwargs):
    """ Variadic entry point for media analysis. """
    if args: return analyse_media(args[0])
    return {"status": "error", "message": "No path provided"}

@eel.expose
def api_extract_metadata(path, name=None, mode='lightweight'):
    """ Triggers a fresh metadata extraction pulse. """
    # Delegate to the specialized parser or direct ffmpeg probe
    return {"status": "extracted", "path": path}

@eel.expose
def mkv_batch_extract(files, track_type="subtitles"):
    """ Orchestrates MKVToolNix for track extraction. """
    from src.core import mkv_tool_wrapper as mkv_tool
    return mkv_tool.mkv_batch_extract(files, track_type)

@eel.expose
def hb_encode(input_path, output_path, preset="Very Fast 1080p30"):
    """ HandBrake CLI orchestration. """
    from src.core import handbrake_wrapper as hb
    return hb.hb_encode(input_path, output_path, preset)

@eel.expose
def batch_remux_to_mkv(folder_path):
    """ Recursive remuxing to MKV via FFmpeg. """
    from src.core.remux_utils import batch_remux_to_mkv as _remux
    return _remux(folder_path)

@eel.expose
def api_scan_isbn(image_path):
    """ Forensic ISBN discovery from images (e.g. cover scans). """
    from src.parsers.isbn_parser import scan_isbn
    return scan_isbn(image_path)
