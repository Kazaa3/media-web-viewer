"""Safe ffprobe wrapper with pymediainfo fallback.

This module provides `run_ffprobe(path, timeout=None)` which returns a
dictionary with parsed ffprobe JSON or a fallback structure.
"""
from __future__ import annotations
import json
import shutil
import subprocess
from typing import Any
from src.core.logger import get_logger

# Specialized logger (v1.46.132 Modernized)
log = get_logger("ffprobe_wrapper")

def _run_ffprobe_cli(path: str, timeout: float | None = None, settings: dict[str, Any] | None = None) -> dict[str, Any]:
    ffprobe = shutil.which('ffprobe')
    if not ffprobe:
        log.error("[FFprobe-Wrapper] ffprobe binary not found in PATH.")
        raise FileNotFoundError('ffprobe not found')

    args = [ffprobe, '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams']
    
    # Implementation of forced encoding (Phase 11)
    if settings and settings.get('forced_encoding'):
        args.extend(['-metadata_encoding:g', settings['forced_encoding']])
        
    args.append(path)
    
    proc = subprocess.run(args, capture_output=True, check=True, timeout=timeout)
    try:
        return json.loads(proc.stdout.decode('utf-8') or '{}')
    except Exception as e:
        log.warning(f"[FFprobe-Wrapper] JSON decode failed for {path}: {e}")
        return {"raw_stdout": proc.stdout.decode('utf-8', errors='replace')}

def _run_pymediainfo(path: str) -> dict[str, Any]:
    try:
        from pymediainfo import MediaInfo
        mi = MediaInfo.parse(path)
        data = {"tracks": [t.to_data() for t in mi.tracks]}
        return data
    except Exception as e:
        log.debug(f"[FFprobe-Wrapper] Fallback pymediainfo failed: {e}")
        return {"error": f'pymediainfo failed: {e}'}

def run_ffprobe(path: str, timeout: float | None = None, settings: dict[str, Any] | None = None) -> dict[str, Any]:
    """Run ffprobe safely or fallback to pymediainfo.

    Returns a dict (parsed JSON) or an error/fallback dict.
    """
    try:
        return _run_ffprobe_cli(path, timeout=timeout, settings=settings)
    except Exception as e:
        log.debug(f"[FFprobe-Wrapper] CLI failed, attempting fallback for {path}: {e}")
        try:
            return _run_pymediainfo(path)
        except Exception as fe:
            log.error(f"[FFprobe-Wrapper] Both CLI and fallback failed for {path}: {fe}", exc_info=True)
            return {"error": str(fe)}

