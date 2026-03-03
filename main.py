# Todo
## Funktionen
# File-Handling
# - Medien scannen (Ordner durchsuchen, Metadaten extrahieren)
# - Weitere Funktionen hinzufügen, z.B. zum Abspielen von Medien, Verwalten von Wiedergabelisten, etc.
##### GUI
# - Hauptfenster mit Navigation (Medienbibliothek, Wiedergabelisten, Einstellungen)
# - Medienbibliothek (Datei-Explorer, Drag & Drop)
##### Datenbank
# Wechsel zu:  pywebview oder Flask
# SQLite über sqlite3 oder SQLAlchemy
############ Datenmodel
# Datenstruktur für Medien
# class MediaItem(name, path, type, duration, tags, ...)


#Benötigte Module importieren
import eel # Electron-like Python Library for building desktop apps with web technologies
import os
from pathlib import Path
import subprocess
import re  # For MKV parsing

# Eigene Parser
from parsers import filename_parser, mutagen_parser, ffmpeg_parser, mediaview_parser

# Audio-Tag-Bibliothek
from mutagen.mp3 import MP3  # Für MP3-Dauer
from mutagen.flac import FLAC  # Für FLAC-Dauer
from mutagen.oggvorbis import OggVorbis  # Für OGG
from mutagen.mp4 import MP4  # Für ALAC/M4A/M4B
from mutagen.oggopus import OggOpus
from mutagen.wave import WAVE
from mutagen.aac import AAC
from mutagen.asf import ASF # Für WMA
from mutagen.id3 import ID3 # statt ffmpeg

#Video-Tag-Bibliothek
#mkvinfo
#mediainfo
#mp3tag




# weitere Container
# mp4, avi, mov, mkv, webm, flv, wmv, mpg, mpeg, m4v, 3gp, 3g2, ogv, ogg, mts, m2ts

#Dokumente
# pdf, doc, docx, txt, md, html, htm
# epub, mobi, azw, fb2

# sonstige
# zip, rar, 7z, tar, gz, bz2, xz
# exe, dmg, deb, rpm, apk
# iso, img, vhd, vmdk, vdi
# bat, sh, ps1, cmd
# py, js, html, css, php, java, c, cpp, h, hpp, cs, rb, go, rs, swift, kt,kts,kts


class MediaItem:
    def __init__(self, name, path):
        self.name = name
        self.path = Path(path)
        self.type = self.path.suffix.lower()
        self.duration = self._get_duration()
        self.tags = self._get_tags()


    def show_info(self):
        print(self.name)
        print(self.path)
        print(self.type)
        print(self.duration)
        print(self.tags)
        print("\n")

    def _get_duration(self):
        """Extrahiert Dauer in Sekunden (mit mutagen)."""
        try:
            if self.type == '.mp3':
                audio = MP3(self.path)
                return int(audio.info.length)
            elif self.type == '.flac':
                audio = FLAC(self.path)
                return int(audio.info.length)
            elif self.type == '.ogg':
                audio = OggVorbis(self.path)
                return int(audio.info.length)
            elif self.type in {'.m4a', '.alac', '.m4b'}:
                audio = MP4(self.path)
                return int(audio.info.length)
            elif self.type == '.opus':
                audio = OggOpus(self.path)
                return int(audio.info.length) 
            elif self.type == '.wav':
                audio = WAVE(self.path)
                return int(audio.info.length)  
        except:
            pass
            
        # FFmpeg fallback if mutagen fails
        try:
            import subprocess, re
            cmd = ["ffmpeg", "-i", self.path.as_posix()]
            output = subprocess.run(cmd, stderr=subprocess.PIPE, text=True).stderr
            dur_match = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", output)
            if dur_match:
                hours = int(dur_match.group(1))
                minutes = int(dur_match.group(2))
                seconds = float(dur_match.group(3))
                return int(hours * 3600 + minutes * 60 + seconds)
        except:
            pass
            
        return 0

    def _get_tags(self):
        """Extrahiert umfassende Metadaten sequenziell mit verschiedenen Parsern."""
        # 1. Filename Parser (Grundlage)
        tags = filename_parser.parse(self.path, self.name)
        
        # 2. Mutagen Parser (Hauptquelle)
        tags = mutagen_parser.parse(self.path, self.type, tags, self.name)
        
        # 3. FFmpeg Parser (Fallback für Bitrate/Samplerate/Container)
        if not tags['samplerate'] or not tags['bitrate'] or tags['tagtype'] == 'None' or not tags['bitdepth']:
            tags = ffmpeg_parser.parse(self.path, self.type, tags)
            
        # 4. Mediaview Parser (Platzhalter)
        tags = mediaview_parser.parse(self.path, self.type, tags)
        
        return tags

    def to_dict(self):
        hours, remainder = divmod(self.duration, 3600)
        mins, secs = divmod(remainder, 60)
        
        if hours > 0:
            duration_str = f"{hours}:{mins:02d}:{secs:02d}"
        else:
            duration_str = f"{mins}:{secs:02d}"
            
        return {
            'name': self.name,
            'path': self.path.as_posix(),
            'duration': duration_str,
            'tags': self.tags,
            'type': self.type[1:]  # 'mp3'
        }


# Testdateien
MEDIA_DIR = "./media"  # Ordner, in dem deine Dateien liegen

import bottle
import mimetypes
import subprocess
import os
import uuid

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


# Funktion, um Medien zu scannen und an die GUI zu senden
@eel.expose("scan_media")
def scan_media():
    if not os.path.exists(MEDIA_DIR):
        os.makedirs(MEDIA_DIR)
        return {"error": "Ordner erstellt – füge Dateien hinzu"}
    media = []
    for f in Path(MEDIA_DIR).iterdir():
        if f.is_file() and f.suffix.lower() in {'.mp3', '.flac', '.ogg', '.wav', '.m4a', '.alac', '.opus', '.aac', '.wma', '.m4b'}:
            item = MediaItem(f.name, f)
            media.append(item.to_dict()) # Datenmodel
    return {"media": media}  # Reich an GUI mit Tags + Dauer

@eel.expose("play_media")
def play_media(path):
    """GUI ruft das an – aber HTML5 Audio handhabt Abspielen client-seitig."""
    return {"status": "play", "path": path}  # Bestätigung

# Main-Funktion, die die Eel-App startet
if __name__ == "__main__":
    eel.init("web")            # Ordner mit HTML/CSS/JS
    eel.start("app.html", size=(1000, 600))    # Starte Seite
