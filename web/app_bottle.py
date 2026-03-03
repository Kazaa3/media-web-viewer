import bottle
import mimetypes
import subprocess
import os
import uuid
from pathlib import Path
from mutagen.mp3 import MP3
from mutagen.flac import FLAC
from mutagen.mp4 import MP4

MEDIA_DIR = "./media"

@bottle.hook('before_request')
def log_request():
    with open(os.path.join(MEDIA_DIR, 'route_log.txt'), 'a') as f:
        f.write(f"REQ IN: {bottle.request.url}\n")

@bottle.route('/media/<filepath:path>')
def serve_media(filepath):
    mime_type, _ = mimetypes.guess_type(filepath)
    ext = filepath.lower()
    
    # Strip the disguise extension added by Javascript
    if filepath.endswith('.flac_transcoded'):
        filepath = filepath[:-16]
        ext = filepath.lower()

    with open(os.path.join(MEDIA_DIR, 'route_log.txt'), 'a') as f:
        f.write(f"ROUTE CALLED: filepath={filepath}, ext={ext}\n")
    
    if ext.endswith('.alac') or ext.endswith('.m4a') or ext.endswith('.m4b'):
        full_path = os.path.join(MEDIA_DIR, filepath)
        cache_dir = os.path.join(MEDIA_DIR, '.cache')
        os.makedirs(cache_dir, exist_ok=True)
        
        # Cachename replaces extension with .flac to avoid collisions
        cache_filename = filepath.replace('/', '_').rsplit('.', 1)[0] + '.flac'
        cache_path = os.path.join(cache_dir, cache_filename)
        tmp_path = cache_path + f'.{uuid.uuid4().hex[:6]}.tmp'
        
        # Check if we already transcoded this file
        if not os.path.exists(cache_path):
            with open(os.path.join(MEDIA_DIR, 'route_log.txt'), 'a') as f:
                f.write(f"TRANSCODING STARTED: full_path={full_path}\n")
            try:
                # Run ffmpeg to generate the FLAC file to a temporary path first
                subprocess.run(
                    ['ffmpeg', '-y', '-v', 'warning', '-i', full_path, '-vn', '-f', 'flac', tmp_path],
                    check=True, capture_output=True, text=True
                )
                # Atomic rename ensures other concurrent requests don't read a half-written file
                os.replace(tmp_path, cache_path)
                with open(os.path.join(MEDIA_DIR, 'route_log.txt'), 'a') as f:
                    f.write("TRANSCODING SUCCESS\n")
            except subprocess.CalledProcessError as e:
                with open(os.path.join(MEDIA_DIR, 'route_log.txt'), 'a') as f:
                    f.write(f"TRANSCODING FAILED: {e.stderr}\n")
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
                return bottle.HTTPError(500, "Transcoding Error")
                
        # Serve the cached FLAC file instead of the ALAC one
        return bottle.static_file(cache_filename, root=cache_dir, mimetype='audio/flac')

    if ext.endswith('.flac'):
        mime_type = 'audio/flac'
    
    if mime_type:
        return bottle.static_file(filepath, root=MEDIA_DIR, mimetype=mime_type)
    return bottle.static_file(filepath, root=MEDIA_DIR)

@bottle.route('/cover/<filepath:path>')
def serve_cover(filepath):
    # Determine the absolute filepath
    full_path = os.path.join(MEDIA_DIR, filepath)
    if not os.path.exists(full_path):
        return bottle.HTTPError(404, "File not found")
        
    path_obj = Path(full_path)
    file_type = path_obj.suffix.lower()
    
    img_data = None
    mime_type = "image/jpeg"
    
    try:
        if file_type == '.mp3':
            audio = MP3(full_path)
            # APIC contains the picture in ID3v2
            for tag in audio.tags.values():
                if tag.FrameID == 'APIC':
                    img_data = tag.data
                    mime_type = tag.mime
                    break
        elif file_type == '.flac':
            audio = FLAC(full_path)
            if audio.pictures:
                img_data = audio.pictures[0].data
                mime_type = audio.pictures[0].mime
        elif file_type in {'.m4a', '.alac', '.m4b'}:
            audio = MP4(full_path)
            if 'covr' in audio.tags and audio.tags['covr']:
                # MP4 covers are usually arrays of binary data
                img_data = bytes(audio.tags['covr'][0])
                # M4A covr images are typically JPEG or PNG. Check magic bytes
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
