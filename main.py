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
# Duplikat-Erkennung



#Benötigte Module importieren
import eel # Electron-like Python Library for building desktop apps with web technologies
import sys
import os
from pathlib import Path
import subprocess
import re  # For MKV parsing

# kann raus. aber aktuell noch im code
import tkinter as tk
from tkinter import filedialog

# Konfiguration
# 1. Ort für den automatischen Bibliotheks-Scan
SCAN_MEDIA_DIR = str(Path(__file__).parent / "media")

# 2. Standard-Pfad beim ersten Öffnen des Browsers
BROWSER_DEFAULT_DIR = "/home/xc"





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




# Debug-Optionen
DEBUG_FLAGS = {
    "scan": False,
    "parser": False,
    "player": False,
    "db": False,
    "ffmpeg": False
}

LOG_BUFFER = []

def debug_log(message):
    print(message)
    LOG_BUFFER.append(str(message))
    # Eel-Aufruf (asynchron, wir warten nicht) - nur wenn verbunden/registriert
    if hasattr(eel, 'log_to_debug'):
        eel.log_to_debug(message)()

@eel.expose("get_debug_logs")
def get_debug_logs():
    """Gibt den gesamten bisherigen Log-Verlauf als String zurück."""
    return "\n".join(LOG_BUFFER)

@eel.expose("get_debug_flags")
def get_debug_flags():
    return DEBUG_FLAGS

@eel.expose("set_debug_flag")
def set_debug_flag(key, value):
    if key in DEBUG_FLAGS:
        DEBUG_FLAGS[key] = value
        debug_log(f"[Debug] Flag '{key}' auf {value} gesetzt.")

# Benutzerdefinierte Module
import db

# Eigene Parser
from parsers import media_parser

# Eigene bottle Web-Routen
from web import app_bottle



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
        self.duration, self.tags = media_parser.extract_metadata(self.path, self.name, debug=DEBUG_FLAGS["parser"])


    def show_info(self):
        print(self.name)
        print(self.path)
        print(self.type)
        print(self.duration)
        print(self.tags)
        print("\n")



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

@eel.expose("clear_database")
def clear_database():
    """Löscht alle Einträge aus der Bibliothek-Datenbank."""
    db.clear_media()
    return {"status": "ok", "message": "Datenbank geleert", "media": []}

@eel.expose("update_tags")
def update_tags(name, tags_dict):
    """Speichert angepasste Tags für ein Item in der DB."""
    db.update_media_tags(name, tags_dict)
    return {"status": "ok"}

@eel.expose("get_default_media_dir")
def get_default_media_dir():
    """Gibt den voreingestellten Medienordner (absolute Pfad) zurück."""
    return SCAN_MEDIA_DIR

# Funktion, um Medien zu scannen und an die GUI zu senden
@eel.expose("scan_media")
def scan_media(dir_path: str | None = None, clear_db: bool = True):
    """Scannt rekursiv einen Ordner und indexiert Audiodateien. Optionaler Reset der DB."""
    import time
    start_time = time.time()
    
    # Status in GUI anzeigen (falls verbunden)
    if hasattr(eel, 'set_db_status'):
        eel.set_db_status(True)()

    # Wenn kein Pfad übergeben wurde, nutzen wir den konfigurierten SCAN_MEDIA_DIR.
    # Wir stellen sicher, dass leere Strings ebenfalls als None behandelt werden.
    effective_path = dir_path if (dir_path and dir_path.strip()) else SCAN_MEDIA_DIR
    scan_root = Path(effective_path).resolve()
    
    debug_log(f"\n[Scan] Starting scan of: {scan_root}")
    
    if not scan_root.exists():
        try:
            scan_root.mkdir(parents=True, exist_ok=True)
            print(f"[Scan] Created missing directory: {scan_root}")
        except Exception as e:
            return {"error": f"Ordner nicht gefunden und konnte nicht erstellt werden: {e}"}
        return {"error": "Ordner erstellt – füge Dateien hinzu", "path": str(scan_root)}

    # DB optional leeren
    if clear_db:
        db.clear_media()

    count = 0
    # Rekursiv suchen, um Medien in Unterordnern zu finden
    for f in scan_root.rglob('*'):
        if f.is_file() and f.suffix.lower() in AUDIO_EXTENSIONS:
            # Überspringe den Transcoding-Cache, um Duplikate zu verhindern
            if '.cache' in f.parts:
                continue
            
            if DEBUG_FLAGS["scan"]:
                debug_log(f"[Debug-Scan] Verarbeite: {f.name}")
            try:
                item = MediaItem(f.name, f)
                db.insert_media(item.to_dict())
                count = count + 1
            except Exception as e:
                if DEBUG_FLAGS["scan"]:
                    debug_log(f"[Debug-Scan] Fehler bei {f.name}: {e}")
                # Ignoriere problematische Dateien, aber setze das Logging fort
                continue

    if hasattr(eel, 'set_db_status'):
        eel.set_db_status(False)()
    
    elapsed = time.time() - start_time
    debug_log(f"\n[Indexing] Scan complete. Processed {count} files in {elapsed:.2f} seconds.\n")

    # Status in GUI ausblenden (redundant, already handled by guard above)


    # Liefere gescannten Stand direkt aus der DB zurück
    return {
        "media": db.get_all_media(),
        "stats": {"count": count, "time_seconds": elapsed}
    }

@eel.expose("play_media")
def play_media(path):
    """GUI ruft das an – aber HTML5 Audio handhabt Abspielen client-seitig."""
    if DEBUG_FLAGS["player"]:
        print(f"[Debug-Player] Spiele ab: {path}")
    return {"status": "play", "path": path} # Bestätigung

@eel.expose("browse_dir")
def browse_dir(dir_path=None):
    """Listet Ordner und Audiodateien eines Verzeichnisses für den Datei-Browser."""
    if not dir_path:
        dir_path = BROWSER_DEFAULT_DIR
    
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

@eel.expose("pick_folder")
def pick_folder():
    """Öffnet einen nativen Ordner-Auswahldialog."""
    try:
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        folder_path = filedialog.askdirectory()
        root.destroy()
        return folder_path if folder_path else None
    except Exception as e:
        print(f"[Error] Folder picker failed: {e}")
        return None

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
    item_dict = item.to_dict()
    db.insert_media(item_dict)
    return {"status": "added", "item": item_dict}

# Main-Funktion, die die Eel-App startet
if __name__ == "__main__":
    # Logge den Start-Befehl (für das Debug-Fenster)
    startup_cmd = f"$ {sys.executable} {' '.join(sys.argv)}"
    debug_log(startup_cmd)

    db.init_db()               
    
    # Ensure scan dir exists and start initial indexing
    Path(SCAN_MEDIA_DIR).mkdir(parents=True, exist_ok=True)
    
    # Erst-Scan beim Start (nur für SCAN_MEDIA_DIR)
    scan_media(dir_path=None, clear_db=True)
    
    web_dir = str(Path(__file__).parent / "web")
    eel.init(web_dir)
    eel.start("app.html", size=(1200, 800))
