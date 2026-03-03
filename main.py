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

# Parser zusammen führen




#Benötigte Module importieren
import eel # Electron-like Python Library for building desktop apps with web technologies
import os
from pathlib import Path
import subprocess
import re  # For MKV parsing

# Konfiguration
MEDIA_DIR = "./media"  # Ordner mit Testdateien
AUDIO_EXTENSIONS = {
    '.mp3', '.flac', '.ogg', '.wav', '.m4a', '.alac', '.opus', '.aac', '.wma', '.m4b'
}
VIDEO_EXTENSIONS = {
    '.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv', '.mpg', '.mpeg', '.m4v', '.3gp', '.3g2', '.ogv', '.ogg', '.mts', '.m2ts'
}
DOCUMENT_EXTENSIONS = {
    '.pdf', '.doc', '.docx', '.txt', '.md', '.html', '.htm'
}
IMAGE_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg', '.ico'
}
EBOOK_EXTENSIONS = {
    '.epub', '.mobi', '.azw', '.fb2'
}
ARCHIVE_EXTENSIONS = {
    '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'
}   

### Typen erstellen


# Audio  --> Werte --> Bitrate --> Samplerate --> Bitdepth --> Tag-Format --> Container
# WMAV2  --> ASFTags --> ASF
# WAV24 --> PCM_S24LE | 32 Bit (s32) | 44.1 kHz
# WAV16 --> PCM_S16LE | 16 Bit (s16) | 44.1 kHz




# Eigene Module

# Benutzerdefinierte Module
import db

# Eigene Parser
from parsers import filename_parser, mutagen_parser, ffmpeg_parser, pymediainfo_parser

# Eigene bottle Web-Routen
from web import app_bottle

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
from mutagen.dsdiff import DSDIFF # DSD Interchange File Format: .dsf-Dateien
from mutagen.dsf import DSF # DSD Stream File: .dsd-Dateien

#Video-Tag-Bibliothek
#mkvinfo
#mediainfo
#mp3tag
# Untersützedateiformate als Liste

# ID3v2.4 / ID3v2.3 / ID3v2.2 / ID3v1.1 / ID3v1
# APEv2 / APEv1
# MP4 Atoms
# FLACVComment
# OggVComment

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


                    # ==========================================
                    # CONTAINER-FORMAT AUSWERTUNG (FFmpeg)
                    # ==========================================
                    # FFmpeg gibt in der Line "Input #0" das exakte Demuxer-Format an.
                    # Viele Formate teilen sich historisch denselben Container-Standard:
                    # 
                    # 1. ISOBMFF (Apple QuickTime Derivate):
                    #    Formate wie .mp4, .m4a (Audio) und .m4b (Audiobooks) basieren alle 
                    #    auf dem "Base Media" Format (ISO/IEC 14496-12). FFmpeg fasst diese 
                    #    beim Einlesen generisch unter dem Begriff "mov,mp4,m4a,3gp,3g2,mj2" zusammen.
                    #    Wenn wir "MOV" auslesen, aber die Datei eigentlich ".m4b" heißt, 
                    #    korrigieren wir die Anzeige für den User exakt auf die Dateiendung (z.B. M4B).
                    #
                    # 2. Matroska / WebM:
                    #    Ein extrem flexibler Open-Source Container, der fast alle Streams schluckt.
                    #    FFmpeg meldet hier "matroska,webm". Wir bereinigen das visuell zu "MKV".
                    # ==========================================

            # ==========================================
            # AUDIO-TAG AUSWERTUNG (Mutagen)
            # ==========================================
            # Je nach Dateityp verwendet die Mutagen-Bibliothek völlig unterschiedliche Parser.
            # Um dem Nutzer saubere, branchenübliche Tag-Typen anzuzeigen, schlüsseln wir diese auf:
            #
            # 1. ID3 (MP3):
            #    ID3-Tags haben historisch viele Iterationen (v1, v2.2, v2.3, v2.4). Da die Version hier
            #    elementar für die Kompatibilität von Car-Audios und Playern ist, lesen wir explizit
            #    den `tags.version` Tuple (z.B. (2,3,0)) aus und wandeln ihn formal in "ID3v2.3" um.
            # 
            # 2. ISOBMFF / Apple (MP4/M4A/M4B):
            #    Nutzt intern sogenannte "MP4 Atoms" (ilst). Ein versionierungsgeladenes Chaos 
            #    wie bei ID3 gibt es hier nicht. Wir benennen Mutagens rohes "MP4Tags" in das
            #    cleane "MP4" um.
            #
            # 3. Xiph (Ogg/FLAC):
            #    Nutzen den "Vorbis Comment" Standard (eine simple LISTE von Schlüssel=Wert paaren).
            #    Auch hier gibt es keine nennenswerte Unterversionierung. Um sie voneinander 
            #    zu trennen, benennen wir "OggVComment" und "FLACVComment" in menschliche Strings um.
            # ==========================================





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
            cmd = ["ffmpeg", "-i", str(self.path)]
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
        # Lossless ALAC → transcode to FLAC
        is_alac = self.type == '.alac' or (self.type in {'.m4a', '.m4b'} and 'ALAC' in codec)
        # Lossy WMA → transcode to OGG (Opus)
        is_wma = self.type == '.wma'
        
        is_transcoded = is_alac or is_wma
        if is_alac:
            transcoded_format = 'FLAC'
        elif is_wma:
            transcoded_format = 'OGG'
        else:
            transcoded_format = None
        
        return {
            'name': self.name,
            'path': str(self.path),
            'duration': duration_str,
            'tags': self.tags,
            'type': self.type[1:],
            'is_transcoded': is_transcoded,
            'transcoded_format': transcoded_format
        }



