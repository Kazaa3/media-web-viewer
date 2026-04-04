import src.core.db as db
import src.core.logger as logger
import bottle
import mimetypes
import subprocess
import os
import uuid
import shutil
import sys
import json
from urllib.parse import unquote
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4

# import logger  (redundant now)
import logging

# Get specialized logger for web component
log = logger.get_logger("web")

APP_ROOT = Path(__file__).resolve().parent.parent
MEDIA_DIR = APP_ROOT / "media"
CACHE_DIR = logger.APP_DATA_DIR / "cache"


def _log(msg):
    """
    @brief Internal helper (legacy proxy) for logging.
    """
    log.info(msg)


def _resolve_path(filename):
    """
    @brief Resolves a filename to its full filesystem path.
    @details Löst einen Dateinamen in seinen vollen Pfad auf.
    @param filename Name of the media file / Name der Datei.
    @return Full path or None / Voller Pfad oder None.
    """
    db_path = db.get_media_path(filename)
    if db_path:
        p = Path(db_path)
        if p.exists():
            return p
    local = MEDIA_DIR / filename
    if local.exists():
        return local
    return None


@bottle.hook('before_request')
def log_request():
    # Keep request tracing lightweight: avoid unconditional INFO logging per request.
    logger.debug("network", f"HTTP Request: {bottle.request.method} {bottle.request.url}")


@bottle.route('/health')
def health_check():
    """
    @brief Lightweight health endpoint for HTTP latency diagnostics.
    @details Sehr leichter Endpunkt zur Messung der Bottle/HTTP-Latenz.
    @return Status dictionary / Status-Dictionary.
    """
    return {
        "status": "ok",
        "service": "media-web-viewer",
        "timestamp": int(__import__('time').time() * 1000),
    }


@bottle.route('/media/<filepath:path>')
def serve_media(filepath):
    """
    @brief Serves media files with optional on-the-fly transcoding.
    @details Liefert Mediendateien aus, optional mit Live-Transkodierung (ALAC→FLAC, WMA→OGG).
             Uses FFmpeg for transcoding with optimized parameters:
             - ALAC → FLAC: lossless, compression_level=5
             - WMA → Opus: lossy, VBR, 128k bitrate
             Transcoded files are cached in ~/.cache/MediaWebViewer/transcoded/
    @param filepath Relative path or filename / Pfad oder Dateiname.
    @return Static file or transcoding stream / Statische Datei oder Transkodierungs-Stream.
    """
    mime_type, _ = mimetypes.guess_type(filepath)
    ext = filepath.lower()

    # Detect transcoding suffix: .flac_transcoded, .ogg_transcoded, .mp3_transcoded, .aac_transcoded
    needs_transcoding = False
    transcode_format = None

    
    suffixes = {
        '.flac_transcoded': 'flac',
        '.ogg_transcoded': 'ogg',
        '.mp3_transcoded': 'mp3',
        '.aac_transcoded': 'aac',
        '.opus_transcoded': 'opus'
    }
    
    for suffix, fmt in suffixes.items():
        if filepath.endswith(suffix):
            filepath = filepath[:-len(suffix)]
            transcode_format = fmt
            needs_transcoding = True
            break

    ext = filepath.lower()
    full_path = _resolve_path(filepath)
    if not full_path:
        return bottle.HTTPError(404, "File not found")

    # [v1.34-TRANSCODE] Automatic Detection: ALAC or problematic OGG
    # OGG transcoding requested by user specifically for testing compatibility.
    is_alac = ext.endswith('.alac') or (ext.endswith('.m4a') and 'alac' in str(full_path).lower())
    is_problem_ogg = ext.endswith('.ogg') # Specifically requested to be handled/transcoded.
    
    if needs_transcoding or is_alac or is_problem_ogg:
        # If not already specified by suffix, use WAV/FLAC for ALAC or Vorbis for OGG
        if not transcode_format:
            transcode_format = 'flac' if is_alac else 'ogg'
            
        CACHE_DIR.mkdir(parents=True, exist_ok=True)
        # Use a deterministic hash for cache key based on the path
        import hashlib
        path_hash = hashlib.md5(str(full_path).encode()).hexdigest()[:10]
        cache_filename = f"trans_{path_hash}.{transcode_format}"
        cache_path = CACHE_DIR / cache_filename
        tmp_path = cache_path.with_suffix(f'.{uuid.uuid4().hex[:6]}.tmp')

        # FFmpeg configuration matrix
        matrix = {
            'mp3': (['audio/mpeg'], ['-c:a', 'libmp3lame', '-q:a', '2', '-f', 'mp3']),
            'ogg': (['audio/ogg'], ['-c:a', 'libvorbis', '-q:a', '4', '-f', 'ogg']), # Standard Vorbis for ogg
            'opus': (['audio/ogg'], ['-c:a', 'libopus', '-b:a', '128k', '-vbr', 'on', '-f', 'ogg']),
            'aac': (['audio/aac'], ['-c:a', 'aac', '-b:a', '128k', '-f', 'adts']),
            'flac': (['audio/flac'], ['-c:a', 'flac', '-compression_level', '5', '-f', 'flac'])
        }
        
        serve_mime_list, ffmpeg_args = matrix.get(str(transcode_format), (['audio/mpeg'], ['-f', 'mp3']))
        serve_mime = serve_mime_list[0]

        if not cache_path.exists():
            _log(f"TRANSCODING STARTED: {full_path} → {transcode_format}")
            start_time = __import__('time').time()
            try:
                # Optimized ffmpeg command: -vn (no video), -map 0:a (first audio stream)
                subprocess.run(
                    ['ffmpeg', '-y', '-v', 'quiet', '-i', str(full_path), '-vn', '-map', '0:a:0'] + ffmpeg_args + [str(tmp_path)],
                    check=True, timeout=30
                )
                
                if tmp_path.exists() and tmp_path.stat().st_size > 0:
                    latency = __import__('time').time() - start_time
                    tmp_path.replace(cache_path)
                    _log(f"TRANSCODING SUCCESS: {cache_path.stat().st_size} bytes in {latency:.3f}s")
                else:
                    raise RuntimeError("Output file empty")
            except Exception as e:
                _log(f"TRANSCODING FAILED: {e}")
                if tmp_path.exists(): tmp_path.unlink()
                # Fallback to static serve below if transcoding fails
            else:
                return bottle.static_file(cache_filename, root=str(CACHE_DIR), mimetype=serve_mime)

    # 3. Standard Static Serving with improved mimetype detection
    mime_type, _ = mimetypes.guess_type(str(full_path))
    if ext.endswith('.flac'):
        mime_type = 'audio/flac'
    elif ext.endswith('.mkv'):
        mime_type = 'video/x-matroska'
    elif ext.endswith('.wav'):
        mime_type = 'audio/wav' # Native wav for wav24
    
    return bottle.static_file(full_path.name, root=str(full_path.parent), mimetype=mime_type)


