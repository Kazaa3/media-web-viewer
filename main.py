# main.py – Media Web Viewer
# Entry point: initializes Eel, exposes API functions to the frontend, and starts the app.
# (Startup print moved below)

#Benötigte Module importieren
import eel # Electron-like Python Library for building desktop apps with web technologies
import sys
import os
import json
import time
import subprocess
import io
import contextlib
from pathlib import Path
import re  # For MKV parsing
from parsers.format_utils import PARSER_CONFIG, load_parser_config, save_parser_config, AUDIO_EXTENSIONS, VIDEO_EXTENSIONS, DOCUMENT_EXTENSIONS, EBOOK_EXTENSIONS

VERSION = "1.1.16"

@eel.expose("get_version")
def get_version():
    """Gibt die aktuelle Versionsnummer zurück."""
    return VERSION

# Konfiguration
# 1. Ort für den automatischen Bibliotheks-Scan
SCAN_MEDIA_DIR = str(Path(__file__).parent / "media")

# 2. Standard-Pfad beim ersten Öffnen des Browsers
BROWSER_DEFAULT_DIR = str(Path.home())
# Redundante Definitionen entfernt, da diese nun aus parsers.format_utils importiert werden.
# (AUDIO_EXTENSIONS, VIDEO_EXTENSIONS etc. werden oben importiert)
IMAGE_EXTENSIONS = {
    '.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp', '.svg', '.ico'
}
ARCHIVE_EXTENSIONS = {
    '.zip', '.rar', '.7z', '.tar', '.gz', '.bz2', '.xz'
}   


# Debug-Optionen
DEBUG_FLAGS = {
    "system": False,
    "ui": False,
    "lib": False,
    "browser": False,
    "edit": False,
    "options": False,
    "start": False,
    "parser": False,
    "scan": False,
    "player": False,
    "db": False,
    "tests": False
}

# Full Debug Mode: If --debug argument is passed, set all flags to True
if "--debug" in sys.argv:
    for key in DEBUG_FLAGS:
        DEBUG_FLAGS[key] = True
    print("[System] Full Debug-Mode activated (--debug). All flags set to True.")

LOG_BUFFER = []

if DEBUG_FLAGS["start"]:
    debug_log("[Startup] main.py loading...")

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

@eel.expose("set_all_debug_flags")
def set_all_debug_flags(value):
    """Aktiviert oder deaktiviert alle Debug-Flags gleichzeitig."""
    for key in DEBUG_FLAGS:
        DEBUG_FLAGS[key] = value
    debug_log(f"[Debug] Alle Flags wurden auf {value} gesetzt.")

@eel.expose("get_language")
def get_language():
    """Gibt die aktuell gewählte Sprache zurück."""
    return PARSER_CONFIG.get("language", "de")

@eel.expose("set_language")
def set_language(lang):
    """Setzt die Sprache der Anwendung."""
    PARSER_CONFIG["language"] = lang
    save_parser_config()
    if DEBUG_FLAGS["system"]:
        debug_log(f"[System] Sprache auf '{lang}' gesetzt.")
    return True

# Benutzerdefinierte Module
import db

# Eigene Parser
from parsers import media_parser

# Eigene bottle Web-Routen
from web import app_bottle

# Models
from models import MediaItem


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

@eel.expose("reset_app_data")
def reset_app_data():
    """Löscht Datenbank und Konfigurationsdateien (Private Daten)."""
    import shutil
    from pathlib import Path
    
    deleted = []
    
    # Paths to clear:
    # 1. ~/.media-web-viewer (Database)
    db_dir = db.DB_DIR
    # 2. ~/.config/gui_media_web_viewer (Parser Config)
    config_dir = Path.home() / ".config" / "gui_media_web_viewer"
    
    for p in [db_dir, config_dir]:
        if p.exists():
            try:
                if p.is_dir():
                    shutil.rmtree(p, ignore_errors=True)
                else:
                    p.unlink()
                deleted.append(str(p))
            except Exception as e:
                debug_log(f"[Error] Reset failed for {p}: {e}")

    # Re-initialize to avoid crash on next actions
    db.init_db()
    save_parser_config() # Create default config
    load_parser_config() # Sync local PARSER_CONFIG in memory
    
    if DEBUG_FLAGS["system"]:
        debug_log(f"[System] Reset complete. Deleted: {', '.join(deleted)}")
    return {"status": "ok", "deleted": deleted}

