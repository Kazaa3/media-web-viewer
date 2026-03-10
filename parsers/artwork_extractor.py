#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Media Web Viewer - Artwork Extractor

Specialized handlers for extracting covers/thumbnails from various containers.
"""

import subprocess
import hashlib
import os
from pathlib import Path
from typing import Optional, Dict, Any
from .format_utils import PARSER_CONFIG
import logger

log = logger.get_logger("artwork")

class ArtworkExtractor:
    """
    @brief Orchestrates artwork extraction using various tools (ffmpeg, mutagen, etc.).
    """

    def __init__(self):
        self.cache_dir = Path.home() / '.cache' / 'gui_media_web_viewer' / 'art'
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def extract(self, path: Path, tags: Dict[str, Any], logical_type: str) -> Optional[str]:
        """
        @brief Main entry point for extraction.
        """
        if PARSER_CONFIG.get('ffmpeg_extract_thumbnails') is False:
            return None

        # 1. Validation and Setup
        if not path.exists():
            return None

        try:
            st = path.stat()
            file_hash = hashlib.md5(f"{path}{st.st_size}{st.st_mtime}".encode()).hexdigest()
        except Exception:
            return None

        art_file = self.cache_dir / f"{file_hash}.jpg"
        if art_file.exists():
            return str(art_file)

        # 2. Strategy Selection
        success = False
        
        # Priority 1: Container-specific "Native" extraction
        if logical_type == 'Audio':
            success = self._extract_audio_art(path, art_file)
        
        # Priority 2: FFmpeg (General fallback for video and embedded image streams)
        if not success:
            if logical_type == 'Video':
                success = self._extract_video_art(path, art_file)
            elif tags.get('has_art') == 'Yes':
                success = self._extract_generic_embedded(path, art_file)

        return str(art_file) if success and art_file.exists() and art_file.stat().st_size > 0 else None

    def _extract_audio_art(self, path: Path, out_path: Path) -> bool:
        """
        Extract art from audio files.
        """
        # Try mutagen first (pure python, can be faster for tags)
        try:
            from mutagen import File
            audio = File(str(path))
            if audio and audio.tags:
                # Check for various tag formats
                # ID3 (MP3)
                if hasattr(audio.tags, 'getall'):
                    pics = audio.tags.getall('APIC')
                    if pics:
                        with open(out_path, 'wb') as f:
                            f.write(pics[0].data)
                        return True
                # FLAC
                if hasattr(audio, 'pictures') and audio.pictures:
                    with open(out_path, 'wb') as f:
                        f.write(audio.pictures[0].data)
                    return True
                # MP4 (M4A/M4B)
                if 'covr' in audio.tags:
                    with open(out_path, 'wb') as f:
                        f.write(audio.tags['covr'][0])
                    return True
        except Exception as e:
            log.debug(f"Mutagen extraction failed for {path.name}: {e}")

        # Fallback to FFmpeg for audio art extraction
        return self._run_ffmpeg([
            "ffmpeg", "-i", str(path),
            "-an", "-vcodec", "copy",
            "-y", str(out_path)
        ], timeout=5)

    def _extract_video_art(self, path: Path, out_path: Path) -> bool:
        """
        Extract art from video files (Attachments or Frames).
        """
        # Try attachments first (common in MKV)
        success = self._run_ffmpeg([
            "ffmpeg", "-i", str(path),
            "-map", "0:v", "-c:v", "copy", "-vframes", "1",
            "-y", str(out_path)
        ], timeout=3)

        if not success or not out_path.exists():
            # Real thumbnailing
            success = self._run_ffmpeg([
                "ffmpeg", "-i", str(path),
                "-ss", "00:00:05", # Seek for non-black frame
                "-vframes", "1",
                "-vf", "scale=w=400:h=400:force_original_aspect_ratio=decrease",
                "-y", str(out_path)
            ], timeout=7)
        
        return success

    def _extract_generic_embedded(self, path: Path, out_path: Path) -> bool:
        """
        Fallback embedded stream extraction.
        """
        return self._run_ffmpeg([
            "ffmpeg", "-i", str(path),
            "-map", "0:v:0", "-c:v", "copy", "-vframes", "1",
            "-y", str(out_path)
        ], timeout=5)

    def _run_ffmpeg(self, cmd: list, timeout: int) -> bool:
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=timeout)
            return True
        except Exception:
            return False

# Singleton instance
extractor = ArtworkExtractor()
