"""Safe ffprobe wrapper with pymediainfo fallback.

This module provides `run_ffprobe(path, timeout=None)` which returns a
dictionary with parsed ffprobe JSON or a fallback structure.
"""
from __future__ import annotations

import json
import shutil
import subprocess
from typing import Any


def _run_ffprobe_cli(path: str, timeout: float | None = None) -> dict[str, Any]:
    ffprobe = shutil.which('ffprobe')
    if not ffprobe:
        raise FileNotFoundError('ffprobe not found')

    args = [ffprobe, '-v', 'quiet', '-print_format', 'json', '-show_format', '-show_streams', path]
    proc = subprocess.run(args, capture_output=True, check=True, timeout=timeout)
    try:
        return json.loads(proc.stdout.decode('utf-8') or '{}')
    except Exception:
        return {"raw_stdout": proc.stdout.decode('utf-8', errors='replace')}


def _run_pymediainfo(path: str) -> dict[str, Any]:
    try:
        from pymediainfo import MediaInfo
        mi = MediaInfo.parse(path)
        data = {"tracks": [t.to_data() for t in mi.tracks]}
        return data
    except Exception as e:
        return {"error": f'pymediainfo failed: {e}'}


def run_ffprobe(path: str, timeout: float | None = None) -> dict[str, Any]:
    """Run ffprobe safely or fallback to pymediainfo.

    Returns a dict (parsed JSON) or an error/fallback dict.
    """
    try:
        return _run_ffprobe_cli(path, timeout=timeout)
    except Exception:
        # fallback
        try:
            return _run_pymediainfo(path)
        except Exception as e:
            return {"error": str(e)}