@eel.expose("update_tags")
def update_tags(name, tags_dict):
    """Speichert angepasste Tags für ein Item in der DB."""
    if DEBUG_FLAGS["db"]:
        debug_log(f"[Debug-DB] Aktualisiere DB Tags für: {name}")
    db.update_media_tags(name, tags_dict)
    return {"status": "ok"}

@eel.expose("rename_media")
def rename_media(old_name, new_name):
    """Benennt ein Medium in der DB um."""
    if not new_name or new_name.strip() == "":
        return {"status": "error", "message": "Name darf nicht leer sein"}
    
    if DEBUG_FLAGS["db"]:
        debug_log(f"[Debug-DB] Benenne um: {old_name} -> {new_name}")
    
    success = db.rename_media(old_name, new_name)
    if success:
        return {"status": "ok"}
    else:
        return {"status": "error", "message": "Name bereits vorhanden oder Fehler"}

@eel.expose
def delete_media(name):
    return db.delete_media(name)

@eel.expose
def get_db_stats():
    return db.get_db_stats()

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

    start_time = time.time()
    # DB optional leeren
    if clear_db:
        db.clear_media()

    # Determine which directories to scan
    scan_roots = []
    if dir_path and dir_path.strip():
        scan_roots.append(Path(dir_path).resolve())
    else:
        # Use all directories from config
        config_dirs = PARSER_CONFIG.get("scan_dirs", [SCAN_MEDIA_DIR])
        for d in config_dirs:
            p = Path(d).resolve()
            if p.exists():
                scan_roots.append(p)
            else:
                debug_log(f"[Scan] Skipping non-existent directory: {d}")

    count = 0
    for scan_root in scan_roots:
        if DEBUG_FLAGS.get("scan"):
            debug_log(f"\n[Scan] Starting scan of: {scan_root}")
        
        # Rekursiv suchen, um Medien in Unterordnern zu finden
        for f in scan_root.rglob('*'):
            if f.is_file() and f.suffix.lower() in AUDIO_EXTENSIONS:
                # Überspringe den Transcoding-Cache, um Duplikate zu verhindern
                if '.cache' in f.parts:
                    continue
                
                # Blacklist für unerwünschte Dateien (Cover-Art, Captcha, etc.)
                name_lower = f.name.lower()
                if any(x in name_lower for x in ['cover art', 'captcha', 'thumb', 'folder', 'albumart', 'al_cave']):
                    continue
                
                if DEBUG_FLAGS["scan"]:
                    debug_log(f"[Debug-Scan] Verarbeite: {f.name}")
                try:
                    item = MediaItem(f.name, f)
                    item_dict = item.to_dict()
                    if DEBUG_FLAGS["db"]:
                        debug_log(f"[DB-Insert] {f.name} (Category: {item_dict.get('category')}) from {f.parent}")
                    db.insert_media(item_dict)
                    count += 1
                except Exception as e:
                    if DEBUG_FLAGS["scan"]:
                        debug_log(f"[Debug-Scan] Fehler bei {f.name}: {e}")
                    # Ignoriere problematische Dateien, aber setze das Logging fort
                    continue

    if hasattr(eel, 'set_db_status'):
        eel.set_db_status(False)()
    
    elapsed = time.time() - start_time
    if DEBUG_FLAGS.get("scan"):
        debug_log(f"\n[Indexing] Scan complete. Processed {count} files in {elapsed:.2f} seconds.\n")

    # Status in GUI ausblenden (redundant, already handled by guard above)


    # Liefere gescannten Stand direkt aus der DB zurück
    return {
        "media": db.get_all_media(),
        "stats": {"count": count, "time_seconds": elapsed}
    }

@eel.expose("get_parser_config")
def get_parser_config():
    """Gibt die aktuelle Parser-Konfiguration an das Frontend zurück."""
    return PARSER_CONFIG

@eel.expose("update_parser_config")
def update_parser_config(new_config):
    """Aktualisiert die Konfiguration und speichert sie auf Festplatte."""
    PARSER_CONFIG.update(new_config)
    save_parser_config()
    return {"status": "ok"}

