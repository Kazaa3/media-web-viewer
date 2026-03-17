#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Media Web Viewer - Artwork Extractor

Specialized handlers for extracting covers/thumbnails from various containers.
"""

import subprocess
import hashlib
import os
import shutil
from pathlib import Path
from typing import Optional, Dict, Any
from .format_utils import PARSER_CONFIG
from src.core import logger

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
        log.debug(f"🖼️ [Artwork] Extracting for {path.name} ({logical_type})")
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

        # Strategy 1: Local Files (Fastest, highest quality for DVD/ISO/Albums)
        success = self._find_local_art(path, art_file)

        # Strategy 2: Mutagen (Fast for Audio/Audiobooks)
        if not success:
            if logical_type == 'Audio' or ext in ('.m4b', '.m4a', '.mp3'):
                success = self._extract_audio_art(path, art_file)

        # Strategy 3: FFmpeg Attachment/Stream Extraction (Great for MKV/MP4)
        if not success:
            success = self._extract_embedded_streams(path, art_file)

        # Strategy 4: Video Thumbnailing (Last resort for Video)
        if not success and logical_type == 'Video':
            success = self._extract_video_thumbnail(path, art_file)

        log.debug(f"🖼️ [Artwork] Final success for {path.name}: {success}")
        if success:
            exists = art_file.exists()
            size = art_file.stat().st_size if exists else 0
            log.debug(f"🖼️ [Artwork] Cache file {art_file.name} exists: {exists}, size: {size}")
            if not exists or size == 0:
                success = False

        return str(art_file) if success else None

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

    def _find_local_art(self, path: Path, out_path: Path) -> bool:
        """
        Search for local artwork files in the same directory (or inside if path is dir).
        Common names: poster, folder, cover, albumart, front.
        """
        log.debug(f"🔍 [Artwork] Searching local art for {path.name}")
        target_dir = path if path.is_dir() else path.parent
        if not target_dir.exists():
            return False

        names = {
            'poster', 'folder', 'cover', 'front', 'albumart',
            'album art', 'artwork', 'default', path.stem.lower()
        }
        exts = {'.jpg', '.jpeg', '.png', '.webp'}
        
        try:
            # List directory once to avoid O(N*M*K) complexity
            candidates = list(target_dir.iterdir())
            log.debug(f"🔍 [Artwork] Found {len(candidates)} candidates in {target_dir}")
            
            # Priority 1: Exact matches (case-insensitive)
            for candidate in candidates:
                if not candidate.is_file():
                    continue
                stem_lower = candidate.stem.lower()
                suffix_lower = candidate.suffix.lower()
                
                log.debug(f"🔍 [Artwork] Checking candidate: {candidate.name} (stem: {candidate.stem}, ext: {candidate.suffix})")
                
                if stem_lower in names and suffix_lower in exts:
                    log.debug(f"✨ [Artwork] Match found: {candidate.name}")
                    try:
                        shutil.copy2(candidate, out_path)
                        log.debug(f"✅ [Artwork] Successfully copied to {out_path}")
                        return True
                    except Exception as e:
                        log.debug(f"❌ [Artwork] Failed to copy {candidate.name}: {e}")
                        continue

            # Priority 2: Matches starting with one of the names
            for candidate in candidates:
                if not candidate.is_file():
                    continue
                stem_lower = candidate.stem.lower()
                suffix_lower = candidate.suffix.lower()
                
                if suffix_lower in exts and any(stem_lower.startswith(n) for n in names):
                    try:
                        shutil.copy2(candidate, out_path)
                        return True
                    except Exception as e:
                        log.debug(f"Failed to copy prefix local art {candidate}: {e}")
                        continue
        except Exception as e:
            log.debug(f"Error searching local art in {target_dir}: {e}")

        return False

    def _run_ffmpeg(self, cmd: list, timeout: int) -> bool:
        """
        Helper to run ffmpeg commands and verify output.
        """
        # The output file is usually the last argument
        out_path = Path(cmd[-1])
        try:
            # We must use check=True to raise error on non-zero exit
            result = subprocess.run(
                cmd, 
                stdout=subprocess.DEVNULL, 
                stderr=subprocess.PIPE, # Capture stderr for debugging if needed
                timeout=timeout,
                check=True
            )
            # Verify the file was actually created and is not empty
            return out_path.exists() and out_path.stat().st_size > 0
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, Exception) as e:
            # log.debug(f"FFmpeg failed: {e}")
            if out_path.exists():
                try:
                    out_path.unlink() # Clean up failed/empty output
                except Exception:
                    pass
            return False

# Singleton instance
extractor = ArtworkExtractor()