@eel.expose("get_library")
def get_library():
    """Gibt alle Medien aus der Datenbank zurück ohne neu zu scannen."""
    return {"media": db.get_all_media()}

# Funktion, um Medien zu scannen und an die GUI zu senden
@eel.expose("scan_media")
def scan_media():
    if not Path(MEDIA_DIR).exists():
        os.makedirs(MEDIA_DIR)
        return {"error": "Ordner erstellt – füge Dateien hinzu"}
    
    # DB leeren und komplett neu einlesen (Refresh)
    db.clear_media()
    
    for f in Path(MEDIA_DIR).iterdir():
        if f.is_file() and f.suffix.lower() in AUDIO_EXTENSIONS:
            item = MediaItem(f.name, f)
            db.insert_media(item.to_dict())
            
    # Liefere gescannten Stand direkt aus der DB zurück
    return {"media": db.get_all_media()}  # Reich an GUI mit Tags + Dauer

@eel.expose("play_media")
def play_media(path):
    """GUI ruft das an – aber HTML5 Audio handhabt Abspielen client-seitig."""
    return {"status": "play", "path": path}  # Bestätigung

@eel.expose("browse_dir")
def browse_dir(dir_path=None):
    """Listet Ordner und Audiodateien eines Verzeichnisses für den Datei-Browser."""
    if not dir_path:
        dir_path = str(Path.home())
    
    target = Path(dir_path)
    if not target.exists() or not target.is_dir():
        return {"error": "Ordner nicht gefunden", "path": dir_path}
    
    items = []
    try:
        for entry in sorted(target.iterdir(), key=lambda e: (not e.is_dir(), e.name.lower())):
            if entry.name.startswith('.'):
                continue
            if entry.is_dir():
                items.append({"name": entry.name, "path": str(entry), "type": "folder"})
            elif entry.suffix.lower() in AUDIO_EXTENSIONS:
                size_mb = entry.stat().st_size / (1024 * 1024)
                items.append({"name": entry.name, "path": str(entry), "type": "file", "size": f"{size_mb:.1f} MB"})
    except PermissionError:
        return {"error": "Keine Berechtigung", "path": dir_path}
    
    parent = str(target.parent) if target.parent != target else None
    return {"path": str(target), "parent": parent, "items": items}

@eel.expose("add_file_to_library")
def add_file_to_library(file_path):
    """Fügt eine einzelne Datei aus dem Datei-Browser der Bibliothek hinzu."""
    p = Path(file_path)
    if not p.exists() or not p.is_file():
        return {"error": "Datei nicht gefunden"}
    if p.suffix.lower() not in AUDIO_EXTENSIONS:
        return {"error": "Kein unterstütztes Audioformat"}
    
    known = db.get_known_media_names()
    if p.name in known:
        return {"status": "exists", "name": p.name}
    
    item = MediaItem(p.name, p)
    db.insert_media(item.to_dict())
    return {"status": "added", "name": p.name}

# Main-Funktion, die die Eel-App startet
if __name__ == "__main__":
    db.init_db()               # SQLite-Datenbank initialisieren (Placeholder)
    eel.init("web")            # Ordner mit HTML/CSS/JS
    eel.start("app.html", size=(1000, 600))    # Starte Seite
