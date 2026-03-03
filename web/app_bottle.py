import bottle
import mimetypes
import subprocess
import uuid
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4

MEDIA_DIR = Path("./media")
LOG_FILE = MEDIA_DIR / "route_log.txt"

def _log(msg):
    with open(LOG_FILE, 'a') as f:
        f.write(msg + "\n")

@bottle.hook('before_request')
def log_request():
    _log(f"REQ IN: {bottle.request.url}")

@bottle.route('/media/<filepath:path>')
def serve_media(filepath):
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
    
    if needs_transcoding:
        full_path = MEDIA_DIR / filepath
        cache_dir = MEDIA_DIR / '.cache'
        cache_dir.mkdir(exist_ok=True)
        
        cache_filename = filepath.replace('/', '_').rsplit('.', 1)[0] + '.' + transcode_format
        cache_path = cache_dir / cache_filename
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
                
        return bottle.static_file(cache_filename, root=str(cache_dir), mimetype=serve_mime)

    if ext.endswith('.flac'):
        mime_type = 'audio/flac'
    
    if mime_type:
        return bottle.static_file(filepath, root=str(MEDIA_DIR), mimetype=mime_type)
    return bottle.static_file(filepath, root=str(MEDIA_DIR))

@bottle.route('/cover/<filepath:path>')
def serve_cover(filepath):
    full_path = MEDIA_DIR / filepath
    if not full_path.exists():
        return bottle.HTTPError(404, "File not found")
        
    file_type = full_path.suffix.lower()
    
    img_data = None
    mime_type = "image/jpeg"
    
    try:
        if file_type == '.mp3':
            audio = MP3(str(full_path))
            # APIC contains the picture in ID3v2
            for tag in audio.tags.values():
                if tag.FrameID == 'APIC':
                    img_data = tag.data
                    mime_type = tag.mime
                    break
        elif file_type == '.flac':
            audio = FLAC(str(full_path))
            if audio.pictures:
                img_data = audio.pictures[0].data
                mime_type = audio.pictures[0].mime
        elif file_type in {'.m4a', '.alac', '.m4b'}:
            audio = MP4(str(full_path))
            if 'covr' in audio.tags and audio.tags['covr']:
                img_data = bytes(audio.tags['covr'][0])
                if img_data.startswith(b'\x89PNG\r\n\x1a\n'):
                    mime_type = 'image/png'
                else:
                    mime_type = 'image/jpeg'
    except Exception as e:
        pass
        
    if img_data:
        bottle.response.content_type = mime_type
        return img_data
    
    return bottle.HTTPError(404, "No cover found")
