import db
import bottle
import mimetypes
import subprocess
import uuid
import sys
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4

# Add parent dir so we can import db
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

APP_ROOT = Path(__file__).resolve().parent.parent
MEDIA_DIR = APP_ROOT / "media"
APP_DATA_DIR = Path.home() / ".media-web-viewer"
LOG_FILE = APP_DATA_DIR / "route_log.txt"
CACHE_DIR = APP_DATA_DIR / "cache"


def _log(msg):
    """
    @brief Internal helper to log messages to the route log file.
    @details Interner Helfer zum Loggen von Nachrichten in die Routen-Logdatei.
    @param msg Message to log / Zu loggende Nachricht.
    """
    try:
        with open(LOG_FILE, "a", encoding='utf-8') as f:
            f.write(f"{msg}\n")

        # Avoid circular import by importing main inside the function
        import __main__ as main
        if hasattr(main, 'DEBUG_FLAGS') and main.DEBUG_FLAGS.get("web"):
            if hasattr(main, 'debug_log'):
                main.debug_log(f"[Web] {msg}")
            else:
                print(f"[Web] {msg}")
    except Exception:
        pass


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
    _log(f"REQ IN: {bottle.request.url}")


@bottle.route('/media/<filepath:path>')
def serve_media(filepath):
    """
    @brief Serves media files with optional on-the-fly transcoding.
    @details Liefert Mediendateien aus, optional mit Live-Transkodierung (ALAC/WMA).
    @param filepath Relative path or filename / Pfad oder Dateiname.
    @return Static file or transcoding stream / Statische Datei oder Transkodierungs-Stream.
    """
    mime_type, _ = mimetypes.guess_type(filepath)
    ext = filepath.lower()

    # Detect transcoding suffix: .flac_transcoded or .ogg_transcoded
    needs_transcoding = False
    transcode_format = None

    if filepath.endswith('.flac_transcoded'):
        filepath = filepath[:-16]
        transcode_format = 'flac'
        needs_transcoding = True
    elif filepath.endswith('.ogg_transcoded'):
        filepath = filepath[:-15]
        transcode_format = 'ogg'
        needs_transcoding = True

    ext = filepath.lower()
    _log(f"ROUTE CALLED: filepath={filepath}, ext={ext}")

    full_path = _resolve_path(filepath)
    if not full_path:
        return bottle.HTTPError(404, "File not found")

    if needs_transcoding:
        CACHE_DIR.mkdir(parents=True, exist_ok=True)

        cache_filename = filepath.replace('/', '_').rsplit('.', 1)[0] + '.' + transcode_format
        cache_path = CACHE_DIR / cache_filename
        tmp_path = cache_path.with_suffix(f'.{uuid.uuid4().hex[:6]}.tmp')

        # FFmpeg output format and MIME type
        if transcode_format == 'ogg':
            ffmpeg_args = ['-c:a', 'libopus', '-b:a', '128k', '-f', 'ogg']
            serve_mime = 'audio/ogg'
        else:
            ffmpeg_args = ['-f', 'flac']
            serve_mime = 'audio/flac'

        if not cache_path.exists():
            _log(f"TRANSCODING STARTED: {full_path} → {transcode_format}")
            try:
                subprocess.run(
                    ['ffmpeg', '-y', '-v', 'warning', '-i', str(full_path), '-vn'] + ffmpeg_args + [str(tmp_path)],
                    check=True, capture_output=True, text=True
                )
                tmp_path.replace(cache_path)
                _log("TRANSCODING SUCCESS")
            except subprocess.CalledProcessError as e:
                _log(f"TRANSCODING FAILED: {e.stderr}")
                if tmp_path.exists():
                    tmp_path.unlink()
                return bottle.HTTPError(500, "Transcoding Error")

        return bottle.static_file(cache_filename, root=str(CACHE_DIR), mimetype=serve_mime)

    if ext.endswith('.flac'):
        mime_type = 'audio/flac'

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


@bottle.error(500)
def error500(error):
    """
    @brief Custom 500 error handler with debug logging.
    @details Benutzerdefinierter HTML 500 Fehler-Handler mit Debug-Logging.
    @param error Error object / Fehler-Objekt.
    @return Error message string / Fehlermeldungs-String.
    """
    import traceback
    with open("/tmp/media_viewer_500.log", "a") as f:
        f.write("\n--- ERROR 500 ---\n")
        f.write(traceback.format_exc())
        f.write(f"URL: {bottle.request.url}\n")
    return "Internal Server Error (Details logged to /tmp/media_viewer_500.log)"
