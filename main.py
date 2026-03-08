#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Media Web Viewer - Desktop Media Player and Library Manager

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

# main.py – Entry point: initializes Eel, exposes API functions to the frontend, and starts the app.

import sys
import os
import platform

def _detect_python_environment():
    """
    Detect current Python environment: system, venv, or conda.
    Returns tuple: (env_type, env_name, env_path, python_version, python_executable)
    """
    python_version = platform.python_version()
    python_executable = sys.executable
    
    # Check for conda
    conda_env = os.environ.get('CONDA_DEFAULT_ENV')
    conda_prefix = os.environ.get('CONDA_PREFIX')
    
    if conda_env and conda_prefix:
        return ('conda', conda_env, conda_prefix, python_version, python_executable)
    
    # Check for venv
    in_venv = sys.prefix != sys.base_prefix
    venv_env = os.environ.get('VIRTUAL_ENV')
    
    if in_venv or venv_env:
        env_path = venv_env or sys.prefix
        env_name = Path(env_path).name if env_path else 'venv'
        return ('venv', env_name, env_path, python_version, python_executable)
    
    # System Python
    return ('system', None, sys.prefix, python_version, python_executable)

# Benötigte Module importieren
try:
    from models import MediaItem
    import db
except ModuleNotFoundError as exc:
    from pathlib import Path
    
    missing_module = exc.name or "unknown"
    env_type, env_name, env_path, py_ver, py_exec = _detect_python_environment()
    
    # Build environment info string
    if env_type == 'conda':
        current_env = f"🐍 Conda: {env_name}\n   Pfad: {env_path}\n   Python: {py_exec}"
    elif env_type == 'venv':
        current_env = f"📦 Venv: {env_name}\n   Pfad: {env_path}\n   Python: {py_exec}"
    else:
        current_env = f"⚙️  System Python {py_ver}\n   Python: {py_exec}"
    
    print(
        f"\n❌ Abhängigkeit '{missing_module}' nicht installiert!\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📍 Aktuelle Umgebung:\n   {current_env}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"✅ Lösung: Starte mit der Projekt-Umgebung:\n\n"
        f"   cd /home/xc/#Coding/gui_media_web_viewer\n"
        f"   source .venv/bin/activate\n"
        f"   python main.py\n\n"
        f"Falls .venv fehlt:\n"
        f"   python3 -m venv .venv\n"
        f"   source .venv/bin/activate\n"
        f"   pip install -r requirements.txt\n\n"
        f"Alternative: Mit Conda (falls verfügbar):\n"
        f"   conda activate <env-name>\n"
        f"   pip install -r requirements.txt\n"
        f"   python main.py\n"
    )
    raise SystemExit(1) from exc

import eel
import logging
import time
import subprocess
import re
from typing import cast
from pathlib import Path
from parsers.format_utils import (
    PARSER_CONFIG, load_parser_config, save_parser_config,
    AUDIO_EXTENSIONS, VIDEO_EXTENSIONS
)
import logger
import env_handler
try:
    import vlc
    HAS_VLC = True
except ImportError:
    HAS_VLC = False

try:
    import m3u8
    HAS_M3U8 = True
except ImportError:
    HAS_M3U8 = False

# Version laden
VERSION_FILE = Path(__file__).parent / "VERSION"
try:
    VERSION = VERSION_FILE.read_text(encoding='utf-8').strip()
except Exception:
    VERSION = "1.2.23"  # Fallback


@eel.expose
def get_version():
    """
    @brief Returns the current version number.
    @details Gibt die aktuelle Versionsnummer zurück.
    @return Version string / Versions-String.
    """
    return VERSION


