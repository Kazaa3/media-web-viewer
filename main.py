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
from mutagen.mp3 import MP3  # Für MP3-Dauer
from mutagen.flac import FLAC  # Für FLAC-Dauer
from mutagen.oggvorbis import OggVorbis  # Für OGG
from mutagen.mp4 import MP4  # Für ALAC/M4A


class MediaItem:
    def __init__(self, name, path):
        self.name = name
        self.path = Path(path)
        self.type = self.path.suffix.lower()
        self.duration = self._get_duration()
        self.tags = self._get_tags()

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
            elif self.type == '.m4a':
                audio = MP4(self.path)
                return int(audio.info.length)
        except:
            pass
        return 0

    def _get_tags(self):
        """Extrahiert Artist, Title (mutagen)."""
        try:
            if self.type == '.flac':
                audio = FLAC(self.path)
                artist = audio.get('ARTIST')
                title = audio.get('TITLE')
                return {
                    'artist': artist[0] if artist else 'Unbekannt',
                    'title': title[0] if title else self.name
                }
            elif self.type == '.mp3':
                audio = MP3(self.path)
                artist = audio.get('TPE1')
                title = audio.get('TIT2')
                return {
                    'artist': artist[0] if artist else 'Unbekannt',
                    'title': title[0] if title else self.name
                }
            elif self.type == '.m4a':
                audio = MP4(self.path)
                artist = audio.get('\xa9ART')  # Apple standard tag
                title = audio.get('\xa9nam')
                return {
                    'artist': artist[0] if artist else 'Unbekannt',
                    'title': title[0] if title else self.name
                }
            elif self.type == '.ogg':
                audio = OggVorbis(self.path)
                artist = audio.get('artist')
                title = audio.get('title')
                return {
                    'artist': artist[0] if artist else 'Unbekannt',
                    'title': title[0] if title else self.name
                }
        except:
            pass
        return {'artist': 'Unbekannt', 'title': self.name}

    def to_dict(self):
        mins, secs = divmod(self.duration, 60)
        return {
            'name': self.name,
            'path': self.path.as_posix(),
            'duration': f"{mins}:{secs:02d}",
            'tags': self.tags,
            'type': self.type[1:]  # 'mp3'
        }


# Testdateien
MEDIA_DIR = "./media"  # Ordner, in dem deine Dateien liegen

import bottle

@bottle.route('/media/<filepath:path>')
def serve_media(filepath):
    return bottle.static_file(filepath, root=MEDIA_DIR)


# Funktion, um Medien zu scannen und an die GUI zu senden
@eel.expose("scan_media")
def scan_media():
    if not os.path.exists(MEDIA_DIR):
        os.makedirs(MEDIA_DIR)
        return {"error": "Ordner erstellt – füge Dateien hinzu"}
    media = []
    for f in Path(MEDIA_DIR).iterdir():
        if f.is_file() and f.suffix.lower() in {'.mp3', '.flac', '.ogg', '.wav', '.m4a'}:
            item = MediaItem(f.name, f)
            media.append(item.to_dict())
    return {"media": media}  # Reich an GUI mit Tags + Dauer

@eel.expose("play_media")
def play_media(path):
    """GUI ruft das an – aber HTML5 Audio handhabt Abspielen client-seitig."""
    return {"status": "play", "path": path}  # Bestätigung

# Main-Funktion, die die Eel-App startet
if __name__ == "__main__":
    eel.init("web")            # Ordner mit HTML/CSS/JS
    eel.start("index.html", size=(1000, 600))    # Starte Seite
