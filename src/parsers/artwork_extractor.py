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

        if not path.exists():
            return None

        # Short-circuit for images: the image is its own artwork
        if logical_type == 'Bilder':
            return str(path)

        try:
            st = path.stat()
            # Cache key includes mtime and size to detect changes
            file_hash = hashlib.md5(f"{path}{st.st_size}{st.st_mtime}".encode()).hexdigest()
        except Exception:
            return None

        art_file = self.cache_dir / f"{file_hash}.jpg"
        if art_file.exists() and art_file.stat().st_size > 0:
            return str(art_file)

        success = False
        ext = path.suffix.lower()

        # Strategy 1: Mutagen (High quality, fast for Audio/Audiobooks)
        if logical_type == 'Audio' or ext in ('.m4b', '.m4a', '.mp3'):
            success = self._extract_audio_art(path, art_file)

        # Strategy 2: FFmpeg Attachment/Stream Extraction (Great for MKV/MP4)
        if not success:
            success = self._extract_embedded_streams(path, art_file)

        # Strategy 3: Video Thumbnailing (Last resort for Video)
        if not success and logical_type == 'Video':
            success = self._extract_video_thumbnail(path, art_file)

        return str(art_file) if success and art_file.exists() and art_file.stat().st_size > 0 else None

    def _extract_audio_art(self, path: Path, out_path: Path) -> bool:
        """
        Extract art from audio files using mutagen.
        Handles multiple APIC/covr tags.
        """
        try:
            from mutagen import File
            audio = File(str(path))
            if not audio or not audio.tags:
                return False

            best_data = None
            
            # ID3 (MP3)
            if hasattr(audio.tags, 'getall'):
                pics = audio.tags.getall('APIC')
                if pics:
                    # Preference: 3 (Cover Front), then others
                    for p in pics:
                        if getattr(p, 'type', 0) == 3:
                            best_data = p.data
                            break
                    if not best_data:
                        best_data = pics[0].data

            # FLAC
            elif hasattr(audio, 'pictures') and audio.pictures:
                # Use first picture
                best_data = audio.pictures[0].data

            # MP4 (M4B/M4A)
            elif 'covr' in audio.tags:
                covr = audio.tags['covr']
                if covr:
                    best_data = covr[0]

            if best_data:
                with open(out_path, 'wb') as f:
                    f.write(best_data)
                return True
        except Exception as e:
            log.debug(f"Mutagen failed for {path.name}: {e}")

        return False

    def _extract_embedded_streams(self, path: Path, out_path: Path) -> bool:
        """
        Try to extract video/image streams (covers/attachments).
        Works well for MKV/MP4 with multiple embedded pictures.
        """
        # 1. Broad stream mapping (picks first attached pic)
        return self._run_ffmpeg([
            "ffmpeg", "-i", str(path),
            "-map", "0:v", "-c:v", "copy", "-vframes", "1",
            "-y", str(out_path)
        ], timeout=5)

    def _extract_video_thumbnail(self, path: Path, out_path: Path) -> bool:
        """
        Create a thumbnail from a video frame.
        """
        return self._run_ffmpeg([
            "ffmpeg", "-i", str(path),
            "-ss", "00:00:07",
            "-vframes", "1",
            "-vf", "scale=w=480:h=480:force_original_aspect_ratio=decrease",
            "-y", str(out_path)
        ], timeout=8)

    def _run_ffmpeg(self, cmd: list, timeout: int) -> bool:
        try:
            subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=timeout)
            return True
        except Exception:
            return False

# Singleton instance
extractor = ArtworkExtractor()
