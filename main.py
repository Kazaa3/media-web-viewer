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

# logische trennung item / full object mit allen tags
#Parser-Zeiten:
#pymediainfo: 2.2ms • mutagen: 0.4ms • container: 0.0ms • filename: 0.0ms • ffmpeg: 51.0ms
#neu sortieren 1.filename 2.container 3. mutagen 4. pymediainfo 5. ffmpeg
# kapitel parser für 3 und 4
# string parser: wenn "zahl " vor dem Titel steht, dann ist das die Tracknummer, z.B. "02 Ludwig van Beethoven" --> Track 2
# container auslesen. mkv parsing. mkv hat keine tags. mkv hat nur streams. 
# cointainer nested aac parsen



### SCAN Debugging-Logs unvollständig bzw sind die einzigen


#Benötigte Module importieren
import eel # Electron-like Python Library for building desktop apps with web technologies
import sys
import os
import json
import time
import subprocess
import io
import contextlib
import pytest
from pathlib import Path
import re  # For MKV parsing

# kann raus. aber aktuell noch im code
import tkinter as tk
from tkinter import filedialog

# Konfiguration
# 1. Ort für den automatischen Bibliotheks-Scan
SCAN_MEDIA_DIR = str(Path(__file__).parent / "media")

# 2. Standard-Pfad beim ersten Öffnen des Browsers
BROWSER_DEFAULT_DIR = str(Path.home())





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

#mp4a.40.2 | 16 Bit (lossy) | 44.1 kHz | 320 kbps
#149.86 MB • Art: Yes
#File: M4B • Container: m4a • Tag Format: MP4Tags
#PCM_S16LE | 16 Bit (s16) | 44.1 kHz | 1411 kbps
#79.21 MB • Art: No
#File: wav • Container: wave
#Parser-Zeiten:
#pymediainfo: 10.0ms • mutagen: 0.3ms • container: übersprungen • filename: 0.0ms • ffmpeg: übersprungen
#die unetrkapitelsortierung ist nicht 1,2,3 sondern 1,21,22,2
# # debug flags menu
# mandatory unit test for all new components
# agenten gesteuerter browser test
# m4b sind immer hörbücher und nicht audio
#die unetrkapitelsortierung ist nicht 1,2,3 sondern 1,21,22,2
# alte einträge zu typ, container und tag ist weg und soll wieder in das linke seiten fenster des players
# tESTS IMMER hinzufügen

# Debug-Optionen
DEBUG_FLAGS = {
    "scan": False,
    "parser": False,
    "player": False,
    "db": False
}

LOG_BUFFER = []

def debug_log(message):
    print(message)
    LOG_BUFFER.append(str(message))
    # Eel-Aufruf (asynchron, wir warten nicht) - nur wenn verbunden/registriert
    if hasattr(eel, 'log_to_debug'):
        eel.log_to_debug(message)()

@eel.expose
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
from parsers.format_utils import PARSER_CONFIG

# Eigene bottle Web-Routen
from web import app_bottle

# Models
from models import MediaItem
#mkvinfo
#mediainfo
#mp3tag
# Untersützedateiformate als Liste

# Tags
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




# MediaItem logic moved to models.py



@eel.expose("get_library")
def get_library():
    """Gibt alle Medien aus der Datenbank zurück ohne neu zu scannen."""
    return {"media": db.get_all_media()}

@eel.expose("clear_database")
def clear_database():
    """Löscht alle Einträge aus der Bibliothek-Datenbank."""
    if DEBUG_FLAGS["db"]:
        debug_log("[Debug-DB] Tabelle wird geleert...")
    db.clear_media()
    return {"status": "ok", "message": "Datenbank geleert", "media": []}

@eel.expose("update_tags")
def update_tags(name, tags_dict):
    """Speichert angepasste Tags für ein Item in der DB."""
    if DEBUG_FLAGS["db"]:
        debug_log(f"[Debug-DB] Aktualisiere DB Tags für: {name}")
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
        debug_log(f"[Debug-Player] Spiele ab: {path}")
    return {"status": "play", "path": path} # Bestätigung

@eel.expose("open_in_explorer")
def open_in_explorer(path_str):
    print(f"Versuche zu oeffnen: {path_str}")
    path_obj = Path(path_str)
    if not path_obj.exists():
        print("Existiert nicht")
        return {"error": "Nicht gefunden"}
        
    try:
        # Check OS and open accordingly
        if os.name == 'nt':  # Windows
            os.startfile(path_str)
        elif sys.platform == 'darwin':  # macOS
            subprocess.run(['open', '-R', path_str])
        else:  # Linux (freedesktop)
            subprocess.run(['xdg-open', str(path_obj.parent)])
        return {"status": "ok"}
    except Exception as e:
        print(f"Fehler beim Oeffnen: {e}")
        return {"error": str(e)}

@eel.expose
def get_parser_config():
    """Returns the current parser configuration including the parser chain order."""
    sys.path.append(str(Path(__file__).parent)) # Ensure local imports work dynamically
    from parsers.format_utils import PARSER_CONFIG
    return PARSER_CONFIG

@eel.expose
def save_parser_config(new_config):
    """Updates and saves the parser configuration from the UI."""
    sys.path.append(str(Path(__file__).parent))
    from parsers.format_utils import PARSER_CONFIG, save_parser_config as save_config
    try:
        PARSER_CONFIG.update(new_config)
        save_config()
        return {"status": "ok"}
    except Exception as e:
        return {"error": str(e)}

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
    
    item = MediaItem(p.name, p, debug_flags=DEBUG_FLAGS, logger=debug_log)
    item_dict = item.to_dict()
    db.insert_media(item_dict)
    return {"status": "added", "item": item_dict}

@eel.expose
def run_tests(suites):
    """Führt ausgewählte pytest-Suiten aus und gibt die Ergebnisse zurück."""
    debug_log(f"[Tests] Running suites: {suites}")
    
    test_files = []
    if 'db' in suites: test_files.append("tests/test_db_logic.py")
    if 'media_item' in suites: test_files.append("tests/test_media_item_logic.py")
    if 'parser' in suites: test_files.append("tests/test_parser_logic.py")
    if 'chapters' in suites: test_files.append("tests/test_chapters_logic.py")
    
    if not test_files:
        return {"error": "Keine Test-Suiten ausgewählt."}

    # Capture stdout to get pytest report
    f = io.StringIO()
    with contextlib.redirect_stdout(f):
        exit_code = pytest.main(["-v"] + test_files)
    
    output = f.getvalue()
    return {
        "exit_code": int(exit_code),
        "output": output,
        "summary": "Tests passed" if exit_code == 0 else "Tests failed"
    }

@eel.expose
def run_gui_tests():
    """Dummy-Funktion für GUI-Tests (da diese über den Agenten laufen)."""
    # In einer realen App würde man hier vielleicht Selenium/Playwright fernsteuern.
    # Hier geben wir einfach einen Hinweis zurück.
    return {
        "status": "info",
        "message": "GUI-Tests müssen über den Antigravity-Agenten (Browser Subagent) gestartet werden."
    }

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
    
    # Block=False verhindert, dass eel.start() den Server sofort beendet (sys.exit), 
    # wenn Chrome den neuen Tab an einen bestehenden Prozess delegiert und sich sofort schließt.
    eel.start("app.html", size=(1200, 800), block=False)
    
    # Server am Leben halten
    while True:
        eel.sleep(1.0)
