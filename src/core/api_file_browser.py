import os
import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional, cast

from src.core.eel_shell import eel
from src.core.config_master import GLOBAL_CONFIG, AUDIO_EXTENSIONS, VIDEO_EXTENSIONS
from src.core.logger import get_logger

log = get_logger("api_file_browser")

# --- Configuration Handshake ---
BROWSER_DEFAULT_DIR = GLOBAL_CONFIG.get("file_browser_settings", {}).get("default_dir", str(Path.home()))

@eel.expose
def browse_dir(dir_path=None):
    """ Lists folders and media files for the in-app file browser. """
    if not dir_path:
        dir_path = BROWSER_DEFAULT_DIR

    target = Path(dir_path)
    if not target.exists() or not target.is_dir():
        log.warning(f"[Browser] Directory not found: {dir_path}")
        return {"error": "Ordner nicht gefunden", "path": dir_path}

    items = []
    try:
        # Sort: Directories first, then alphabetical
        entries = sorted(target.iterdir(), key=lambda e: (not e.is_dir(), e.name.lower()))
        for entry in entries:
            if entry.name.startswith('.'):
                continue
            
            if entry.is_dir():
                items.append({"name": entry.name, "path": str(entry), "type": "folder"})
            elif entry.suffix.lower() in AUDIO_EXTENSIONS or entry.suffix.lower() in VIDEO_EXTENSIONS:
                size_mb = entry.stat().st_size / (1024 * 1024)
                item_type = "video" if entry.suffix.lower() in VIDEO_EXTENSIONS else "audio"
                items.append({
                    "name": entry.name, "path": str(entry), 
                    "type": item_type, "size": f"{size_mb:.1f} MB"
                })
    except PermissionError:
        return {"error": "Keine Berechtigung", "path": dir_path}
    except Exception as e:
        log.error(f"[Browser] Error listing {dir_path}: {e}")
        return {"error": str(e), "path": dir_path}

    parent = str(target.parent) if target.parent != target else None
    return {"path": str(target), "parent": parent, "items": items}

@eel.expose
def pick_folder():
    """ Opens a native OS folder selection dialog using Tkinter. """
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
        log.error(f"[System] Folder picker failed: {e}")
        return None

@eel.expose
def pick_file():
    """ Opens a native OS file selection dialog. """
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        file_path = filedialog.askopenfilename()
        root.destroy()
        return file_path if file_path else None
    except Exception as e:
        log.error(f"[System] File picker failed: {e}")
        return None

@eel.expose
def open_in_explorer(path_str):
    """ Opens a specific path in the native OS file explorer (v1.54.022). """
    path_obj = Path(path_str)
    if not path_obj.exists():
        return {"error": "Nicht gefunden"}

    try:
        if os.name == 'nt': # Windows
            os.startfile(path_str)
        elif sys.platform == 'darwin': # macOS
            subprocess.run(['open', '-R', path_str])
        else: # Linux
            # Open parent folder and select if possible (standard behavior is just opening the parent)
            subprocess.run(['xdg-open', str(path_obj.parent)])
        return {"status": "ok"}
    except Exception as e:
        log.error(f"[Explorer] Error opening {path_str}: {e}")
        return {"error": str(e)}

@eel.expose
def delete_file(path_str):
    """ Safe file deletion with logging. """
    p = Path(path_str)
    if p.exists() and p.is_file():
        try:
            p.unlink()
            log.info(f"[Filesystem] Deleted file: {path_str}")
            return True
        except Exception as e:
            log.error(f"[Filesystem] Failed to delete file {path_str}: {e}")
    return False

@eel.expose
def write_file(path_str, content):
    """ Generic text file writer for logs or exports. """
    try:
        Path(path_str).write_text(content, encoding='utf-8')
        return True
    except Exception as e:
        log.error(f"[Filesystem] Failed to write file {path_str}: {e}")
        return False
