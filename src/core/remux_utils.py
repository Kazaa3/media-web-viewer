import subprocess
import os
from pathlib import Path
import logging
import hashlib
from . import logger

log = logging.getLogger("remux_utils")
MEDIA_CACHE = Path(logger.APP_DATA_DIR) / "cache" / "media"

def remux_to_mp4_cache(full_path: str | Path) -> str:
    """
    Remuxes compatible MKV/AVI to MP4 in cache for Direct Play.
    Returns the absolute path to the cached MP4.
    """
    MEDIA_CACHE.mkdir(parents=True, exist_ok=True)
    full = Path(full_path)
    # Generate unique hash based on path and mtime
    try:
        h = hashlib.md5(f"{full}{full.stat().st_mtime}".encode()).hexdigest()
    except Exception:
        h = hashlib.md5(str(full).encode()).hexdigest()
        
    out = MEDIA_CACHE / f"{h}.mp4"
    
    if out.exists():
        return str(out)
        
    log.info(f"Remuxing to cache: {full} -> {out}")
    cmd = [
        "ffmpeg", "-y", "-i", str(full),
        "-map", "0:v:0?", "-map", "0:a:0?",
        "-c", "copy", "-movflags", "+faststart",
        str(out)
    ]
    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=300)
        return str(out)
    except Exception as e:
        log.error(f"Remux failed: {e}")
        return str(full) # Fallback to original

def extract_main_from_iso(iso_path: str | Path) -> str:
    """
    Extracts the main movie from ISO to cache using ffmpeg.
    """
    MEDIA_CACHE.mkdir(parents=True, exist_ok=True)
    full = Path(iso_path)
    h = hashlib.md5(f"iso_{full}{full.stat().st_mtime}".encode()).hexdigest()
    out = MEDIA_CACHE / f"{h}.mkv"
    
    if out.exists():
        return str(out)
        
    log.info(f"Extracting from ISO: {full} -> {out}")
    # Simple extraction via ffmpeg (works for many ISOs if they are single title)
    cmd = ["ffmpeg", "-y", "-i", str(full), "-c", "copy", str(out)]
    try:
        subprocess.run(cmd, check=True, capture_output=True, timeout=600)
        return str(out)
    except Exception as e:
        log.error(f"ISO extraction failed: {e}")
        return ""