@eel.expose
def get_environment_info():
    """
    @brief Returns comprehensive information about the Python environment.
    @details Gibt detaillierte Informationen über die Python-Umgebung zurück, 
             inklusive aktuelle Umgebung, System Python Installationen, und Conda Umgebungen.
    @return Dictionary with environment details / Dictionary mit Umgebungsdetails.
    """
    import platform
    import subprocess
    import json
    
    # ===== Current Environment =====
    # Check if we're in a virtual environment (venv/virtualenv)
    in_venv = sys.prefix != sys.base_prefix
    venv_path = sys.prefix if in_venv else None
    
    # Get VIRTUAL_ENV environment variable (more reliable for venv)
    venv_env = os.environ.get('VIRTUAL_ENV', None)
    
    # Check for Conda environment
    conda_env_name = os.environ.get('CONDA_DEFAULT_ENV', None)
    conda_prefix = os.environ.get('CONDA_PREFIX', None)
    in_conda = conda_env_name is not None or conda_prefix is not None
    
    # Determine current environment type and path
    env_type = None
    env_path = None
    env_name = None
    
    if in_conda:
        env_type = "conda"
        env_path = conda_prefix
        env_name = conda_env_name
    elif in_venv or venv_env:
        env_type = "venv"
        env_path = venv_path or venv_env
        env_name = Path(env_path).name if env_path else None
    else:
        env_type = "system"
    
    # Build current environment info
    current_env = {
        "type": env_type,
        "name": env_name,
        "path": env_path,
        "python_version": platform.python_version(),
        "python_executable": sys.executable,
    }
    
    # ===== Alternative Environments Discovery =====
    
    def _get_conda_environments():
        """Get list of available Conda environments."""
        environments = []
        try:
            result = subprocess.run(
                ["conda", "env", "list", "--json"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                data = json.loads(result.stdout)
                for env_path in data.get("envs", []):
                    env_name = Path(env_path).name
                    env_python = Path(env_path) / "bin" / "python"
                    
                    if env_python.exists():
                        try:
                            v_result = subprocess.run(
                                [str(env_python), "--version"],
                                capture_output=True,
                                text=True,
                                timeout=2
                            )
                            version = v_result.stdout.strip() or v_result.stderr.strip()
                            is_recommended = env_name == "p14"
                            
                            environments.append({
                                "name": env_name,
                                "path": env_path,
                                "version": version,
                                "recommended": is_recommended
                            })
                        except Exception:
                            pass
        except Exception:
            pass
        return sorted(environments, key=lambda x: x["name"])
    
    def _get_system_pythons():
        """Get list of system Python installations."""
        pythons = []
        search_paths = ["/usr/bin", "/usr/local/bin", "/opt/python"]
        seen_versions = set()
        
        for search_path in search_paths:
            search_dir = Path(search_path)
            if not search_dir.exists():
                continue
            
            for python_exe in search_dir.glob("python*"):
                if not python_exe.is_file() or not os.access(python_exe, os.X_OK):
                    continue
                
                try:
                    result = subprocess.run(
                        [str(python_exe), "--version"],
                        capture_output=True,
                        text=True,
                        timeout=2
                    )
                    version = result.stdout.strip() or result.stderr.strip()
                    
                    if version and version not in seen_versions:
                        seen_versions.add(version)
                        pythons.append({
                            "path": str(python_exe),
                            "version": version
                        })
                except Exception:
                    pass
        
        return sorted(pythons, key=lambda x: x["version"])
    
    def _get_installed_packages():
        """Get list of installed packages in current environment."""
        packages = []
        try:
            result = subprocess.run(
                [sys.executable, "-m", "pip", "list", "--format=json"],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                packages_data = json.loads(result.stdout)
                # Sort by name
                packages = sorted(packages_data, key=lambda x: x["name"].lower())
        except Exception as e:
            logging.warning(f"Failed to get installed packages: {e}")
        return packages
    
    def _find_local_venvs():
        """Find local venv directories in common locations."""
        venvs = []
        venv_names = [".venv", "venv", "env", ".env"]
        
        # Check project directory
        project_dir = Path(__file__).parent
        for venv_name in venv_names:
            venv_path = project_dir / venv_name
            if venv_path.exists() and (venv_path / "bin" / "python").exists():
                python_exe = venv_path / "bin" / "python"
                try:
                    result = subprocess.run(
                        [str(python_exe), "--version"],
                        capture_output=True,
                        text=True,
                        timeout=2
                    )
                    version = result.stdout.strip() or result.stderr.strip()
                    venvs.append({
                        "name": venv_name,
                        "path": str(venv_path),
                        "version": version,
                        "is_current": str(venv_path) == env_path
                    })
                except Exception:
                    pass
        
        return venvs
    
    # Discover available environments (cached/fast)
    conda_envs = _get_conda_environments()
    system_pythons = _get_system_pythons()
    installed_packages = _get_installed_packages()
    local_venvs = _find_local_venvs()
    
    # ===== Build Response =====
    return {
        # Current Environment (Primary)
        "python_version": platform.python_version(),
        "python_executable": sys.executable,
        "python_prefix": sys.prefix,
        "python_base_prefix": sys.base_prefix,
        "in_venv": in_venv,
        "venv_path": venv_path or venv_env,
        "in_conda": in_conda,
        "conda_env_name": conda_env_name,
        "conda_prefix": conda_prefix,
        "env_type": env_type,
        "env_path": env_path,
        "env_name": env_name,
        "platform": platform.platform(),
        "platform_system": platform.system(),
        "platform_release": platform.release(),
        
        # Current Environment (Detailed)
        "current_environment": current_env,
        
        # Alternative Environments (Discovery Results)
        "available_conda_environments": conda_envs,
        "available_system_pythons": system_pythons,
        "local_venvs": local_venvs,
        
        # Installed Packages
        "installed_packages": installed_packages,
        "package_count": len(installed_packages),
        
        # Recommendations
        "recommended_environment": {
            "name": "p14",
            "type": "conda",
            "python_version": "3.14.2",
            "reason": "Latest stable Python release for Media Web Viewer"
        }
    }


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
    "tests": False,
    "api": False,
    "web": False,
    "i18n": False,
    "websocket": False,
    "performance": False,
    "metadata": False,
    "transcode": False,
    "file_ops": False,
    "network": False
}

def initialize_debug_flags(args=None):
    """
    @brief Initializes debug mode and flags based on CLI arguments.
    """
    if args is None:
        args = sys.argv
    
    debug_mode = "--debug" in args
    logger.setup_logging(debug_mode)
    
    if debug_mode:
        for key in DEBUG_FLAGS:
            DEBUG_FLAGS[key] = True
        logger.set_debug_flags(DEBUG_FLAGS)
        logging.info("[System] Full Debug-Mode activated (--debug). All flags set to True.")
    else:
        logger.set_debug_flags(DEBUG_FLAGS)

# Initialize logging early with default sys.argv
initialize_debug_flags()

# Ensure we are running in a clean and exclusive environment
env_handler.validate_safe_startup()

# Log environment information at startup
def _log_environment_info():
    """Log Python environment details at startup."""
    env_type, env_name, env_path, py_ver, py_exec = _detect_python_environment()
    
    logging.info("═" * 60)
    logging.info("[Startup] Application started - Environment Information")
    logging.info("─" * 60)
    
    if env_type == 'conda':
        logging.info(f"  Environment Type: Conda")
        logging.info(f"  Environment Name: {env_name}")
        logging.info(f"  Environment Path: {env_path}")
    elif env_type == 'venv':
        logging.info(f"  Environment Type: Virtual Environment (venv)")
        logging.info(f"  Environment Name: {env_name}")
        logging.info(f"  Environment Path: {env_path}")
    else:
        logging.info(f"  Environment Type: System Python")
        logging.info(f"  Environment Path: {env_path}")
    
    logging.info(f"  Python Version: {py_ver}")
    logging.info(f"  Python Executable: {py_exec}")
    logging.info("═" * 60)

_log_environment_info()


def debug_log(message: str) -> None:
    """
    @brief Universal logging helper (bridged to central logging system).
    """
    logging.info(message)
    # Eel callback if front-end is already listening
    try:
        if hasattr(eel, 'log_to_debug'):
            eel.log_to_debug(message)()
    except Exception:
        pass


if DEBUG_FLAGS["start"]:
    debug_log("[Startup] main.py loading...")

# Removed redundant debug flag processing (now in initialize_debug_flags)


@eel.expose
def get_debug_logs():
    """
    @brief Returns the entire log history as a single string.
    @details Gibt den gesamten bisherigen Log-Verlauf als String zurück.
    @return Multi-line log string / Mehrzeiliger Log-String.
    """
    return "\n".join(logger.get_ui_logs())


@eel.expose
def get_debug_flags():
    """
    @brief Returns the current internal debug flags.
    @details Gibt die aktuell gesetzten internen Debug-Flags zurück.
    @return Dictionary of debug flags / Dictionary der Debug-Flags.
    """
    return DEBUG_FLAGS


@eel.expose
def set_debug_flag(key, value):
    """
    @brief Sets a specific debug flag.
    @details Setzt ein spezifisches Debug-Flag.
    @param key Flag name / Name des Flags.
    @param value Boolean value / Boole'scher Wert.
    """
    if key in DEBUG_FLAGS:
        DEBUG_FLAGS[key] = value
        debug_log(f"[Debug] Flag '{key}' auf {value} gesetzt.")


@eel.expose
def set_all_debug_flags(value):
    """
    @brief Activates or deactivates all debug flags simultaneously.
    @details Aktiviert oder deaktiviert alle Debug-Flags gleichzeitig.
    @param value Boolean value / Boole'scher Wert.
    """
    for key in DEBUG_FLAGS:
        DEBUG_FLAGS[key] = value
    debug_log(f"[Debug] Alle Flags wurden auf {value} gesetzt.")


@eel.expose
def get_language():
    """
    @brief Returns the currently selected UI language.
    @details Gibt die aktuell gewählte Sprache zurück.
    @return Language code (e.g. 'de', 'en') / Sprachcode.
    """
    return PARSER_CONFIG.get("language", "de")


@eel.expose
def set_language(lang):
    """
    @brief Sets the UI language of the application.
    @details Setzt die Sprache der Anwendung.
    @param lang Language code / Sprachcode.
    @return True if successful / True falls erfolgreich.
    """
    PARSER_CONFIG["language"] = lang
    save_parser_config()
    if DEBUG_FLAGS["system"]:
        debug_log(f"[System] Sprache auf '{lang}' gesetzt.")
    return True


# Benutzerdefinierte Module

# Eigene Parser
# from parsers import media_parser (Importing for side effects if needed, but unused here)


# Eigene bottle Web-Routen
# from web import app_bottle (Importing for side effects if needed, but unused here)

# Models


@eel.expose
def get_library():
    """
    @brief Returns all media items from the database without re-scanning.
    @details Gibt alle Medien aus der Datenbank zurück ohne neu zu scannen.
    @return Dict with list of media items / Dokument mit Medien-Liste.
    """
    return {"media": db.get_all_media()}


@eel.expose
def clear_database():
    """
    @brief Deletes all entries from the library database.
    @details Löscht alle Einträge aus der Bibliothek-Datenbank.
    @return Status dictionary / Status-Dictionary.
    """
    if DEBUG_FLAGS["db"]:
        debug_log("[Debug-DB] Tabelle wird geleert...")
    db.clear_media()
    return {"status": "ok", "message": "Datenbank geleert", "media": []}


@eel.expose
def reset_app_data():
    """
    @brief Wipes the database and configuration files (private user data).
    @details Löscht Datenbank und Konfigurationsdateien (Private Daten).
    @return Status dictionary with list of deleted paths / Status-Dictionary.
    """
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
    save_parser_config()  # Create default config
    load_parser_config()  # Sync local PARSER_CONFIG in memory

    if DEBUG_FLAGS["system"]:
        debug_log(f"[System] Reset complete. Deleted: {', '.join(deleted)}")
    return {"status": "ok", "deleted": deleted}


@eel.expose
def update_tags(name, tags_dict):
    """
    @brief Saves customized tags for a media item in the database.
    @details Speichert angepasste Tags für ein Item in der DB.
    @param name Media record name / Datenbank-Name des Eintrags.
    @param tags_dict Dictionary of tags to update / Zu aktualisierende Tags.
    @return Status dictionary / Status-Dictionary.
    """
    if DEBUG_FLAGS["db"] or DEBUG_FLAGS["metadata"]:
        logger.debug("metadata", f"Updating tags for {name}: {tags_dict}")
    db.update_media_tags(name, tags_dict)
    return {"status": "ok"}


@eel.expose
def rename_media(old_name, new_name):
    """
    @brief Renames a media record in the database.
    @details Benennt ein Medium in der DB um.
    @param old_name Current name / Aktueller Name.
    @param new_name Target name / Neuer Name.
    @return Status dictionary / Status-Dictionary.
    """
    if not new_name or new_name.strip() == "":
        return {"status": "error", "message": "Name darf nicht leer sein"}

    logger.debug("file_ops", f"Renaming record: {old_name} -> {new_name}")

    success = db.rename_media(old_name, new_name)
    if success:
        return {"status": "ok"}
    else:
        return {"status": "error", "message": "Name bereits vorhanden oder Fehler"}


@eel.expose
def delete_media(name):
    """
    @brief Deletes a media item from the database.
    @details Löscht ein Medium aus der DB.
    @param name Media record name / Datenbank-Name.
    """
    logger.debug("file_ops", f"Deleting record: {name}")
    return db.delete_media(name)


@eel.expose
def get_db_stats():
    """
    @brief Returns statistical information about the database content.
    @details Gibt Statistiken über den Inhalt der Datenbank zurück.
    @return Stats dictionary / Statistik-Dictionary.
    """
    return db.get_db_stats()


@eel.expose
def get_default_media_dir():
    """
    @brief Returns the default media directory (absolute path).
    @details Gibt den voreingestellten Medienordner (absoluter Pfad) zurück.
    @return Path string / Pfad-String.
    """
    return SCAN_MEDIA_DIR

# Funktion, um Medien zu scannen und an die GUI zu senden


@eel.expose
def ping():
    """
    @brief Connectivity check.
    @details Gibt eine Bestätigung zurück, dass das Backend erreichbar ist.
    @return dict with status 'ok' and message 'pong'.
    """
    return {"status": "ok", "message": "pong"}

def scan_media(dir_path: str | None = None, clear_db: bool = True):
    """
    @brief Scans a directory recursively and indexes audio files.
    @details Scannt rekursiv einen Ordner und indexiert Audiodateien. Optionaler Reset der DB.
    @param dir_path Optional path to scan / Optionaler Pfad zum Scannen.
    @param clear_db If True, clears the database before scanning / Falls True, leert die Datenbank vor dem Scan.
    @return Dictionary with media list and scan stats / Dictionary mit Medien-Liste und Statistiken.
    """
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

    count: int = 0
    for scan_root in scan_roots:
        logger.debug("scan", f"Starting scan of: {scan_root}")

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

                logger.debug("scan", f"Verarbeite: {f.name}")
                try:
                    item = MediaItem(f.name, f)
                    item_dict = item.to_dict()
                    logger.debug("db", f"{f.name} (Category: {item_dict.get('category')}) from {f.parent}")
                    db.insert_media(item_dict)
                    count += 1
                except Exception as e:
                    logger.debug("scan", f"Fehler bei {f.name}: {e}")
                    # Ignoriere problematische Dateien, aber setze das Logging fort
                    continue

    if hasattr(eel, 'set_db_status'):
        eel.set_db_status(False)()

    elapsed = time.time() - start_time
    logger.debug("performance", f"Scan of {scan_root or 'all'} took {elapsed:.2f} seconds.")
    logger.debug("scan", f"Scan complete. Processed {count} files in {elapsed:.2f} seconds.")

    # Status in GUI ausblenden (redundant, already handled by guard above)

    # Liefere gescannten Stand direkt aus der DB zurück
    return {
        "media": db.get_all_media(),
        "stats": {"count": count, "time_seconds": elapsed}
    }


@eel.expose
def get_parser_config():
    """
    @brief Returns the current parser configuration to the frontend.
    @details Gibt die aktuelle Parser-Konfiguration an das Frontend zurück.
    @return Configuration dictionary / Konfigurations-Dictionary.
    """
    return PARSER_CONFIG


@eel.expose
def update_parser_config(new_config):
    """
    @brief Updates the parser configuration and saves it to disk.
    @details Aktualisiert die Konfiguration und speichert sie auf Festplatte.
    @param new_config Dictionary with updated settings / Dictionary mit neuen Einstellungen.
    @return Status dictionary / Status-Dictionary.
    """
    PARSER_CONFIG.update(new_config)
    save_parser_config()
    return {"status": "ok"}


@eel.expose
def add_scan_dir():
    """
    @brief Opens a dialog to select a new directory for library scanning.
    @details Öffnet einen Dialog zur Auswahl eines neuen Scan-Verzeichnisses.
    @return Status dictionary with updated directory list / Status-Dictionary mit aktualisierter Liste.
    """
    new_dir = pick_folder()
    if new_dir:
        dirs = cast(list[str], PARSER_CONFIG.get("scan_dirs", []))
        if new_dir not in dirs:
            dirs.append(new_dir)
            PARSER_CONFIG["scan_dirs"] = dirs
            save_parser_config()
            return {"status": "ok", "dirs": dirs}
    return {"status": "cancel"}


@eel.expose
def remove_scan_dir(dir_path):
    """
    @brief Removes a directory from the scan list in the configuration.
    @details Entfernt ein Verzeichnis aus der Scan-Liste in der Konfiguration.
    @param dir_path Path to remove / Zu entfernender Pfad.
    @return Status dictionary / Status-Dictionary.
    """
    dirs = cast(list[str], PARSER_CONFIG.get("scan_dirs", []))
    if dir_path in dirs:
        dirs.remove(dir_path)
        PARSER_CONFIG["scan_dirs"] = dirs
        save_parser_config()
        return {"status": "ok", "dirs": dirs}
    return {"status": "error", "message": "Pfad nicht in Liste"}


@eel.expose
def play_media(path):
    """
    @brief Triggers media playback (handled client-side by the browser).
    @details Triggert die Medienwiedergabe (wird clientseitig vom Browser gehandhabt).
    @param path Media URL or path / Medien-URL oder Pfad.
    @return Confirmation dictionary / Bestätigungs-Dictionary.
    """
    if DEBUG_FLAGS["player"]:
        debug_log(f"[Debug-Player] Spiele ab: {path}")
    return {"status": "play", "path": path}  # Bestätigung


@eel.expose
def open_in_explorer(path_str):
    """
    @brief Opens a specific file or folder in the system's native file explorer.
    @details Öffnet eine Datei oder einen Ordner im nativen Datei-Explorer des Systems.
    @param path_str Absolute path / Absoluter Pfad.
    @return Status or error dictionary / Status- oder Fehler-Dictionary.
    """
    path_obj = Path(path_str)
    if not path_obj.exists():
        logging.warning("[FileExplorer] Path does not exist / Pfad existiert nicht")
        return {"error": "Nicht gefunden"}

    try:
        # Check OS and open accordingly
        if os.name == 'nt':  # Windows
            # Use getattr to satisfy mypy on non-Windows systems
            startfile = getattr(os, 'startfile', None)
            if startfile:
                startfile(path_str)
        elif sys.platform == 'darwin':  # macOS
            subprocess.run(['open', '-R', path_str])
        else:  # Linux (freedesktop)
            subprocess.run(['xdg-open', str(path_obj.parent)])
        return {"status": "ok"}
    except Exception as e:
        logging.error(f"[FileExplorer] Error opening path / Fehler beim Oeffnen: {e}")
        return {"error": str(e)}


@eel.expose
def browse_dir(dir_path=None):
    """
    @brief Lists folders and audio files for the in-app file browser.
    @details Listet Ordner und Audiodateien eines Verzeichnisses für den Datei-Browser.
    @param dir_path Directory path / Verzeichnispfad.
    @return Dictionary with path info and item list / Dictionary mit Pfad-Infos und Element-Liste.
    """
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
            elif entry.suffix.lower() in AUDIO_EXTENSIONS or entry.suffix.lower() in VIDEO_EXTENSIONS:
                size_mb = entry.stat().st_size / (1024 * 1024)
                item_type = "video" if entry.suffix.lower() in VIDEO_EXTENSIONS else "audio"
                items.append({"name": entry.name, "path": str(entry), "type": item_type, "size": f"{size_mb:.1f} MB"})
    except PermissionError:
        return {"error": "Keine Berechtigung", "path": dir_path}

    parent = str(target.parent) if target.parent != target else None
    return {"path": str(target), "parent": parent, "items": items}


@eel.expose
def pick_folder():
    """
    @brief Opens a native OS folder selection dialog using Tkinter.
    @details Öffnet einen nativen Ordner-Auswahldialog mittels Tkinter.
    @return Selected path or None / Gewählter Pfad oder None.
    """
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
        logging.error(f"[System] Folder picker failed: {e}")
        return None


@eel.expose
def add_file_to_library(file_path):
    """
    @brief Adds a single file from the browser to the library.
    @details Fügt eine einzelne Datei aus dem Datei-Browser der Bibliothek hinzu.
    @param file_path Absolute path / Absoluter Pfad.
    @return Status dictionary / Status-Dictionary.
    """
    p = Path(file_path)
    if not p.exists() or not p.is_file():
        return {"error": "Datei nicht gefunden"}
    if p.suffix.lower() not in AUDIO_EXTENSIONS and p.suffix.lower() not in VIDEO_EXTENSIONS:
        return {"error": "Kein unterstütztes Audio- oder Videoformat"}

    known = db.get_known_media_names()
    if p.name in known:
        return {"status": "exists", "name": p.name}

    item = MediaItem(p.name, p)
    item_dict = item.to_dict()
    db.insert_media(item_dict)
    return {"status": "added", "item": item_dict}

# VLC Player Instance (Global)
VLC_INSTANCE = None
VLC_PLAYER = None


@eel.expose
def play_vlc(file_path: str):
    """
    @brief Plays a media file in an external VLC window.
    @details Spielt eine Mediendatei in einem externen VLC-Fenster ab.
    """
    global VLC_INSTANCE, VLC_PLAYER
    if not HAS_VLC:
        return {"error": "python-vlc ist nicht installiert"}

    try:
        if VLC_INSTANCE is None:
            VLC_INSTANCE = vlc.Instance()
        
        if VLC_PLAYER is not None:
            VLC_PLAYER.stop()

        VLC_PLAYER = VLC_INSTANCE.media_player_new()
        media = VLC_INSTANCE.media_new(file_path)
        VLC_PLAYER.set_media(media)
        VLC_PLAYER.play()
        
        logger.get_ui_logger().info(f"VLC: Spiele {file_path}")
        return {"status": "ok"}
    except Exception as e:
        logger.get_ui_logger().error(f"VLC Fehler: {e}")
        return {"error": str(e)}


@eel.expose
def stop_vlc():
    """
    @brief Stops the VLC player.
    """
    global VLC_PLAYER
    if VLC_PLAYER:
        VLC_PLAYER.stop()
    return {"status": "ok"}


@eel.expose
def import_vlc_playlist(m3u_path: str):
    """
    @brief Imports a VLC playlist (m3u8/m3u/XSPF) into the library.
    @details Importiert eine VLC-Playlist (m3u8/m3u/XSPF) in die Bibliothek.
    @param m3u_path Path to the playlist file / Pfad zur Playlist-Datei.
    @return Dictionary with imported media items / Dictionary mit importierten Items.
    """
    if not HAS_M3U8:
        return {"error": "python-m3u8 Modul ist nicht installiert. Bitte installieren: pip install m3u8"}
    
    try:
        playlist_file = Path(m3u_path)
        if not playlist_file.exists():
            return {"error": "Playlist-Datei nicht gefunden"}
        
        # Load playlist
        playlist = m3u8.load(str(playlist_file))
        
        imported = []
        skipped = []
        errors = []
        
        for segment in playlist.segments:
            if not segment.uri:
                continue
                
            # Convert URI to absolute path if relative
            media_path = Path(segment.uri)
            if not media_path.is_absolute():
                media_path = playlist_file.parent / media_path
            
            if not media_path.exists():
                errors.append(f"Datei nicht gefunden: {media_path.name}")
                continue
            
            # Check if already in library
            known = db.get_known_media_names()
            if media_path.name in known:
                skipped.append(media_path.name)
                continue
            
            # Parse and add to library
            try:
                item = MediaItem(media_path.name, media_path)
                item_dict = item.to_dict()
                db.insert_media(item_dict)
                imported.append(item_dict)
            except Exception as e:
                errors.append(f"{media_path.name}: {str(e)}")
        
        if DEBUG_FLAGS["player"]:
            debug_log(f"[VLC Import] {len(imported)} importiert, {len(skipped)} übersprungen, {len(errors)} Fehler")
        
        return {
            "status": "ok",
            "imported": imported,
            "skipped": skipped,
            "errors": errors,
            "count": len(imported)
        }
    except Exception as e:
        logging.error(f"[VLC Import] Error: {e}")
        return {"error": str(e)}


@eel.expose
def export_playlist_to_vlc(media_names: list, output_path: str):
    """
    @brief Exports selected media items to a VLC-compatible m3u8 playlist.
    @details Exportiert ausgewählte Medien in eine VLC-kompatible m3u8 Playlist.
    @param media_names List of media item names from database / Liste von Medien-Namen aus der DB.
    @param output_path Target path for the .m3u8 file / Ziel-Pfad für die .m3u8-Datei.
    @return Status dictionary / Status-Dictionary.
    """
    try:
        playlist_file = Path(output_path)
        if not playlist_file.suffix:
            playlist_file = playlist_file.with_suffix('.m3u8')
        
        lines = ["#EXTM3U\n"]
        exported = 0
        missing = []
        
        # Get all media and create a lookup dict
        all_media = db.get_all_media()
        media_dict = {item['name']: item for item in all_media}
        
        for name in media_names:
            item_dict = media_dict.get(name)
            if not item_dict:
                missing.append(name)
                continue
            
            file_path = item_dict.get("path", "")
            if not file_path or not Path(file_path).exists():
                missing.append(name)
                continue
            
            # Add EXTINF metadata line (duration, title)
            duration = item_dict.get("duration", 0) or -1
            title = item_dict.get("title") or name
            artist = item_dict.get("artist", "")
            extinf_title = f"{artist} - {title}" if artist else title
            
            lines.append(f"#EXTINF:{duration},{extinf_title}\n")
            lines.append(f"{file_path}\n")
            exported += 1
        
        playlist_file.write_text("".join(lines), encoding='utf-8')
        
        if DEBUG_FLAGS["player"]:
            debug_log(f"[VLC Export] {exported} Tracks nach {playlist_file.name} exportiert")
        
        return {
            "status": "ok",
            "path": str(playlist_file),
            "exported": exported,
            "missing": missing
        }
    except Exception as e:
        logging.error(f"[VLC Export] Error: {e}")
        return {"error": str(e)}


@eel.expose
def pick_file(title="Datei auswählen", filetypes=None):
    """
    @brief Opens a native file picker dialog.
    @details Öffnet einen nativen Datei-Auswahldialog.
    @param title Dialog title / Dialog-Titel.
    @param filetypes List of (description, extension) tuples / Liste von Dateifiltern.
    @return Selected file path or None / Gewählter Pfad oder None.
    """
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        
        if filetypes:
            file_path = filedialog.askopenfilename(title=title, filetypes=filetypes)
        else:
            file_path = filedialog.askopenfilename(title=title)
        
        root.destroy()
        return file_path if file_path else None
    except Exception as e:
        logging.error(f"[System] File picker failed: {e}")
        return None


@eel.expose
def pick_save_file(title="Datei speichern", filetypes=None, default_name="playlist.m3u8"):
    """
    @brief Opens a native file save dialog.
    @details Öffnet einen nativen Datei-Speichern-Dialog.
    @param title Dialog title / Dialog-Titel.
    @param filetypes List of (description, extension) tuples / Liste von Dateifiltern.
    @param default_name Default filename / Standard-Dateiname.
    @return Selected file path or None / Gewählter Pfad oder None.
    """
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.wm_attributes('-topmost', 1)
        
        if filetypes:
            file_path = filedialog.asksaveasfilename(
                title=title, 
                filetypes=filetypes,
                defaultextension=".m3u8",
                initialfile=default_name
            )
        else:
            file_path = filedialog.asksaveasfilename(
                title=title,
                initialfile=default_name
            )
        
        root.destroy()
        return file_path if file_path else None
    except Exception as e:
        logging.error(f"[System] File save picker failed: {e}")
        return None


@eel.expose
def pick_folder_cli(prompt="Ordnerpfad eingeben"):
    """
    @brief CLI-based folder picker without GUI dependencies.
    @details CLI-basierter Ordner-Picker ohne GUI-Abhängigkeiten (nur Bordmittel).
    @param prompt Input prompt text / Eingabe-Prompt-Text.
    @return Valid folder path or None / Gültiger Ordnerpfad oder None.
    """
    try:
        print(f"\n{prompt}:")
        print(f"(Standard: {Path.home()})")
        user_input = input("> ").strip()
        
        if not user_input:
            return str(Path.home())
        
        folder_path = Path(user_input).expanduser().resolve()
        
        if folder_path.exists() and folder_path.is_dir():
            return str(folder_path)
        else:
            print(f"Fehler: '{folder_path}' ist kein gültiger Ordner.")
            return None
    except (KeyboardInterrupt, EOFError):
        print("\nAbgebrochen.")
        return None
    except Exception as e:
        logging.error(f"[System] CLI folder picker failed: {e}")
        return None


@eel.expose
def pick_file_cli(prompt="Dateipfad eingeben", extensions=None):
    """
    @brief CLI-based file picker without GUI dependencies.
    @details CLI-basierter Datei-Picker ohne GUI-Abhängigkeiten (nur Bordmittel).
    @param prompt Input prompt text / Eingabe-Prompt-Text.
    @param extensions Optional list of allowed extensions / Optionale Liste erlaubter Endungen.
    @return Valid file path or None / Gültiger Dateipfad oder None.
    """
    try:
        ext_info = ""
        if extensions:
            ext_info = f" (Erlaubte Formate: {', '.join(extensions)})"
        
        print(f"\n{prompt}{ext_info}:")
        user_input = input("> ").strip()
        
        if not user_input:
            return None
        
        file_path = Path(user_input).expanduser().resolve()
        
        if not file_path.exists():
            print(f"Fehler: Datei '{file_path}' nicht gefunden.")
            return None
        
        if not file_path.is_file():
            print(f"Fehler: '{file_path}' ist keine Datei.")
            return None
        
        if extensions and file_path.suffix.lower() not in extensions:
            print(f"Fehler: Dateiformat '{file_path.suffix}' nicht erlaubt.")
            return None
        
        return str(file_path)
    except (KeyboardInterrupt, EOFError):
        print("\nAbgebrochen.")
        return None
    except Exception as e:
        logging.error(f"[System] CLI file picker failed: {e}")
        return None


@eel.expose
def pick_save_file_cli(prompt="Speicherpfad eingeben", default_name="output.txt", extensions=None):
    """
    @brief CLI-based save file dialog without GUI dependencies.
    @details CLI-basierter Speichern-Dialog ohne GUI-Abhängigkeiten (nur Bordmittel).
    @param prompt Input prompt text / Eingabe-Prompt-Text.
    @param default_name Default filename / Standard-Dateiname.
    @param extensions Optional list of allowed extensions / Optionale Liste erlaubter Endungen.
    @return Valid save path or None / Gültiger Speicherpfad oder None.
    """
    try:
        ext_info = ""
        if extensions:
            ext_info = f" (Formate: {', '.join(extensions)})"
        
        print(f"\n{prompt}{ext_info}:")
        print(f"(Standard: {default_name})")
        user_input = input("> ").strip()
        
        if not user_input:
            user_input = default_name
        
        save_path = Path(user_input).expanduser().resolve()
        
        # Add extension if missing
        if extensions and save_path.suffix.lower() not in extensions:
            save_path = save_path.with_suffix(extensions[0])
        
        # Check if parent directory exists
        if not save_path.parent.exists():
            print(f"Fehler: Verzeichnis '{save_path.parent}' existiert nicht.")
            create = input("Verzeichnis erstellen? (j/n): ").strip().lower()
            if create == 'j':
                save_path.parent.mkdir(parents=True, exist_ok=True)
            else:
                return None
        
        # Warn if file exists
        if save_path.exists():
            overwrite = input(f"Datei '{save_path.name}' existiert. Überschreiben? (j/n): ").strip().lower()
            if overwrite != 'j':
                return None
        
        return str(save_path)
    except (KeyboardInterrupt, EOFError):
        print("\nAbgebrochen.")
        return None
    except Exception as e:
        logging.error(f"[System] CLI save file picker failed: {e}")
        return None


@eel.expose
def get_test_suites():
    """
    @brief Discovers all test files in the tests/ directory and extracts metadata.
    @details Findet alle Testdateien im Verzeichnis tests/ und extrahiert deren Metadaten.
    @return List of test suite objects / Liste von Test-Suite-Objekten.
    """
    test_dir = Path(__file__).parent / "tests"
    if not test_dir.exists():
        return []

    suites = []
    for f in sorted(test_dir.glob("*.py")):
        if f.name.startswith("__"):
            continue
        # Include all .py files in tests/ as they might be utility scripts the user wants
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
            if line.startswith("# Kategorie:"):
                metadata["category"] = line.split(":", 1)[1].strip()
            elif line.startswith("# Eingabewerte:"):
                metadata["inputs"] = line.split(":", 1)[1].strip()
            elif line.startswith("# Ausgabewerte:"):
                metadata["outputs"] = line.split(":", 1)[1].strip()
            elif line.startswith("# Testdateien:"):
                metadata["files"] = line.split(":", 1)[1].strip()
            elif line.startswith("# Kommentar:"):
                metadata["comment"] = line.split(":", 1)[1].strip()

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
    """
    @brief Updates the metadata comments in a specific test file.
    @details Aktualisiert die Metadaten-Kommentare in einer bestimmten Testdatei.
    @param filename Name of the test file / Name der Testdatei.
    @param metadata Dictionary of metadata fields / Dictionary der Metadaten-Felder.
    @return Status or error dictionary / Status- oder Fehler-Dictionary.
    """
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
    """
    @brief Creates a new test file based on a template.
    @details Erstellt eine neue Testdatei basierend auf einem Template.
    @param name Base name for the test / Basisname des Tests.
    @return Status or filename dictionary / Status- oder Dateinamen-Dictionary.
    """
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
    """
    @brief Deletes a specific test file from the disk.
    @details Löscht eine bestimmte Testdatei von der Festplatte.
    @param filename Test file name / Name der Testdatei.
    @return Status or error dictionary / Status- oder Fehler-Dictionary.
    """
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
    """
    @brief Reads a markdown file from the logbook or the README.
    @details Liest eine Markdown-Datei aus dem Logbuch oder die README ein.
    @param feature_name Entry name or 'README' / Name des Eintrags oder 'README'.
    @return Content string (Markdown) / Inhalts-String (Markdown).
    """
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
    """
    @brief Returns a list of all markdown files in the logbook folder with metadata.
    @details Gibt eine Liste aller Markdown-Dateien im logbuch/ Ordner mit Metadaten zurück.
    @return List of logbook entry objects / Liste von Logbuch-Eintrag-Objekten.
    """
    log_dir = Path(__file__).parent / "logbuch"
    if not log_dir.exists():
        return []

    entries = []
    # Natural sort by filename
    for f in sorted(log_dir.glob("*.md")):
        try:
            with open(f, 'r', encoding='utf-8') as fp:
                lines = [fp.readline() for _ in range(20)]  # Mehr Zeilen lesen um alles zu finden
                category = "Sonstiges"
                summary = ""
                status = "COMPLETED"  # Default
                title = f.stem

                title_de = ""
                title_en = ""
                summary_de = ""
                summary_en = ""

                for line in lines:
                    line = line.strip()
                    # Support both <!-- Tag: Value --> and Tag: Value formats
                    content = line
                    if "<!--" in line and "-->" in line:
                        content = line.split("<!--")[1].split("-->")[0].strip()

                    if ":" in content:
                        key, val = content.split(":", 1)
                        key = key.strip()
                        val = val.strip()

                        if key == "Category":
                            category = val
                        elif key == "Status":
                            status = val
                        elif key == "Title_DE":
                            title_de = val
                        elif key == "Title_EN":
                            title_en = val
                        elif key == "Summary_DE":
                            summary_de = val
                        elif key == "Summary_EN":
                            summary_en = val
                        elif key == "Summary":
                            summary = val

                    if line.startswith("# "):
                        title = line.replace("# ", "").strip()

                # Special case for Known Issues
                if f.name == "00_Known_Issues.md":
                    category = "Bug"

                # Fallbacks
                if not title_de:
                    title_de = title
                if not title_en:
                    title_en = title

                # Bi-directional summary fallback
                if not summary:
                    summary = summary_de or summary_en
                if not summary_de:
                    summary_de = summary
                if not summary_en:
                    summary_en = summary

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
    """
    @brief Saves or updates a logbook entry file.
    @details Speichert oder aktualisiert einen Logbuch-Eintrag.
    @param filename Target filename / Ziel-Dateiname.
    @param content Markdown content / Markdown-Inhalt.
    @return Status or error dictionary / Status- oder Fehler-Dictionary.
    """
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
    """
    @brief Deletes a logbook entry from the disk.
    @details Löscht einen Logbuch-Eintrag.
    @param filename Entry filename / Dateiname des Eintrags.
    @return Status or error dictionary / Status- oder Fehler-Dictionary.
    """
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
    """
    @brief Executes selected pytest suites and returns the results.
    @details Führt ausgewählte pytest-Suiten aus und gibt die Ergebnisse zurück.
    @param test_files List of test filenames / Liste von Test-Dateinamen.
    @return Result dictionary with passes/fails and output / Ergebnis-Dictionary.
    """
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
    """
    @brief Placeholder for GUI tests (handled via the agent).
    @details Dummy-Funktion für GUI-Tests (da diese über den Agenten laufen).
    @return Info dictionary / Info-Dictionary.
    """
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
    # Append to log silently so it's visible in the debug window later
    debug_log(startup_cmd)
    if any(DEBUG_FLAGS.values()):
        debug_log(startup_cmd)

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
    logger.debug("websocket", f"Eel initialized with root: {web_dir}")

    if DEBUG_FLAGS["start"]:
        debug_log("[Startup] Starting Eel UI...")
    
    # Find a free port dynamically to allow multiple sessions
    import socket
    def find_free_port():
        """Find and return a free port for this session."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('', 0))
            s.listen(1)
            port = s.getsockname()[1]
        return port
    
    def get_preferred_browser():
        """
        Get the preferred browser controller for launching the application.
        
        Preference order:
        1. Google Chrome
        2. Chromium
        3. Firefox
        4. Default system browser
        
        Returns:
            webbrowser.BaseBrowser: Browser controller instance
        """
        import webbrowser
        import shutil
        
        # Priority list of browsers
        browser_candidates = [
            ('google-chrome', 'Google Chrome'),
            ('chromium-browser', 'Chromium'),
            ('chromium', 'Chromium'),
            ('firefox', 'Firefox'),
        ]
        
        for browser_cmd, browser_name in browser_candidates:
            browser_path = shutil.which(browser_cmd)
            if browser_path:
                logging.info(f"[Browser] Selected: {browser_name} ({browser_path})")
                try:
                    # Register and get browser controller
                    browser_controller = webbrowser.get(f'{browser_path} %s')
                    return browser_controller
                except Exception as e:
                    logging.warning(f"[Browser] Failed to register {browser_name}: {e}")
                    continue
        
        # Fallback to default browser
        logging.warning("[Browser] Using system default browser (Vivaldi or other)")
        return webbrowser
    
    session_port = find_free_port()
    
    # Block=False verhindert, dass eel.start() den Server sofort beendet (sys.exit),
    # wenn Chrome den neuen Tab an einen bestehenden Prozess delegiert und sich sofort schließt.
    try:
        logger.debug("websocket", f"Starting Eel server session on port {session_port}...")
        eel.start("app.html", mode=None, size=(1450, 800), block=False, port=session_port)
        
        # Open browser explicitly after Eel starts with session-specific URL
        session_url = f"http://localhost:{session_port}/app.html"
        logging.info(f"[Session] Opening browser at {session_url}")
        
        # Use preferred browser (Chrome/Chromium over Vivaldi)
        browser = get_preferred_browser()
        browser.open(session_url)
        
    except Exception as e:
        logging.error(f"[Startup-Error] Failed to start session: {e}")

    # Server am Leben halten
    while True:
        eel.sleep(1.0)