@eel.expose("add_scan_dir")
def add_scan_dir():
    """Öffnet einen Dialog zur Auswahl eines neuen Scan-Verzeichnisses."""
    new_dir = pick_folder()
    if new_dir:
        dirs = PARSER_CONFIG.get("scan_dirs", [])
        if new_dir not in dirs:
            dirs.append(new_dir)
            PARSER_CONFIG["scan_dirs"] = dirs
            save_parser_config()
            return {"status": "ok", "dirs": dirs}
    return {"status": "cancel"}

@eel.expose("remove_scan_dir")
def remove_scan_dir(dir_path):
    """Entfernt ein Verzeichnis aus der Scan-Liste."""
    dirs = PARSER_CONFIG.get("scan_dirs", [])
    if dir_path in dirs:
        dirs.remove(dir_path)
        PARSER_CONFIG["scan_dirs"] = dirs
        save_parser_config()
        return {"status": "ok", "dirs": dirs}
    return {"status": "error", "message": "Pfand nicht in Liste"}

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
        import tkinter as tk
        from tkinter import filedialog
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
def get_test_suites():
    """Discover all test files in the tests/ directory and extract metadata."""
    test_dir = Path(__file__).parent / "tests"
    if not test_dir.exists():
        return []
    
    suites = []
    for f in sorted(test_dir.glob("*.py")):
        if f.name.startswith("test_") or f.name.startswith("benchmark_"):
            try:
                content = f.read_text(encoding='utf-8')
            except Exception:
                content = ""
            
            metadata = {
                "category": "-",
                "inputs": "-",
                "outputs": "-",
                "files": "-",
                "comment": "-"
            }
            
            for line in content.splitlines():
                if line.startswith("# Kategorie:"): metadata["category"] = line.split(":", 1)[1].strip()
                elif line.startswith("# Eingabewerte:"): metadata["inputs"] = line.split(":", 1)[1].strip()
                elif line.startswith("# Ausgabewerte:"): metadata["outputs"] = line.split(":", 1)[1].strip()
                elif line.startswith("# Testdateien:"): metadata["files"] = line.split(":", 1)[1].strip()
                elif line.startswith("# Kommentar:"): metadata["comment"] = line.split(":", 1)[1].strip()

            display_name = f.stem.replace("test_", "").replace("benchmark_", "Benchmark: ").replace("_", " ").title()
            suites.append({
                "id": f.name,
                "name": display_name,
                "path": str(f),
                "metadata": metadata
            })
    return suites

@eel.expose
def update_test_metadata(filename, metadata):
    """Updates the metadata comments in a test file."""
    test_dir = Path(__file__).parent / "tests"
    file_path = test_dir / filename
    
    if not file_path.exists():
        return {"error": "Test-Datei nicht gefunden"}
        
    try:
        content = file_path.read_text(encoding='utf-8')
        lines = content.splitlines()
        
        # Remove existing metadata lines
        new_lines = []
        for line in lines:
            if not any(line.startswith(prefix) for prefix in [
                "# Kategorie:", "# Eingabewerte:", "# Ausgabewerte:", "# Testdateien:", "# Kommentar:"
            ]):
                new_lines.append(line)
        
        # Prepend new metadata
        header = [
            f"# Kategorie: {metadata.get('category', '-')}",
            f"# Eingabewerte: {metadata.get('inputs', '-')}",
            f"# Ausgabewerte: {metadata.get('outputs', '-')}",
            f"# Testdateien: {metadata.get('files', '-')}",
            f"# Kommentar: {metadata.get('comment', '-')}",
            ""  # Add empty line after metadata
        ]
        
        # Join lines with proper newline handling
        # Skip leading empty lines if there are any after removing metadata
        while new_lines and not new_lines[0].strip():
            new_lines.pop(0)

        final_content = "\n".join(header + new_lines)
        file_path.write_text(final_content, encoding='utf-8')
        return {"status": "ok"}
    except Exception as e:
        return {"error": str(e)}

@eel.expose
def create_new_test(name):
    """Creates a new test file with a basic template."""
    test_dir = Path(__file__).parent / "tests"
    test_dir.mkdir(parents=True, exist_ok=True)
    
    # Sanitize name
    safe_name = "".join([c for c in name if c.isalnum() or c in (' ', '_', '-')]).strip().replace(' ', '_')
    if not safe_name.startswith('test_'):
        safe_name = f"test_{safe_name}"
    
    filename = f"{safe_name}.py"
    file_path = test_dir / filename
    
    if file_path.exists():
        return {"status": "error", "message": "Test existiert bereits"}
        
    template = f"""# Kategorie: -
# Eingabewerte: -
# Ausgabewerte: -
# Testdateien: -
# Kommentar: Neuer Test

import pytest

def {safe_name}():
    # Hier Test-Code schreiben
    assert True
"""
    try:
        file_path.write_text(template, encoding='utf-8')
        return {"status": "ok", "filename": filename}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@eel.expose
