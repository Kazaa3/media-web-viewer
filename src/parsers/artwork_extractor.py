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
from src.core.config_master import GLOBAL_CONFIG

log = logger.get_logger("artwork")

class ArtworkExtractor:
    """
    @brief Orchestrates artwork extraction using various tools (ffmpeg, mutagen, etc.).
    """

    def __init__(self):
        art_cfg = GLOBAL_CONFIG.get("artwork_settings", {})
        cache_raw = art_cfg.get("cache_root", "~/.cache/gui_media_web_viewer/art")
        self.cache_dir = Path(os.path.expanduser(cache_raw))
        
        try:
            self.cache_dir.mkdir(parents=True, exist_ok=True)
        except FileExistsError:
            if not self.cache_dir.is_dir():
                log.error(f"[Artwork-Init] Cache path {self.cache_dir} exists but is not a directory!")
        except Exception as e:
            log.error(f"[Artwork-Init] Failed to create cache directory {self.cache_dir}: {e}")

    def extract(self, path: Path, tags: Dict[str, Any], logical_type: str) -> Optional[str]:
        """
        @brief Main entry point for extraction.
        """
        art_cfg = GLOBAL_CONFIG.get("artwork_settings", {})
        log.debug(f"🖼️ [Artwork] Extracting for {path.name} ({logical_type})")
        if not art_cfg.get("enable_extraction", True):
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
        if art_cfg.get("enable_local_search", True):
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
        ffmpeg_bin = GLOBAL_CONFIG["program_paths"].get("ffmpeg", "ffmpeg")
        art_cfg = GLOBAL_CONFIG.get("artwork_settings", {})
        ext_cfg = GLOBAL_CONFIG.get("extraction_settings", {}).get("embedded_artwork", [])
        timeout = art_cfg.get("ffmpeg_timeout_sec", 5)
        
        args = [ffmpeg_bin, "-i", str(path)] + ext_cfg + ["-y", str(out_path)]
        
        return self._run_ffmpeg(args, timeout=timeout, log_tag="extract_embedded_streams")

    def _extract_video_thumbnail(self, path: Path, out_path: Path) -> bool:
        """
        Create a thumbnail from a video frame.
        """
        ffmpeg_bin = GLOBAL_CONFIG["program_paths"].get("ffmpeg", "ffmpeg")
        art_cfg = GLOBAL_CONFIG.get("artwork_settings", {})
        ext_cfg = GLOBAL_CONFIG.get("extraction_settings", {}).get("video_thumbnail", {})
        
        offset = art_cfg.get("thumbnail_offset_sec", 7)
        res = art_cfg.get("thumbnail_resolution", "480:480")
        width, height = res.split(':')
        
        timeout = art_cfg.get("ffmpeg_timeout_sec", 8) 
        
        flags = ext_cfg.get("flags", ["-vframes", "1"])
        vf_scale = ext_cfg.get("vf_scale", "scale=w={width}:h={height}:force_original_aspect_ratio=decrease")
        formatted_vf = vf_scale.format(width=width, height=height)
        
        args = [
            ffmpeg_bin, "-i", str(path),
            "-ss", f"{offset:02d}", # Formatted offset
        ] + flags + ["-vf", formatted_vf, "-y", str(out_path)]
        
        return self._run_ffmpeg(args, timeout=timeout, log_tag="extract_video_thumbnail")

    def _find_local_art(self, path: Path, out_path: Path) -> bool:
        """
        Search for local artwork files in the same directory (or inside if path is dir).
        Also checks up to 2 levels of parent directories.
        Common names: poster, folder, cover, albumart, front.
        """
        log.debug(f"🔍 [Artwork] Searching local art for {path.name}")
        
        # Search targets: current (if dir), parent, grandparent
        search_dirs = []
        curr = path if path.is_dir() else path.parent
        if curr.exists():
            search_dirs.append(curr)
            if curr.parent != curr and curr.parent.exists() and str(curr.parent) != '/':
                search_dirs.append(curr.parent)
                if curr.parent.parent != curr.parent and curr.parent.parent.exists() and str(curr.parent.parent) != '/':
                    search_dirs.append(curr.parent.parent)

        names = {
            'poster', 'folder', 'cover', 'front', 'albumart',
            'album art', 'artwork', 'default', path.stem.lower()
        }
        exts = {'.jpg', '.jpeg', '.png', '.webp'}
        
        for target_dir in search_dirs:
            try:
                candidates = list(target_dir.iterdir())
                log.debug(f"🔍 [Artwork] Checking {len(candidates)} candidates in {target_dir}")
                
                # Priority 1: Exact matches (case-insensitive)
                for candidate in candidates:
                    if not candidate.is_file():
                        continue
                    stem_lower = candidate.stem.lower()
                    suffix_lower = candidate.suffix.lower()
                    
                    if stem_lower in names and suffix_lower in exts:
                        log.debug(f"✨ [Artwork] Match found in {target_dir.name}: {candidate.name}")
                        try:
                            shutil.copy2(candidate, out_path)
                            return True
                        except Exception: continue

                # Priority 2: Prefix matches
                for candidate in candidates:
                    if not candidate.is_file():
                        continue
                    stem_lower = candidate.stem.lower()
                    suffix_lower = candidate.suffix.lower()
                    
                    if suffix_lower in exts and any(stem_lower.startswith(n) for n in names):
                        try:
                            shutil.copy2(candidate, out_path)
                            return True
                        except Exception: continue
            except Exception as e:
                log.debug(f"Error searching art in {target_dir}: {e}")

        return False

    def _run_ffmpeg(self, cmd: list, timeout: int, log_tag: str = "generic") -> bool:
        """
        Helper to run ffmpeg commands and verify output.
        (v1.46.132 Granular Logging)
        """
        out_path = Path(cmd[-1])
        
        # Determine log redirection (Forensic Phase 7)
        log_cfg = GLOBAL_CONFIG.get("logging_registry", {})
        enable_granular = log_cfg.get("enable_granular_transcoder_logs", False)
        log_dir = Path(log_cfg.get("transcoding_log_dir", str(PROJECT_ROOT / "logs" / "transcoding")))
        
        std_out = subprocess.DEVNULL
        std_err = subprocess.PIPE
        
        if enable_granular:
            try:
                log_dir.mkdir(parents=True, exist_ok=True)
                # Timestamped safe name (Forensic Phase 7.1)
                ts = time.strftime('%Y%m%d_%H%M%S')
                log_file = log_dir / f"{ts}_{log_tag}.log"
                # Decision: Append for history as requested by user
                log_handle = open(log_file, "a", encoding="utf-8")
                std_out = log_handle
                std_err = log_handle
                log_handle.write(f"--- FFmpeg Execution Start: {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
                log_handle.write(f"Command: {' '.join(cmd)}\n\n")
            except Exception as e:
                log.debug(f"[Artwork-Log-Internal] Failed to setup granular log: {e}")
                log_handle = None
        else:
            log_handle = None

        try:
            result = subprocess.run(
                cmd, 
                stdout=std_out, 
                stderr=std_err,
                timeout=timeout,
                check=True
            )
            return out_path.exists() and out_path.stat().st_size > 0
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, Exception) as e:
            # If we captured stderr in PIPE but didn't use a log file, we might want to log it
            if not log_handle and hasattr(e, 'stderr') and e.stderr:
                log.debug(f"FFmpeg failed: {e.stderr.decode(errors='replace')}")
            
            if out_path.exists():
                try:
                    out_path.unlink()
                except Exception: pass
            return False
        finally:
            if log_handle:
                try:
                    log_handle.write(f"\n--- FFmpeg Execution End: {time.strftime('%Y-%m-%d %H:%M:%S')} ---\n")
                    log_handle.close()
                except Exception: pass

# Singleton instance
extractor = ArtworkExtractor()