@bottle.route('/cover/<filepath:path>')
def serve_cover(filepath):
    """
    @brief Extracts and serves the embedded cover art from a media file.
    @details Extrahiert und liefert das eingebettete Cover-Bild einer Mediendatei.
    @param filepath Media filename or path / Medien-Dateiname oder Pfad.
    @return Image data or 404 / Bilddaten oder 404.
    """
    # Check database for cached artwork first
    item_name = unquote(filepath)
    db_item = db.get_media_by_name(item_name)
    if db_item and db_item.get('art_path'):
        art_path = Path(db_item['art_path'])
        if art_path.exists():
            mime_type, _ = mimetypes.guess_type(str(art_path))
            return bottle.static_file(art_path.name, root=str(art_path.parent), mimetype=mime_type or 'image/jpeg')

    full_path = _resolve_path(filepath)
    if not full_path or not full_path.exists():
        return bottle.HTTPError(404, "File not found")

    file_type = full_path.suffix.lower()

    img_data = None
    mime_type = "image/jpeg"

    try:
        if file_type == '.mp3':
            audio_mp3 = MP3(str(full_path))
            if audio_mp3.tags:
                # APIC contains the picture in ID3v2
                for tag in audio_mp3.tags.values():
                    if hasattr(tag, 'FrameID') and tag.FrameID == 'APIC':
                        img_data = tag.data
                        mime_type = tag.mime
                        break
        elif file_type == '.flac':
            audio_flac = FLAC(str(full_path))
            if audio_flac.pictures:
                img_data = audio_flac.pictures[0].data
                mime_type = audio_flac.pictures[0].mime
        elif file_type in {'.m4a', '.alac', '.m4b'}:
            audio_mp4 = MP4(str(full_path))
            if audio_mp4.tags and 'covr' in audio_mp4.tags and audio_mp4.tags['covr']:
                img_data = bytes(audio_mp4.tags['covr'][0])
                if img_data.startswith(b'\x89PNG\r\n\x1a\n'):
                    mime_type = 'image/png'
                else:
                    mime_type = 'image/jpeg'
    except Exception:
        pass

    if img_data:
        bottle.response.content_type = mime_type
        return img_data

    return bottle.HTTPError(404, "No cover found")


@bottle.route('/direct/<filepath:path>')
def serve_direct(filepath):
    """
    @brief Serves media files directly (Range-compatible) for Direct Play.
    """
    full_path = _resolve_path(filepath)
    if not full_path or not full_path.exists():
        return bottle.HTTPError(404, "File not found")
        
    mime_type, _ = mimetypes.guess_type(str(full_path))
    return bottle.static_file(full_path.name, root=str(full_path.parent), mimetype=mime_type)


@bottle.route('/cache/<filepath:path>')
def serve_cache(filepath):
    """
    @brief Serves files from the local media cache (Remuxed/Extracted).
    """
    cache_path = CACHE_DIR / "media" / filepath
    if not cache_path.exists():
        return bottle.HTTPError(404, "Cache file not found")
        
    mime_type, _ = mimetypes.guess_type(str(cache_path))
    return bottle.static_file(cache_path.name, root=str(cache_path.parent), mimetype=mime_type)


@bottle.error(500)
def error500(error):
    """
    @brief Custom 500 error handler with debug logging.
    """
    import traceback
    log.error("\n--- ERROR 500 ---\n%s\nURL: %s", traceback.format_exc(), bottle.request.url)
    return "Internal Server Error (Details logged to app.log)"