def delete_test(filename):
    """Löscht eine Test-Datei."""
    test_dir = Path(__file__).parent / "tests"
    file_path = test_dir / filename
    
    if not file_path.exists():
        return {"status": "error", "message": "Datei nicht gefunden"}
        
    try:
        file_path.unlink()
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@eel.expose
def get_logbook_entry(feature_name):
    """Read a markdown file from the logbuch directory or README from main dir."""
    if feature_name.upper() == "README" or feature_name.upper() == "README.MD":
        log_file = Path(__file__).parent / "README.md"
    else:
        log_file = Path(__file__).parent / "logbuch" / f"{feature_name}.md"
        if not log_file.exists():
            # Fallback without extension just in case it was passed directly
            log_file = Path(__file__).parent / "logbuch" / feature_name
            
    if not log_file.exists():
        return f"<h1>Error</h1><p>Logbook entry for '{feature_name}' not found.</p>"
    
    try:
        content = log_file.read_text(encoding='utf-8')
        # Simple markdown to HTML conversion (basic bold/header)
        # In a real app we'd use 'markdown' library, but let's keep it simple or use JS side.
        return content
    except Exception as e:
        return f"<h1>Error</h1><p>{str(e)}</p>"

@eel.expose
def list_logbook_entries():
    """Gibt eine Liste aller Markdown-Dateien im logbuch/ Ordner mit Metadaten zurück."""
    log_dir = Path(__file__).parent / "logbuch"
    if not log_dir.exists():
        return []
    
    entries = []
    # Natural sort by filename
    for f in sorted(log_dir.glob("*.md")):
        try:
            with open(f, 'r', encoding='utf-8') as fp:
                lines = [fp.readline() for _ in range(10)] # Mehr Zeilen lesen um alles zu finden
                category = "Sonstiges"
                summary = ""
                status = "COMPLETED" # Default
                title = f.stem
                
                title_de = ""
                title_en = ""
                summary_de = ""
                summary_en = ""
                
                for line in lines:
                    line = line.strip()
                    if "<!-- Category:" in line:
                        category = line.split("Category: ")[1].split(" -->")[0]
                    if "<!-- Summary:" in line:
                        summary = line.split("Summary: ")[1].split(" -->")[0]
                    if "<!-- Summary_DE:" in line:
                        summary_de = line.split("Summary_DE: ")[1].split(" -->")[0]
                    if "<!-- Summary_EN:" in line:
                        summary_en = line.split("Summary_EN: ")[1].split(" -->")[0]
                    if "<!-- Status:" in line:
                        status = line.split("Status: ")[1].split(" -->")[0]
                    if "<!-- Title_DE:" in line:
                        title_de = line.split("Title_DE: ")[1].split(" -->")[0]
                    if "<!-- Title_EN:" in line:
                        title_en = line.split("Title_EN: ")[1].split(" -->")[0]
                    if line.startswith("# "):
                        title = line.replace("# ", "").strip()
                
                # Fallbacks
                if not title_de: title_de = title
                if not title_en: title_en = title
                if not summary_de: summary_de = summary
                if not summary_en: summary_en = summary

                entries.append({
                    "name": f.stem,
                    "filename": f.name,
                    "title": title,
                    "title_de": title_de,
                    "title_en": title_en,
                    "category": category,
                    "summary": summary,
                    "summary_de": summary_de,
                    "summary_en": summary_en,
                    "status": status
                })
        except Exception:
            entries.append({
                "name": f.stem,
                "filename": f.name,
                "title": f.stem,
                "category": "Fehler",
                "summary": "",
                "status": "ERROR"
            })
    
    return entries

