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
from parsers import filename_parser, mutagen_parser, ffmpeg_parser, pymediainfo_parser

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
# Untersützedateiformate als Liste



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
            
        # 4. pymediainfo Parser (Fallback)
        # Python wrapper around the same libmediainfo library like in MediaInfo GUI
        tags = pymediainfo_parser.parse(self.path, self.type, tags)
        
        # 5. mp3tag
        # TODO: Implement mp3tag parser for audio book chapter support
        
        return tags

    def to_dict(self):
        hours, remainder = divmod(self.duration, 3600)
        mins, secs = divmod(remainder, 60)
        
        if hours > 0:
            duration_str = f"{hours}:{mins:02d}:{secs:02d}"
        else:
            duration_str = f"{mins}:{secs:02d}"
            
        codec = self.tags.get('codec', '').upper()
        is_transcoded = self.type == '.alac' or (self.type in {'.m4a', '.m4b'} and 'ALAC' in codec)
        transcoded_format = 'FLAC' if is_transcoded else None
        
        return {
            'name': self.name,
            'path': self.path.as_posix(),
            'duration': duration_str,
            'tags': self.tags,
            'type': self.type[1:],
            'is_transcoded': is_transcoded,
            'transcoded_format': transcoded_format
        }


# Testdateien
MEDIA_DIR = "./media"  # Ordner, in dem deine Dateien liegen

# Import the separated bottle routes
from web import app_bottle


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
