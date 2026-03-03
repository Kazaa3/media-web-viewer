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
    
    # Strip the disguise extension added by Javascript
    needs_transcoding = False
    if filepath.endswith('.flac_transcoded'):
        filepath = filepath[:-16]
        ext = filepath.lower()
        needs_transcoding = True

    _log(f"ROUTE CALLED: filepath={filepath}, ext={ext}")
    
    if needs_transcoding:
        full_path = MEDIA_DIR / filepath
        cache_dir = MEDIA_DIR / '.cache'
        cache_dir.mkdir(exist_ok=True)
        
        # Cachename replaces extension with .flac to avoid collisions
        cache_filename = filepath.replace('/', '_').rsplit('.', 1)[0] + '.flac'
        cache_path = cache_dir / cache_filename
        tmp_path = cache_path.with_suffix(f'.{uuid.uuid4().hex[:6]}.tmp')
        
        # Check if we already transcoded this file
        if not cache_path.exists():
            _log(f"TRANSCODING STARTED: full_path={full_path}")
            try:
                # Run ffmpeg to generate the FLAC file to a temporary path first
                subprocess.run(
                    ['ffmpeg', '-y', '-v', 'warning', '-i', str(full_path), '-vn', '-f', 'flac', str(tmp_path)],
                    check=True, capture_output=True, text=True
                )
                # Atomic rename ensures other concurrent requests don't read a half-written file
                tmp_path.replace(cache_path)
                _log("TRANSCODING SUCCESS")
            except subprocess.CalledProcessError as e:
                _log(f"TRANSCODING FAILED: {e.stderr}")
                if tmp_path.exists():
                    tmp_path.unlink()
                return bottle.HTTPError(500, "Transcoding Error")
                
        # Serve the cached FLAC file instead of the ALAC one
        return bottle.static_file(cache_filename, root=str(cache_dir), mimetype='audio/flac')

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