@eel.expose
def save_logbook_entry(filename, content):
    """Speichert oder aktualisiert einen Logbuch-Eintrag."""
    log_dir = Path(__file__).parent / "logbuch"
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # Sichere den Dateinamen
    if not filename.endswith('.md'):
        filename = filename + '.md'
    
    # Verhindere Directory Traversal
    if '/' in filename or '\\' in filename or filename.startswith('.'):
        return {"error": "Ungültiger Dateiname"}
    
    file_path = log_dir / filename
    
    try:
        file_path.write_text(content, encoding='utf-8')
        return {"status": "ok", "filename": filename}
    except Exception as e:
        return {"error": str(e)}

@eel.expose
def delete_logbook_entry(filename):
    """Löscht einen Logbuch-Eintrag."""
    log_dir = Path(__file__).parent / "logbuch"
    
    if not filename.endswith('.md'):
        filename = filename + '.md'
    
    # Verhindere Directory Traversal
    if '/' in filename or '\\' in filename or filename.startswith('.') or '..' in filename:
        return {"error": "Ungültiger Dateiname"}
    
    file_path = log_dir / filename
    
    if not file_path.exists():
        return {"error": "Datei nicht gefunden"}
    
    try:
        file_path.unlink()
        return {"status": "ok"}
    except Exception as e:
        return {"error": str(e)}

@eel.expose
def run_tests(test_files):
    """Führt ausgewählte pytest-Suiten aus und gibt die Ergebnisse zurück."""
    import pytest  # Nur lokal importieren – nicht als globale Abhängigkeit
    if DEBUG_FLAGS.get("tests"):
        debug_log(f"[Tests] Running files: {test_files}")
    
    if not test_files:
        return {"error": "Keine Test-Suiten ausgewählt."}

    # Verify files exist
    valid_files = []
    for tf in test_files:
        p = Path(__file__).parent / "tests" / tf
        if p.exists():
            valid_files.append(str(p))
    
    if not valid_files:
        return {"error": "Keine gültigen Test-Dateien gefunden."}

    # Capture stdout to get pytest report
    f = io.StringIO()
    # We need to set PYTHONPATH so tests can import models/parsers
    env = os.environ.copy()
    env["PYTHONPATH"] = str(Path(__file__).parent)
    
    # Run pytest in a subprocess to avoid issues with repeat runs/sys.modules
    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", "-v"] + valid_files,
            capture_output=True,
            text=True,
            env=env,
            cwd=str(Path(__file__).parent)
        )
        
        output = result.stdout + "\n" + result.stderr
        
        # Parse output for passed/failed
        import re
        passes = 0
        fails = 0
        match = re.search(r'==.*?\s(\d+)\s+passed', output)
        if match:
            passes = int(match.group(1))
        match_fails = re.search(r'==.*?\s(\d+)\s+failed', output)
        if match_fails:
            fails = int(match_fails.group(1))
            
        summary = f"{passes} passed, {fails} failed"
        
        return {
            "exit_code": result.returncode,
            "output": output,
            "summary": summary,
            "passes": passes,
            "fails": fails
        }
    except Exception as e:
        return {"error": str(e)}

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
    # Only print on startup if a debug flag is active (though usually all are False initially)
    # Append to LOG_BUFFER silently so it's visible in the debug window later
    LOG_BUFFER.append(startup_cmd)
    if any(DEBUG_FLAGS.values()):
        print(startup_cmd)

    db.init_db()               
    
    # Ensure scan dirs exist and start initial indexing
    config_dirs = PARSER_CONFIG.get("scan_dirs", [SCAN_MEDIA_DIR])
    for d in config_dirs:
        Path(d).mkdir(parents=True, exist_ok=True)
    
    # Erst-Scan beim Start (alle konfigurierten Verzeichnisse)
    # In einem Thread, damit die GUI sofort erscheint
    import threading
    threading.Thread(target=lambda: scan_media(dir_path=None, clear_db=True), daemon=True).start()
    
    web_dir = str(Path(__file__).parent / "web")
    eel.init(web_dir)
    
    if DEBUG_FLAGS["start"]:
        print("[Startup] Starting Eel UI...")
    # Block=False verhindert, dass eel.start() den Server sofort beendet (sys.exit), 
    # wenn Chrome den neuen Tab an einen bestehenden Prozess delegiert und sich sofort schließt.
    # port=0 sucht automatisch einen freien Port
    try:
        eel.start("app.html", size=(1350, 800), block=False, port=0)
    except Exception as e:
        print(f"[Startup-Error] eel.start failed: {e}")
    
    # Server am Leben halten
    while True:
        eel.sleep(1.0)
