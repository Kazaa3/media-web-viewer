import src.core.db as db
import src.core.logger as logger
import bottle
import mimetypes
import subprocess
import os
import uuid
import shutil
import sys
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

    logger.debug("network", f"serve_media: filepath={filepath}, needs_transcoding={needs_transcoding}, format={transcode_format}")

    ext = filepath.lower()
    full_path = _resolve_path(filepath)
    if not full_path:
        return bottle.HTTPError(404, "File not found")

    if needs_transcoding:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

        cache_filename = filepath.replace('/', '_').rsplit('.', 1)[0] + '.' + transcode_format
        cache_path = CACHE_DIR / cache_filename
        tmp_path = cache_path.with_suffix(f'.{uuid.uuid4().hex[:6]}.tmp')

        # FFmpeg configuration matrix
        matrix = {
            'mp3': (['audio/mpeg'], ['-c:a', 'libmp3lame', '-q:a', '2', '-f', 'mp3']),
            'ogg': (['audio/ogg'], ['-c:a', 'libopus', '-b:a', '128k', '-vbr', 'on', '-f', 'ogg']),
            'opus': (['audio/ogg'], ['-c:a', 'libopus', '-b:a', '128k', '-vbr', 'on', '-f', 'ogg']),
            'aac': (['audio/aac'], ['-c:a', 'aac', '-b:a', '128k', '-f', 'adts']),
            'flac': (['audio/flac'], ['-c:a', 'flac', '-compression_level', '5', '-f', 'flac'])
        }
        
        serve_mime_list, ffmpeg_args = matrix.get(str(transcode_format), (['audio/mpeg'], ['-f', 'mp3']))
        serve_mime = serve_mime_list[0]

        if not cache_path.exists():
            _log(f"TRANSCODING STARTED: {full_path} → {transcode_format}")
            logger.debug("transcode", f"Transcoding required: {full_path} to {transcode_format}")
            try:
                result = subprocess.run(
                    ['ffmpeg', '-y', '-v', 'warning', '-i', str(full_path), '-vn', '-map', '0:a:0'] + ffmpeg_args + [str(tmp_path)],
                    check=True, capture_output=True, text=True, timeout=120
                )
                if tmp_path.exists() and tmp_path.stat().st_size > 0:
                    tmp_path.replace(cache_path)
                    _log(f"TRANSCODING SUCCESS: {cache_path.stat().st_size} bytes")
                    logger.debug("transcode", f"Transcoding success: {cache_path} ({cache_path.stat().st_size} bytes)")
                else:
                    raise RuntimeError("FFmpeg produced empty output")
            except subprocess.TimeoutExpired:
                _log(f"TRANSCODING TIMEOUT: {full_path}")
                logger.debug("transcode", f"Transcoding timeout for {full_path}")
                if tmp_path.exists():
                    tmp_path.unlink()
                return bottle.HTTPError(504, "Transcoding Timeout")
            except subprocess.CalledProcessError as e:
                _log(f"TRANSCODING FAILED: {e.stderr}")
                logger.debug("transcode", f"Transcoding failed for {full_path}: stderr={e.stderr}, returncode={e.returncode}")
                if tmp_path.exists():
                    tmp_path.unlink()
                return bottle.HTTPError(500, f"Transcoding Error: {e.stderr[:200]}")
            except Exception as e:
                _log(f"TRANSCODING ERROR: {e}")
                logger.debug("transcode", f"Transcoding unexpected error for {full_path}: {e}")
                if tmp_path.exists():
                    tmp_path.unlink()
                return bottle.HTTPError(500, "Transcoding Error")

        return bottle.static_file(cache_filename, root=str(CACHE_DIR), mimetype=serve_mime)

    if ext.endswith('.flac'):
        mime_type = 'audio/flac'
    elif ext.endswith('.mkv'):
        mime_type = 'video/x-matroska'
    elif ext.endswith('.mp4'):
        mime_type = 'video/mp4'
    elif ext.endswith('.webm'):
        mime_type = 'video/webm'

    if mime_type:
        return bottle.static_file(full_path.name, root=str(full_path.parent), mimetype=mime_type)
    return bottle.static_file(full_path.name, root=str(full_path.parent))


@bottle.route('/cover/<filepath:path>')
def serve_cover(filepath):
    """
    @brief Extracts and serves the embedded cover art from a media file.
    @details Extrahiert und liefert das eingebettete Cover-Bild einer Mediendatei.
    @param filepath Media filename or path / Medien-Dateiname oder Pfad.
    @return Image data or 404 / Bilddaten oder 404.
    """
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


@bottle.route('/video-stream/<filepath:path>')
def stream_video(filepath):
    """
    @brief Real-time video streaming with live transcoding.
    @details Nutzt FFmpeg für Live-Transkodierung in ein browser-kompatibles Format (Fragmented MP4).
             Optimiert für geringe Latenz und hohe Kompatibilität.
    @param filepath Pfad zur Mediendatei.
    """
    full_path = _resolve_path(filepath)
    if not full_path:
        return bottle.HTTPError(404, "File not found")

    is_iso = str(full_path).lower().endswith('.iso')
    input_source = f"dvd://{full_path}" if is_iso else str(full_path)

    # FFmpeg command for fragmented MP4 streaming
    # -frag_keyframe+empty_moov: Required for streaming MP4
    # -preset ultrafast: Faster encoding
    # -tune zerolatency: Minimize delay
    cmd = [
        'ffmpeg', '-re', '-i', input_source,
        '-vcodec', 'libx264', '-preset', 'ultrafast', '-tune', 'zerolatency',
        '-acodec', 'aac', '-ar', '44100', '-ab', '128k',
        '-f', 'mp4', '-movflags', 'frag_keyframe+empty_moov+default_base_moof',
        '-loglevel', 'error', '-'
    ]

    logger.debug("network", f"VIDEO_STREAM STARTED: {input_source}")

    def generate():
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            if not process.stdout:
                 return
            while True:
                chunk = process.stdout.read(64 * 1024)
                if not chunk:
                    break
                yield chunk
        finally:
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
            logger.debug("network", f"VIDEO_STREAM ENDED: {input_source}")

    bottle.response.content_type = 'video/mp4'
    return generate()


@bottle.route('/vlc-stream/<filepath:path>')
def stream_vlc(filepath):
    """
    @brief Real-time video streaming with VLC as the backend engine.
    @details Nutzt VLC für Live-Transkodierung und liefert den Stream an den Browser.
    """
    full_path = _resolve_path(filepath)
    if not full_path:
        return bottle.HTTPError(404, "File not found")

    vlc_path = shutil.which('vlc') or 'vlc'
    # VLC sout chain: transcode and mux to mp4 for browser
    # access=file,dst=- is the way to pipe to stdout in VLC
    sout = '#transcode{vcodec=h264,vb=2000,scale=auto,acodec=mp4a,ab=128,channels=2,samplerate=44100}:std{access=file,mux=mp4,dst=-}'
    
    cmd = [
        vlc_path, '-I', 'dummy', str(full_path),
        '--sout', sout, 'vlc://quit'
    ]

    logger.debug("network", f"VLC_STREAM STARTED: {full_path}")

    def generate():
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        try:
            if not process.stdout:
                 return
            while True:
                chunk = process.stdout.read(64 * 1024)
                if not chunk:
                    break
                yield chunk
        finally:
            process.terminate()
            try:
                process.wait(timeout=2)
            except subprocess.TimeoutExpired:
                process.kill()
            logger.debug("network", f"VLC_STREAM ENDED: {full_path}")

    bottle.response.content_type = 'video/mp4'
    return generate()


@bottle.error(500)
def error500(error):
    """
    @brief Custom 500 error handler with debug logging.
    @details Benutzerdefinierter HTML 500 Fehler-Handler mit Debug-Logging.
    @param error Error object / Fehler-Objekt.
    @return Error message string / Fehlermeldungs-String.
    """
    import traceback
    log.error("\n--- ERROR 500 ---\n%s\nURL: %s", traceback.format_exc(), bottle.request.url)
    return "Internal Server Error (Details logged to app.log)"
