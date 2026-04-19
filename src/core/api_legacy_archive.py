"""
Forensic Legacy Archive (v1.54.022)
This module contains functions that were removed from main.py during the Core Slimming phase.
Functions are preserved here to ensure no logic is lost and for potential legacy support.

UNUSED FUNCTIONS (SUPERSEDED OR REDUNDANT):
- add_file_to_library
- add_scan_dir
- api_ping
- delete_media
- get_active_video_workers
- get_api_forensics
- get_app_mode
- get_environment_forensics
- get_footer_registry
- get_gevent_status
- get_global_health_audit
- get_hardware_forensics
- get_hydration_stats
- get_language
- get_net_ping
- get_parser_mode
- get_process_forensics
- get_security_forensics
- get_start_page
- get_startup_config
- get_state_forensics
- get_sys_overview
- get_system_environment
- get_ui_settings
- get_venv_summary
- heartbeat
- kill_stale_and_restart
- log_gui_event
- log_js_error
- log_spawn_event
- nuclear_restart
- pip_install_packages
- remove_scan_dir
- rename_media
- report_items_spawned
- report_playback_state
- report_spawn
- reset_config
- rtt_ping
- run_direct_scan
- run_video_transcode_diagnostic
- scan_media
- set_app_mode
- set_footer_element_state
- set_language
- set_log_level
- set_parser_mode
- set_start_page
- set_ui_setting
- shutdown_backend
- sync_library_atomic
- terminate_worker_process
- trigger_db_reconnect
- trigger_factory_reset
- update_startup_config
- update_tags

RESTORED FUNCTIONS (LEGACY ARCHIVE):
- _detect_python_environment
- _get_requirements_status
- _parse_nfo_file
- _scan_media_execution
- confirm_receipt
- find_venv_pid
- get_category_master
- get_global_config
- get_mock_data_enabled
- get_playlist_forensics
- get_tech_markers
- prune_playlist_orphans
- rtt_item_test
- rtt_stress_ping
- run_debug_test
- sanitize_json_utf8
- set_hydration_mode
- set_mock_data_enabled
- set_ui_config_value
- update_browse_dir
- update_library_dir
"""

import os, sys, json, time, sqlite3, subprocess, platform
from pathlib import Path
try:
    from src.core.eel_shell import eel
except ImportError:
    import eel


# --- [_detect_python_environment] ---
@eel.expose
def _detect_python_environment():
    """
    Detect current Python environment: system, venv, or conda.
    Returns tuple: (env_type, env_name, env_path, python_version, python_executable)
    """
    python_version = platform.python_version()
    python_executable = sys.executable

    # Check for venv
    in_venv = sys.prefix != sys.base_prefix
    venv_env = os.environ.get('VIRTUAL_ENV')

    if in_venv or venv_env:
        env_path = venv_env or sys.prefix
        env_name = Path(env_path).name if env_path else 'venv'
        return ('venv', env_name, env_path, python_version, python_executable)

    # Check for conda
    conda_env = os.environ.get('CONDA_DEFAULT_ENV')
    conda_prefix = os.environ.get('CONDA_PREFIX')

    if conda_env and conda_prefix:
        return (
            'conda',
            conda_env,
            conda_prefix,
            python_version,
            python_executable)

    # System Python
    return ('system', None, sys.prefix, python_version, python_executable)



# --- [_get_requirements_status] ---
@eel.expose
def _get_requirements_status():
    """Get install status for requirements.txt packages in current interpreter."""
    import importlib.util

    # Check multiple locations for requirements
    req_locations = [
        PROJECT_ROOT / "requirements.txt",
        PROJECT_ROOT / "infra" / "requirements-build.txt",
        PROJECT_ROOT / "infra" / "requirements-core.txt",
        PROJECT_ROOT / "infra" / "requirements-testbed.txt",
        PROJECT_ROOT / "infra" / "requirements-selenium.txt",
        PROJECT_ROOT / "infra" / "requirements-run.txt",
        PROJECT_ROOT / "infra" / "requirements-dev.txt",
        PROJECT_ROOT / "infra" / "requirements.txt",     # venv
    ]

    requirements_file = None
    for loc in req_locations:
        if loc.exists():
            requirements_file = loc
            # If it's a main redirect/entry, use it and stop.
            if loc.name == "requirements.txt" or loc.name == "requirements-run.txt":
                break

    if not requirements_file:
        return {
            "available": False,
            "total": 0,
            "installed_count": 0,
            "missing_count": 0,
            "installed": [],
            "missing": [],
            "source": "None"
        }

    status = {
        "available": True,
        "total": 0,
        "installed_count": 0,
        "missing_count": 0,
        "installed": [],
        "missing": [],
        "source": "requirements.txt"
    }

    import_overrides = {
        "python-vlc": "vlc",  # overirdes anschauen
        "bottle-websocket": "bottle_websocket",
        "gevent-websocket": "geventwebsocket",
        "pytest-cov": "pytest_cov",
        "pyinstaller": "PyInstaller",
        "pillow": "PIL",
        "markdown": "markdown",
        "scapy": "scapy",
        "future": "future",
        "chardet": "chardet",
        "pyscreeze": "pyscreeze",
        "pyautogui": "pyautogui",
    }

    requirement_names = set()

    def parse_requirements(file_path, seen=None):
        if seen is None:
            seen = set()
        # Normalize path for seen set
        try:
            abs_path = file_path.resolve()
        except BaseException:
            return
        if str(abs_path) in seen:
            return
        seen.add(str(abs_path))

        try:
            for raw_line in file_path.read_text(encoding="utf-8").splitlines():
                line = raw_line.strip()
                if not line or line.startswith("#"):
                    continue

                # Handle recursive requirements (-r)
                if line.startswith("-r"):
                    ref_name = line[2:].strip()
                    ref_path = file_path.parent / ref_name
                    if ref_path.exists():
                        parse_requirements(ref_path, seen)
                    continue

                # Handle other pip flags we don't care about for existence check
                if line.startswith("-"):
                    continue

                line = line.split(" #", 1)[0].split(";", 1)[0].strip()
                if not line:
                    continue

                if " @ " in line:
                    package_name = line.split(" @ ", 1)[0].strip()
                else:
                    # Capture everything before the first version specifier
                    package_name = re.split(
                        r"(==|>=|<=|~=|!=|>|<|\[)", line, maxsplit=1)[0].strip()

                if package_name:
                    requirement_names.add(package_name)
        except Exception as e:
            log.error(f"Error parsing {file_path}: {e}")

    parse_requirements(requirements_file)

    # If the main requirement file was just a redirect, show the final target
    if requirements_file and status["source"] == "requirements.txt" and requirements_file.name != "requirements.txt":
        status["source"] = f"requirements.txt -> {requirements_file.name}"

    # If we followed a chain, show the last one that actually had content
    if requirements_file:
        status["source"] = str(requirements_file.relative_to(PROJECT_ROOT))

    installed = []
    missing = []
    for package_name in requirement_names:
        import_name = import_overrides.get(
            package_name.lower(), package_name.replace("-", "_"))
        if not import_name:
            missing.append(package_name)
            continue
        try:
            if importlib.util.find_spec(import_name) is not None:
                installed.append(package_name)
            else:
                missing.append(package_name)
        except Exception:
            missing.append(package_name)

    installed.sort(key=str.lower)
    missing.sort(key=str.lower)

    status["installed"] = installed
    status["missing"] = missing
    status["total"] = len(requirement_names)
    status["installed_count"] = len(installed)
    status["missing_count"] = len(missing)
    return status



# --- [_parse_nfo_file] ---
@eel.expose
def _parse_nfo_file(nfo_path: Path) -> dict:
    """
    Parses a Kodi/Plex style .nfo XML file (Centralized v1.46.131).
    """
    metadata = {}
    nfo_cfg = GLOBAL_CONFIG.get("nfo_settings", {})
    if not nfo_cfg.get("enable_parsing", True):
        return {}

    try:
        import xml.etree.ElementTree as ET
        if not nfo_path.exists(): return {}
        
        # Use centralized encoding if provided (default utf-8)
        encoding = nfo_cfg.get("encoding", "utf-8")
        with nfo_path.open("r", encoding=encoding, errors="replace") as f:
            content = f.read()
            # Basic sanity check for XML
            if not content.strip().startswith("<"):
                return {}
            
            # Reset pointer or parse from string
            root = ET.fromstring(content)
        
        # Mapping: XML Tag -> Metadata Key (Centralized)
        mappings = nfo_cfg.get("mapping", {
            'title': 'title', 'year': 'year', 'genre': 'genre',
            'artist': 'artist', 'album': 'album', 'plot': 'plot'
        })
        
        for xml_tag, meta_key in mappings.items():
            el = root.find(xml_tag)
            if el is not None and el.text:
                metadata[meta_key] = el.text.strip()
                
        # Handle multiple genres (Kodi standard)
        genres = [g.text for g in root.findall('genre') if g.text]
        if genres: 
            metadata['genre'] = ", ".join(genres)
            
    except Exception as e:
        # Respect the global compact logging flag
        exc = None if GLOBAL_CONFIG["logging_registry"].get("log_compact_errors_only", True) else True
        log.error(f"[NFO-Parser-Error] Failed to parse {nfo_path.name}: {e}", exc_info=exc)
        
    return metadata



# --- [_scan_media_execution] ---
@eel.expose
def _scan_media_execution(dir_path: str | None = None, clear_db: bool = True):
    """
    @brief Performs the actual media scan (Refactored for Round 5.5 Performance).
    """
    start_time = time.time()
    count_indexed = 0
    total_traversed = 0

    # 0. Round 5.6 - Emergency DB Purge (v1.35.98)
    if clear_db:
        log.warning("[DB-SCAN] Round 5.6: Emergency DB Purge triggered. Clearing existing items.")
        db.clear_media()
        # [DIAGNOSTIC] Ensure existing_media is reset
        existing_media = set()
    else:
        existing_media = {str(Path(m['path']).resolve()) for m in db.get_all_media_items() if m.get('path')}

    # 1. Imports (Round 5.5: Avoid Scoping Issues)
    from src.parsers.format_utils import (
        AUDIO_EXTENSIONS, VIDEO_EXTENSIONS, PICTURE_EXTENSIONS,
        DOCUMENT_EXTENSIONS, EBOOK_EXTENSIONS, DISK_IMAGE_EXTENSIONS,
        DSD_EXTENSIONS, HDDVD_EXTENSIONS, PARSER_CONFIG, get_default_scan_dir
    )

    # 4. Prepare Extension Filter & Fast-Category-Mapper (v1.35.98)
    from src.core.models import MASTER_CAT_MAP
    ext_to_cat = {}
    for cat, info in MASTER_CAT_MAP.items():
        for ext in info.get("extensions", []):
            ext_to_cat[ext.lower()] = cat

    all_exts = set(ext_to_cat.keys())
    
    # [v1.45.130] Toggles
    enable_collections = GLOBAL_CONFIG.get("enable_collection_management", True)
    enable_nfo = GLOBAL_CONFIG.get("enable_nfo_parsing", True)

    # 2. Fast-Scan Override
    parser_mode = 'lightweight'
    GLOBAL_CONFIG["parser_mode"] = 'lightweight'

    # MUTE ARTWORK (The True 10-minute Stall Source)
    orig_art_cfg = PARSER_CONFIG.get('ffmpeg_extract_thumbnails', True)
    PARSER_CONFIG['ffmpeg_extract_thumbnails'] = False

    log.info(f"[DB-SCAN] EMERGENCY Round 5.5 (v1.35.98): Mode={parser_mode} & Muting Thumbnails.")

    # 3. Path Resolution
    scan_roots = [Path(dir_path).resolve()] if dir_path else []
    if not scan_roots:
        config_dirs = PARSER_CONFIG.get("scan_dirs", [])
        for d in config_dirs:
            p = Path(d).resolve()
            if p.exists():
                scan_roots.append(p)

    # Default fallback
    if not scan_roots:
        scan_roots = [get_default_scan_dir()]

    # Path Resolution logic...
    # (Already handled by 0. Round 5.6)

    # 4. Prepare Extension Filter
    indexed_cats = PARSER_CONFIG.get("indexed_categories", [])

    # 5. Batch Collection
    collected_items = []

    try:
        scan_settings = GLOBAL_CONFIG.get("scan_settings", {})
        max_files = scan_settings.get("max_files", 50000)
        max_depth = scan_settings.get("max_depth", 12)
        enable_ext_skip = scan_settings.get("enable_extension_skipping", True)
        skip_exts = set(scan_settings.get("skip_extensions", [".txt", ".log", ".tmp"]))
        enable_size_skip = scan_settings.get("enable_size_skipping", True)
        min_size = scan_settings.get("min_size_kb", 1) * 1024
        max_size = scan_settings.get("max_size_mb", 50000) * 1024 * 1024
        batch_size = scan_settings.get("batch_commit_size", 250)
        log_compact = scan_settings.get("log_compact_errors_only", True)
        log_unsupported = scan_settings.get("log_unsupported_extensions", False)

        for scan_root in scan_roots:
            log.info(f" [Scan] Starting scan of: {scan_root}")
            for root, dirs, files in os.walk(str(scan_root), followlinks=False):
                total_traversed += (len(files) + len(dirs))
                if total_traversed > max_files:
                    log.warning(f"[DB-SCAN] Safety Cap Triggered ({max_files} items). Stopping traversal.")
                    dirs[:] = []  # Stop os.walk from recursing further
                    break

                d = Path(root)
                # Depth Check (Centralized)
                try:
                    rel_path = d.relative_to(scan_root)
                    if len(rel_path.parts) > max_depth:
                        dirs[:] = []  # Stop recursion
                        continue
                except Exception as e:
                    exc = None if log_compact else True
                    log.error(f"[Scan-Depth-Error] Failed depth calculation for {d}: {e}", exc_info=exc)
                    continue

                # 2. Folders as Media (Albums/DVDs) - v1.45.130
                if d != scan_root and enable_collections:
                    media_files = [f for f in files if f.lower().endswith(tuple(all_exts))]
                    m_count = len(media_files)
                    
                    if m_count > 0:
                        # 1. Detect NFO & Coverage
                        nfo_file = next((f for f in files if f.lower().endswith('.nfo')), None)
                        nfo_data = _parse_nfo_file(d / nfo_file) if (nfo_file and enable_nfo) else {}
                        
                        # 2. Determine Collection Category
                        is_audio = any(f.lower().endswith(tuple(AUDIO_EXTENSIONS)) for f in media_files)
                        cat = 'audio' if is_audio else 'video'
                        
                        # Forensic Categorization Logic (v1.45.130-EXT)
                        folder_name = d.name.lower()
                        genre = nfo_data.get('genre', '').lower()
                        artist = nfo_data.get('artist', '').lower()
                        
                        # Optical Media Check (v1.45.130)
                        has_dvd = 'video_ts' in [sd.lower() for sd in dirs]
                        has_bd = 'bdmv' in [sd.lower() for sd in dirs]
                        
                        if has_dvd or has_bd: cat = 'video_iso'
                        elif 'klassik' in genre or 'classical' in genre or 'klassik' in folder_name: cat = 'klassik'
                        elif 'soundtrack' in genre or 'ost' in genre or 'ost' in folder_name: cat = 'soundtrack'
                        elif 'podcast' in genre or 'podcast' in folder_name: cat = 'podcast'
                        elif 'hörbuch' in genre or 'audiobook' in genre or 'hörbuch' in folder_name: cat = 'hörbuch'
                        elif ('mix' in folder_name or 'mixtape' in folder_name) and any(va in artist for va in ['va', 'varios', 'various artists']): cat = 'mix'
                        elif any(va in artist for va in ['va', 'varios', 'various artists']): cat = 'compilation'
                        elif m_count > 1 and is_audio: cat = 'album'
                        elif m_count > 1 and not is_audio: cat = 'series'
                        elif 'doku' in folder_name or 'dokumentation' in folder_name: cat = 'documentation'
                        
                        collected_items.append({
                            'name': f"[FOLDER] {d.name}", 'path': str(d), 'category': cat,
                            'is_mock': 0, 'mock_stage': 0, 'full_tags': nfo_data, 'chapters': [],
                            'type': 'folder', 'media_type': cat, 'nfo_parsed': 1 if nfo_data else 0
                        })
                        count_indexed += 1
                        
                        # Atomic Batch Commit (v1.46.102)
                        if len(collected_items) >= batch_size:
                            log.info(f"[DB-SCAN] Batch Commit (Folder): {len(collected_items)} items...")
                            db.insert_media_batch(collected_items)
                            collected_items = []

                # 3. Individual Files (Standard Pass)
                for filename in files:
                    ext = "." + filename.rsplit('.', 1)[-1].lower() if '.' in filename else ""
                    
                    if enable_ext_skip and ext in skip_exts:
                        log.debug(f"[Scan-Trace] SKIPPING (Blacklisted Ext '{ext}'): {filename}")
                        continue
                        
                    if ext not in all_exts:
                        if log_unsupported:
                            log.debug(f"[Scan-Trace] SKIPPING (Unsupported Ext '{ext}'): {filename}")
                        continue
                        
                    f_path = os.path.join(root, filename)
                    if f_path in existing_media:
                        log.debug(f"[Scan-Trace] SKIPPING (Already Indexed): {filename}")
                        continue

                    if enable_size_skip:
                        try:
                            f_size = os.path.getsize(f_path)
                            if f_size < min_size:
                                log.debug(f"[Scan-Trace] SKIPPING (Ghost File < {min_size}B): {filename}")
                                continue
                            if f_size > max_size:
                                log.debug(f"[Scan-Trace] SKIPPING (Oversize File > {max_size}B): {filename}")
                                continue
                        except Exception as e:
                            log.warning(f"[Scan-Size-Error] Skip due to unreadable file size for {filename}: {e}")
                            continue

                    try:
                        cat = ext_to_cat.get(ext, 'Unknown')
                        log.debug(f"[Scan-Trace] INDEXING: {filename} -> {cat}")
                        collected_items.append({
                            'name': filename, 'path': f_path, 'category': cat,
                            'is_mock': 0, 'mock_stage': 0, 'full_tags': {}, 'chapters': [],
                            'type': 'file', 'file_type': ext[1:].upper(),
                            'extension': ext
                        })
                        count_indexed += 1
                    except Exception as e:
                        exc = None if log_compact else True
                        log.error(f"[Scan-Index-Error] Fatal crash indexing '{filename}': {e}", exc_info=exc)

                    # 4. Atomic Batch Commit (v1.46.102)
                    if len(collected_items) >= batch_size:
                        log.info(f"[DB-SCAN] Batch Commit: {len(collected_items)} items...")
                        db.insert_media_batch(collected_items)
                        collected_items = []

        # 6. Final Sync
        if collected_items:
            log.info(f"[DB-SCAN] Finalizing batch of {len(collected_items)} items...")
            db.insert_media_batch(collected_items)

        # --- [v1.54.001] OBJECT-CENTRIC GROUPING PHASE ---
        log.info("[DB-SCAN] Starting Object-Centric Grouping Phase (v1.54)...")
        all_items = db.get_all_media_items()
        engine = ObjectDiscoveryEngine()
        discovered_objects = engine.discover_groups(all_items)
        
        objects_inserted = 0
        for obj in discovered_objects:
            # 1. Insert the parent object record
            parent_id = db.insert_media_object(obj.to_dict())
            if parent_id:
                objects_inserted += 1
                # 2. Link all child items to the new parent
                for item_id in obj.items:
                    db.set_item_parent(item_id, parent_id)
                # 3. Link sidecars (using path as lookup)
                for sidecar_path in obj.sidecars.values():
                    sidecar_item = next((it for it in all_items if it['path'] == sidecar_path), None)
                    if sidecar_item:
                        db.set_item_parent(sidecar_item['id'], parent_id)

        log.info(f"[DB-SCAN] Object Grouping Complete. Created {objects_inserted} high-density objects.")

        # 10. Round 5.6 - Final Sync & Availability Check (v1.35.98)
        if not clear_db:
            log.info("[DB-SCAN] Running availability check for incremental sync...")
            total, missing = db.check_media_availability()
            log.info(f"[DB-SCAN] Availability check done. Total: {total} | Missing/Renamed: {missing}")

        return {"status": "ok", "count": count_indexed, "time_seconds": time.time() - start_time}

    except Exception as e:
        log.error(f"[Scan-Trace] CRITICAL FAILURE: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        # Restore artwork setting
        PARSER_CONFIG['ffmpeg_extract_thumbnails'] = orig_art_cfg
        # Silent Status Update
        websockets = getattr(eel, '_websockets', [])
        if len(websockets) > 0 and hasattr(eel, 'set_db_status'):
            try:
                eel.set_db_status("Ready")
            except Exception:
                pass



# --- [add_file_to_library] ---
def add_file_to_library(file_path):
    """
    @brief Adds a single file from the browser to the library.
    @details Fgt eine einzelne Datei aus dem Datei-Browser der Bibliothek hinzu.
    @param file_path Absolute path / Absoluter Pfad.
    @return Status dictionary / Status-Dictionary.
    """
    p = Path(file_path)
    if not p.exists() or not p.is_file():
        return {"error": "Datei nicht gefunden"}
    if p.suffix.lower() not in AUDIO_EXTENSIONS and p.suffix.lower() not in VIDEO_EXTENSIONS:
        return {"error": "Kein untersttztes Audio- oder Videoformat"}

    known = db.get_known_media_names()
    if p.name in known:
        return {"status": "exists", "name": p.name}

    item = MediaItem(p.name, p)
    item_dict = item.to_dict()
    db.insert_media(item_dict)
    return {"status": "added", "item": item_dict}



# --- [add_scan_dir] ---
def add_scan_dir():
    """
    @brief Opens a dialog to select a new directory for library scanning.
    @details ffnet einen Dialog zur Auswahl eines neuen Scan-Verzeichnisses.
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



# --- [api_ping] ---
def api_ping(client_ts=None, payload_size=0):
    """
    @brief Lightweight ping endpoint for Eel roundtrip latency diagnostics.
    @details Minimal payload endpoint to measure frontend<->backend roundtrip and payload transfer time.
    @param client_ts Optional client timestamp / Optionaler Client-Timestamp.
    @param payload_size Optional echo payload size in bytes (0..200000) / Optionale Echo-Payload.
    @return Dictionary with timestamps and payload size / Dictionary mit Zeitstempeln und Payload-Gre.
    """
    now_ms = int(time.time() * 1000)

    try:
        size = int(payload_size)
    except Exception:
        size = 0

    size = max(0, min(size, 200000))
    payload = "x" * size if size > 0 else ""

    return {
        "status": "ok",
        "server_ts": now_ms,
        "client_ts": client_ts,
        "payload_size": size,
        "payload": payload,
    }



# --- [confirm_receipt] ---
@eel.expose
def confirm_receipt(event_name):
    """
    @brief Simple confirmation from frontend to backend.
    """
    log.info(f"[Sync] Frontend confirmed receipt of: {event_name}")
    return {"status": "log_noted"}



# --- [delete_media] ---
def delete_media(name):
    """
    @brief Deletes a media item from the database.
    @details Lscht ein Medium aus der DB.
    @param name Media record name / Datenbank-Name.
    """
    logger.debug("file_ops", f"Deleting record: {name}")
    return db.delete_media(name)



# --- [find_venv_pid] ---
@eel.expose
def find_venv_pid(venv_name):
    import psutil
    venv_path = str((PROJECT_ROOT / venv_name).resolve())
    for proc in psutil.process_iter(['pid', 'exe', 'cmdline']):
        try:
            exe = proc.info.get('exe')
            if exe and exe.startswith(venv_path):
                return proc.info['pid']
            cmdline = proc.info.get('cmdline')
            if cmdline and venv_path in ' '.join(cmdline):
                return proc.info['pid']
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return None



# --- [get_active_video_workers] ---
def get_active_video_workers():
    """
    Video Health: Live Worker Audit (v1.37.25).
    Identifies active FFmpeg/MKVMerge processes associated with the workspace.
    """
    import subprocess
    import os

    workers = []
    try:
        # We use 'ps' to get process details for the current user
        # comm= (command name), args= (full command line)
        output = subprocess.check_output(['ps', '-u', str(os.getlogin()), '-o', 'pid,comm,args'], encoding='utf-8')
        lines = output.splitlines()[1:]  # Skip header

        cwd = os.getcwd()

        for line in lines:
            parts = line.strip().split(None, 2)
            if len(parts) < 3:
                continue

            pid, comm, args = parts[0], parts[1], parts[2]

            # Filter for our key workers
            comm_lower = comm.lower()
            if 'ffmpeg' in comm_lower or 'mkvmerge' in comm_lower:
                # Forensic Check: Is it in our CWD?
                # This prevents accidentally listing system-level ffmpeg processes not from our app
                is_workspace = cwd in args

                workers.append({
                    "pid": pid,
                    "name": comm,
                    "command": args[:100] + "..." if len(args) > 100 else args,
                    "is_workspace": is_workspace
                })

        return {"status": "ok", "workers": workers}
    except Exception as e:
        log.error(f"[Forensic-VID] Worker Audit Failed: {e}")
        return {"status": "error", "message": str(e)}



# --- [get_api_forensics] ---
def get_api_forensics():
    registry = [
        {"name": "get_global_health_audit", "status": "EXPOSED"},
        {"name": "get_all_media", "status": "EXPOSED"},
        {"name": "get_db_stats", "status": "EXPOSED"}
    ]
    return api_reporting.get_api_forensics(registry)


# --- [get_app_mode] ---
def get_app_mode():
    """Returns the current app mode (High-Performance/Low-Bandwidth)."""
    return PARSER_CONFIG.get("app_mode", "High-Performance")



# --- [get_category_master] ---
@eel.expose
def get_category_master():
    """Returns the centralized category mapping (v1.35.76 SSOT)."""
    log.info("[BD-AUDIT] Handshake: get_category_master requested.")
    return MASTER_CAT_MAP



# --- [get_environment_forensics] ---
def get_environment_forensics():
    return api_reporting.get_environment_forensics()



# --- [get_footer_registry] ---
def get_footer_registry():
    """ Returns a merged dict of primary flat flags and granular footer sub-settings. """
    settings = GLOBAL_CONFIG.get("ui_settings", {})

    # 1. Primary Flat Flags
    flat_keys = [
        "enable_diagnostics_hud", "enable_dom_auditor", "enable_technical_hud",
        "enable_sync_anchor", "enable_footer_hud_cluster", "enable_zen_mode",
        "enable_footer_db_status"
    ]
    resp = {k: settings.get(k, False) for k in flat_keys}

    # 2. Nested Granular Settings (v1.41.158)
    resp.update(settings.get("footer_settings", {}))
    return resp



# --- [get_gevent_status] ---
def get_gevent_status():
    """Returns the status of gevent patching and version info."""
    try:
        import gevent
        from gevent import monkey
        import greenlet
        import threading

        # Check if threading is actually monkey-patched
        # (Standard threading.current_thread() is replaced by gevent's version)
        is_patched = monkey.is_module_patched("socket")

        return {
            "active": True,
            "version": gevent.__version__,
            "greenlet": greenlet.__version__,
            "patched": {
                "socket": monkey.is_module_patched("socket"),
                "thread": monkey.is_module_patched("thread"),
                "time": monkey.is_module_patched("time"),
                "sys": monkey.is_module_patched("sys"),
                "threading": monkey.is_module_patched("threading")
            }
        }
    except ImportError:
        return {"active": False, "error": "gevent not installed"}



# --- [get_global_config] ---
@eel.expose
def get_global_config():
    """Returns the full centralized configuration (v1.41.00)."""
    log.info("[BD-AUDIT] Handshake: get_global_config requested.")
    return GLOBAL_CONFIG



# --- [get_global_health_audit] ---
def get_global_health_audit():
    return api_reporting.get_global_health_audit()



# --- [get_hardware_forensics] ---
def get_hardware_forensics():
    return api_reporting.get_hardware_forensics()



# --- [get_hydration_stats] ---
def get_hydration_stats():
    """
    Forensic Hydration Sync (v1.37.22): Returns raw counts for DB Index vs Backend Cache.
    """
    from src.core import db
    import sqlite3

    results = {
        "db_index": 0,
        "backend_cache": 0,
        "status": "ok"
    }

    try:
        # 1. RAW SQLite Count
        conn = sqlite3.connect(db.DB_FILENAME)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM media")
        results["db_index"] = cursor.fetchone()[0]
        conn.close()

        # 2. Backend Memory Cache Count
        # We access the module-level library to see what's loaded
        items = db.get_library()
        results["backend_cache"] = len(items)

        return results
    except Exception as e:
        log.error(f"[Forensic-DBI] Audit failed: {e}")
        return {"status": "error", "error": str(e)}



# --- [get_language] ---
def get_language():
    """
    @brief Returns the currently selected UI language.
    @details Gibt die aktuell gewhlte Sprache zurck.
    @return Language code (e.g. 'de', 'en') / Sprachcode.
    """
    return PARSER_CONFIG.get("language", "de")



# --- [get_mock_data_enabled] ---
@eel.expose
def get_mock_data_enabled():
    """Returns whether mock data is enabled in the configuration."""
    return PARSER_CONFIG.get("enable_mock_data", False)



# --- [get_net_ping] ---
def get_net_ping():
    return api_reporting.get_net_ping()



# --- [get_parser_mode] ---
def get_parser_mode():
    """Returns the current parser mode (lightweight/full/ultimate)."""
    return PARSER_CONFIG.get("parser_mode", "lightweight")



# --- [get_playlist_forensics] ---
@eel.expose
def get_playlist_forensics():
    return api_reporting.get_playlist_forensics()


# --- [get_process_forensics] ---
def get_process_forensics():
    return api_reporting.get_process_forensics()


# --- [get_security_forensics] ---
def get_security_forensics():
    return api_reporting.get_security_forensics()


# --- [get_start_page] ---
def get_start_page():
    """Returns the global start page."""
    return PARSER_CONFIG.get("start_page", "player")



# --- [get_startup_config] ---
def get_startup_config():
    """Returns the current startup (browser/env) configuration."""
    return {
        "browser_choice": PARSER_CONFIG.get("browser_choice", "auto"),
        "browser_flags": PARSER_CONFIG.get("browser_flags", []),
        "env_vars": PARSER_CONFIG.get("env_vars", {}),
    }



# --- [get_state_forensics] ---
def get_state_forensics():
    return api_reporting.get_state_forensics()


# --- [get_sys_overview] ---
def get_sys_overview(force_refresh=False):
    """
    @brief Returns comprehensive information about the Python and System environment.
    @details Provides detailed metrics for MediaInfo, FFmpeg, Python Venvs, and Requirements.
    @return Dictionary with high-fidelity system metrics for the Environment Hub.
    """
    import platform
    import subprocess
    import json

    now = time.time()
    if not force_refresh and _ENV_INFO_CACHE["data"] is not None:
        if (now - float(_ENV_INFO_CACHE["ts"])) <= _ENV_INFO_CACHE_TTL_SECONDS:
            return _ENV_INFO_CACHE["data"]

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

    # Determine active runtime environment type and path
    # Priority: active interpreter/venv > conda shell context > system
    env_type = None
    env_path = None
    env_name = None

    if in_venv or venv_env:
        env_type = "venv"
        env_path = venv_path or venv_env
        env_name = Path(env_path).name if env_path else None
    elif in_conda:
        env_type = "conda"
        env_path = conda_prefix
        env_name = conda_env_name
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
            # Main conda call with reduced timeout (3s)
            result = subprocess.run(
                ["conda", "env", "list", "--json"],
                capture_output=True,
                text=True,
                timeout=3
            )
            if result.returncode == 0:
                try:
                    data = json.loads(result.stdout)
                    for env_path in data.get("envs", []):
                        try:
                            env_name = Path(env_path).name
                            env_python = Path(env_path) / "bin" / "python"

                            # Check existence and version with timeout (1s)
                            if env_python.exists():
                                v_result = subprocess.run(
                                    [str(env_python), "--version"],
                                    capture_output=True,
                                    text=True,
                                    timeout=1
                                )
                                version = v_result.stdout.strip() or v_result.stderr.strip()
                                is_recommended = False

                                environments.append({
                                    "name": env_name,
                                    "path": env_path,
                                    "version": version,
                                    "recommended": is_recommended
                                })
                        except (subprocess.TimeoutExpired, Exception):
                            continue
                except (json.JSONDecodeError, KeyError):
                    pass
        except (subprocess.TimeoutExpired, FileNotFoundError, Exception):
            pass
        return sorted(environments, key=lambda x: x["name"])

    def _get_system_pythons():
        """Get list of system Python installations."""
        pythons = []
        search_paths = ["/usr/bin", "/usr/local/bin", "/opt/python"]
        seen_versions = set()

        for search_path in search_paths:
            try:
                search_dir = Path(search_path)
                if not search_dir.exists():
                    continue

                # Use a specific glob to avoid listing too many files
                for python_exe in search_dir.glob("python3*"):
                    try:
                        if not python_exe.is_file() or not os.access(python_exe, os.X_OK):
                            continue

                        result = subprocess.run(
                            [str(python_exe), "--version"],
                            capture_output=True,
                            text=True,
                            timeout=1
                        )
                        version = result.stdout.strip() or result.stderr.strip()

                        if version and version not in seen_versions:
                            seen_versions.add(version)
                            pythons.append({
                                "path": str(python_exe),
                                "version": version
                            })
                    except (subprocess.TimeoutExpired, Exception):
                        pass
            except Exception:
                pass

        return sorted(pythons, key=lambda x: x["version"])

    def _get_packages_fallback():
        """Fallback method to get packages if pip list fails."""
        packages = []
        try:
            from importlib import metadata
            for dist in metadata.distributions():
                name = dist.metadata.get("Name") or dist.metadata.get("name")
                version = dist.version
                if not name:
                    continue
                packages.append({
                    "name": name,
                    "version": version
                })
            packages = sorted(packages, key=lambda x: x["name"].lower())
        except Exception:
            try:
                import pkg_resources
                for dist in pkg_resources.working_set:
                    packages.append({
                        "name": dist.project_name,
                        "version": dist.version
                    })
                packages = sorted(packages, key=lambda x: x["name"].lower())
            except Exception:
                pass
        return packages

    def _get_installed_packages():
        """Get list of installed packages in current environment."""
        packages = []
        source = "none"

        def _parse_columns_output(raw_text: str):
            parsed = []
            lines = [line.strip()
                     for line in (raw_text or "").splitlines() if line.strip()]
            if not lines:
                return parsed
            for line in lines:
                if line.lower().startswith("package") and "version" in line.lower():
                    continue
                if set(line) <= set("- "):
                    continue
                parts = line.split()
                if len(parts) >= 2:
                    parsed.append({"name": parts[0], "version": parts[1]})
            return parsed

        try:
            # Primary method: pip list --format=json (timeout 5s)
            result = subprocess.run([sys.executable,
                                     "-m",
                                     "pip",
                                     "list",
                                     "--format=json",
                                     "--disable-pip-version-check"],
                                    capture_output=True,
                                    text=True,
                                    timeout=5)
            if result.returncode == 0:
                try:
                    packages_data = json.loads(result.stdout)
                    packages = sorted(
                        packages_data, key=lambda x: x.get(
                            "name", "").lower())
                    source = "pip_list_json"
                except (json.JSONDecodeError, TypeError, KeyError):
                    log.warning(
                        "Failed to parse pip list JSON - falling back")
                    packages = _get_packages_fallback()
                    source = "importlib_or_pkg_resources"
            else:
                # Fallback 1: pip list (columns)
                try:
                    fallback_result = subprocess.run(
                        [sys.executable, "-m", "pip", "list", "--format=columns", "--disable-pip-version-check"],
                        capture_output=True,
                        text=True,
                        timeout=5
                    )
                    if fallback_result.returncode == 0:
                        packages = sorted(
                            _parse_columns_output(fallback_result.stdout),
                            key=lambda x: x.get("name", "").lower()
                        )
                        if packages:
                            source = "pip_list_columns"
                except Exception:
                    pass

                # Fallback 2: importlib/pkg_resources
                if not packages:
                    packages = _get_packages_fallback()
                    source = "importlib_or_pkg_resources"
        except (subprocess.TimeoutExpired, Exception) as e:
            log.warning(
                f"pip list failed ({type(e).__name__}) - using importlib fallback")
            packages = _get_packages_fallback()
            source = "importlib_or_pkg_resources"

        return packages, source

    def _find_local_venvs():
        """Find local venv directories in common locations using Multi-Venv Strategy."""
        venvs = []

        # Strategy definition: Detailed multi-venv concept
        VENV_STRATEGY = {
            ".venv_core": {
                "purpose": "Zentrale Laufzeitumgebung fr die App-Logik.",
                "role": "CORE"
            },
            ".venv_run": {
                "purpose": "Optimierte Laufzeitumgebung fr den Anwenderbetrieb.",
                "role": "RUN"
            },
            ".venv_build": {
                "purpose": "Umgebung fr das Packaging (PyInstaller, .deb).",
                "role": "BUILD"
            },
            ".venv_dev": {
                "purpose": "Entwicklungsumgebung mit Lintern (flake8, pyre).",
                "role": "DEV"
            },
            ".venv_testbed": {
                "purpose": "Isolierte Umgebung fr Integrations-Tests.",
                "role": "TEST"
            },
            ".venv_selenium": {
                "purpose": "Umgebung fr E2E Browser-Tests.",
                "role": "E2E"
            }
        }

        try:
            # Discovery of subsidiary venvs based on strategy
            for vname, info in VENV_STRATEGY.items():
                venv_path = PROJECT_ROOT / vname
                exists = venv_path.exists() and (venv_path / "bin" / "python").exists()

                version = None
                if exists:
                    python_exe = venv_path / "bin" / "python"
                    try:
                        result = subprocess.run(
                            [str(python_exe), "--version"],
                            capture_output=True,
                            text=True,
                            timeout=1
                        )
                        version = result.stdout.strip() or result.stderr.strip()
                    except (subprocess.TimeoutExpired, Exception):
                        version = "unknown"

                venvs.append({
                    "name": vname,
                    "path": str(venv_path),
                    "exists": exists,
                    "version": version,
                    "is_current": str(venv_path) == env_path,
                    "purpose": info["purpose"],
                    "role": info["role"]
                })

            # Add legacy/default 'venv' if it exists
            default_venv = PROJECT_ROOT / "venv"
            if default_venv.exists() and (default_venv / "bin" / "python").exists():
                if not any(v["name"] == "venv" for v in venvs):
                    python_exe = default_venv / "bin" / "python"
                    try:
                        result = subprocess.run(
                            [str(python_exe), "--version"],
                            capture_output=True,
                            text=True,
                            timeout=1
                        )
                        version = result.stdout.strip() or result.stderr.strip()
                    except (subprocess.TimeoutExpired, Exception):
                        version = "unknown"

                    venvs.append({
                        "name": "venv",
                        "path": str(default_venv),
                        "exists": True,
                        "version": version,
                        "is_current": str(default_venv) == env_path,
                        "purpose": "Standard Fallback-Umgebung.",
                        "role": "FALLBACK"
                    })
        except Exception as e:
            log.debug(f"Error finding local venvs: {e}")

        return venvs

    def _get_mediainfo_status():
        """Get runtime status for pymediainfo (python) and mediainfo (system)."""
        cli_path = shutil.which("mediainfo")
        pymediainfo_available = False
        pymediainfo_version = None

        try:
            import pymediainfo  # type: ignore
            pymediainfo_available = True
            pymediainfo_version = getattr(pymediainfo, "__version__", None)
        except Exception:
            pymediainfo_available = False

        mediainfo_cli_version = None
        if cli_path:
            try:
                result = subprocess.run(
                    [cli_path, "--version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=2,
                )
                output = result.stdout or ""
                match = re.search(r"v(\d+\.\d+(?:\.\d+)*)", output)
                mediainfo_cli_version = match.group(1) if match else None
            except Exception:
                mediainfo_cli_version = None

        return {
            "pymediainfo_available": pymediainfo_available,
            "pymediainfo_version": pymediainfo_version,
            "mediainfo_cli_available": bool(cli_path),
            "mediainfo_cli_path": cli_path,
            "mediainfo_cli_version": mediainfo_cli_version,
        }

    def _get_runtime_tools_status():
        from src.core.config_master import GLOBAL_CONFIG
        ffmpeg_path = GLOBAL_CONFIG["program_paths"].get("ffmpeg", "ffmpeg")
        ffprobe_path = GLOBAL_CONFIG["program_paths"].get("ffprobe", "ffprobe")
        vlc_cli_path = shutil.which("vlc")
        mkvinfo_path = shutil.which("mkvinfo")
        mkvmerge_path = shutil.which("mkvmerge")
        mkvinfo_version = None
        mkvmerge_version = None
        python_mkv_available = False
        python_mkv_version = None
        try:
            import pymkv
            python_mkv_available = True
            python_mkv_version = getattr(pymkv, "__version__", None)
        except Exception:
            python_mkv_available = False
        if mkvinfo_path:
            try:
                mkvinfo_result = subprocess.run(
                    [mkvinfo_path, "--version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=2,
                )
                first_line = (mkvinfo_result.stdout or "").splitlines()[
                    0] if mkvinfo_result.stdout else ""
                match = re.search(r"mkvinfo v(\S+)", first_line)
                mkvinfo_version = match.group(1) if match else None
            except Exception:
                mkvinfo_version = None
        if mkvmerge_path:
            try:
                mkvmerge_result = subprocess.run(
                    [mkvmerge_path, "--version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=2,
                )
                first_line = (mkvmerge_result.stdout or "").splitlines()[
                    0] if mkvmerge_result.stdout else ""
                match = re.search(r"mkvmerge v(\S+)", first_line)
                mkvmerge_version = match.group(1) if match else None
            except Exception:
                mkvmerge_version = None

        browser_candidates = [
            ("google-chrome", "google-chrome"),
            ("google-chrome-stable", "google-chrome-stable"),
            ("chromium", "chromium"),
            ("chromium-browser", "chromium-browser"),
            ("firefox", "firefox"),
        ]

        browser_name = None
        browser_path = None
        browser_version = None
        for candidate_name, binary in browser_candidates:
            found = shutil.which(binary)
            if found:
                browser_name = candidate_name
                browser_path = found
                break

        if browser_path:
            try:
                browser_result = subprocess.run(
                    [browser_path, "--version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=2,
                )
                first_line = (browser_result.stdout or "").splitlines()[
                    0] if browser_result.stdout else ""
                match = re.search(r"(\d+\.\d+(?:\.\d+){1,3})", first_line)
                browser_version = match.group(1) if match else None
            except Exception:
                browser_version = None

        mutagen_available = False
        mutagen_version = None
        try:
            import mutagen  # type: ignore
            mutagen_available = True
            mutagen_version = getattr(
                mutagen, "version_string", None) or getattr(
                mutagen, "__version__", None)
        except Exception:
            mutagen_available = False

        python_vlc_available = bool(globals().get("HAS_VLC", False))
        python_vlc_version = None
        if python_vlc_available:
            try:
                python_vlc_version = getattr(vlc, "__version__", None)
            except Exception:
                python_vlc_version = None

        ffmpeg_version = None
        if ffmpeg_path:
            try:
                ffmpeg_result = subprocess.run(
                    [ffmpeg_path, "-version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=2,
                )
                first_line = (ffmpeg_result.stdout or "").splitlines()[
                    0] if ffmpeg_result.stdout else ""
                match = re.search(
                    r"ffmpeg version\s+([^\s]+)",
                    first_line,
                    re.IGNORECASE)
                ffmpeg_version = match.group(1) if match else None
            except Exception:
                ffmpeg_version = None

        ffprobe_version = None
        if ffprobe_path:
            try:
                ffprobe_result = subprocess.run(
                    [ffprobe_path, "-version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=2,
                )
                first_line = (ffprobe_result.stdout or "").splitlines()[
                    0] if ffprobe_result.stdout else ""
                match = re.search(
                    r"ffprobe version\s+([^\s]+)",
                    first_line,
                    re.IGNORECASE)
                ffprobe_version = match.group(1) if match else None
            except Exception:
                ffprobe_version = None

        vlc_cli_version = None
        if vlc_cli_path:
            try:
                vlc_result = subprocess.run(
                    [vlc_cli_path, "--version"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.DEVNULL,
                    text=True,
                    timeout=2,
                )
                first_line = (vlc_result.stdout or "").splitlines()[
                    0] if vlc_result.stdout else ""
                match = re.search(r"(\d+\.\d+(?:\.\d+){1,3})", first_line)
                vlc_cli_version = match.group(1) if match else None
            except Exception:
                vlc_cli_version = None

        return {
            "ffmpeg_cli_available": bool(ffmpeg_path),
            "ffmpeg_cli_path": ffmpeg_path,
            "ffmpeg_cli_version": ffmpeg_version,
            "ffprobe_cli_available": bool(ffprobe_path),
            "ffprobe_cli_path": ffprobe_path,
            "ffprobe_cli_version": ffprobe_version,
            "mkvinfo_cli_available": bool(mkvinfo_path),
            "mkvinfo_cli_path": mkvinfo_path,
            "mkvinfo_cli_version": mkvinfo_version,
            "mkvmerge_cli_available": bool(mkvmerge_path),
            "mkvmerge_cli_path": mkvmerge_path,
            "mkvmerge_cli_version": mkvmerge_version,
            "python_mkv_available": python_mkv_available,
            "python_mkv_version": python_mkv_version,
            "browser_available": bool(browser_path),
            "browser_name": browser_name,
            "browser_path": browser_path,
            "browser_version": browser_version,
            "vlc_cli_available": bool(vlc_cli_path),
            "vlc_cli_path": vlc_cli_path,
            "vlc_cli_version": vlc_cli_version,
            "python_vlc_available": python_vlc_available,
            "python_vlc_version": python_vlc_version,
            "mutagen_available": mutagen_available,
            "mutagen_version": mutagen_version,
        }

    # Discovery logic
    conda_envs = _get_conda_environments()
    system_pythons = _get_system_pythons()
    installed_packages, installed_packages_source = _get_installed_packages()
    local_venvs = _find_local_venvs()
    mediainfo_status = _get_mediainfo_status()
    tools_status = _get_runtime_tools_status()
    requirements_status = _get_requirements_status()

    # Core Packages Transformation (Filtering for Dashboard)
    CORE_KEYS = ["bottle", "eel", "gevent", "m3u8", "mutagen", "pymediainfo", "vlc", "psutil"]
    core_packages = []
    for pkg in installed_packages:
        if pkg.get("name", "").lower() in CORE_KEYS:
            core_packages.append(pkg)

    # ===== Build Response (v1.41.00 Unified Schema) =====
    result = {
        # Identifiers
        "python_version": platform.python_version(),
        "python_path": sys.executable,
        "mediainfo": mediainfo_status.get("mediainfo_cli_version") or mediainfo_status.get("pymediainfo_version") or "N/A",
        "ffmpeg": tools_status.get("ffmpeg_cli_version") or "N/A",

        # Lists & Matrices
        "core_packages": core_packages,
        "venvs": local_venvs,
        "conda": conda_envs,
        "requirements": {
            "installed": requirements_status.get("installed_count", 0),
            "total": requirements_status.get("total", 0),
            "missing": requirements_status.get("missing", [])
        }
    }

    _ENV_INFO_CACHE["data"] = result
    _ENV_INFO_CACHE["ts"] = time.time()
    return result



# --- [get_system_environment] ---
def get_system_environment():
    """
    Environment Forensic Audit (v1.37.29).
    Provides real-time resource telemetry and environmental metadata.
    """
    import psutil
    import socket
    import platform
    import time

    try:
        process = psutil.Process()

        # 1. Resource Telemetry
        cpu_percent = process.cpu_percent(interval=None)  # Non-blocking
        mem_info = process.memory_info()
        mem_rss_mb = mem_info.rss / (1024 * 1024)

        # 2. Uptime calculation
        uptime = time.time() - APP_START_TIME

        # 3. Port Health Audit
        port = 8345
        port_status = "error"
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                # If we catch an error, it means we can bind, which means it's NOT bound yet.
                # Since we ARE running, it SHOULD be bound.
                # Checking if OUR process has it would be better, but this is a quick check.
                res = s.connect_ex(('127.0.0.1', port))
                port_status = "active" if res == 0 else "inactive"
        except BaseException:
            pass

        return {
            "status": "ok",
            "telemetry": {
                "cpu": f"{cpu_percent:.1f}%",
                "ram": f"{mem_rss_mb:.1f} MB",
                "uptime": f"{int(uptime)}s",
                "port_8345": port_status
            },
            "platform": {
                "python": platform.python_version(),
                "os": platform.system() + " " + platform.release(),
                "eel": "0.16.0"  # Current Baseline
            },
            "pid": os.getpid()
        }
    except Exception as e:
        log.error(f"[Forensic-ENV] Environment Audit Failed: {e}")
        return {"status": "error", "message": str(e)}



# --- [get_tech_markers] ---
@eel.expose
def get_tech_markers():
    """Returns the centralized transcoding tech markers (v1.35.76 SSOT)."""
    log.info("[BD-AUDIT] Handshake: get_tech_markers requested.")
    return TECH_MARKERS



# --- [get_ui_settings] ---
def get_ui_settings():
    """Returns the current UI registry (v1.46.007 Refined Structure)."""
    # Synthesize the structure expected by ui_core.js
    return {
        **GLOBAL_CONFIG,
        "ui_settings": {
            **GLOBAL_CONFIG,
            "footer_settings": GLOBAL_CONFIG.get("footer_settings", {}),
            "ui_flag_registry": GLOBAL_CONFIG.get("ui_flag_registry", {})
        }
    }



# --- [get_venv_summary] ---
def get_venv_summary():
    """
    @brief Returns a comprehensive summary of the current and available Python environments.
    @details Gibt eine Zusammenfassung der aktuellen und verfgbaren Python-Umgebungen zurck.
    @return Dictionary with environment details and recommendations.
    """
    env_type, env_name, env_path, py_ver, py_exec = _detect_python_environment()

    # Strategy definition: Detailed multi-venv concept
    VENV_STRATEGY = {
        ".venv_core": {
            "purpose": "Zentrale Laufzeitumgebung fr die App-Logik.",
            "role": "CORE",
            "required": True
        },
        ".venv_build": {
            "purpose": "Umgebung fr das Packaging (PyInstaller, .deb).",
            "role": "BUILD",
            "required": False
        },
        ".venv_dev": {
            "purpose": "Entwicklungsumgebung mit Lintern (flake8, pyre).",
            "role": "DEV",
            "required": False
        },
        ".venv_testbed": {
            "purpose": "Isolierte Umgebung fr Integrations-Tests.",
            "role": "TEST",
            "required": False
        },
        ".venv_selenium": {
            "purpose": "Umgebung fr E2E Browser-Tests.",
            "role": "E2E",
            "required": False
        }
    }

    available_venvs = []
    # Discovery of subsidiary venvs based on strategy
    for vname, info in VENV_STRATEGY.items():
        vpath = PROJECT_ROOT / vname
        exists = vpath.exists() and (vpath / "bin" / "python").exists()

        available_venvs.append({
            "name": vname,
            "path": str(vpath),
            "exists": exists,
            "active": (str(vpath) == str(env_path)) if exists else False,
            "purpose": info["purpose"],
            "role": info["role"]
        })

    # Add default 'venv' if it exists but is not in strategy
    default_venv = PROJECT_ROOT / "venv"
    if default_venv.exists() and (default_venv / "bin" / "python").exists():
        if not any(v["name"] == "venv" for v in available_venvs):
            available_venvs.append({
                "name": "venv",
                "path": str(default_venv),
                "exists": True,
                "active": (str(default_venv) == str(env_path)),
                "purpose": "Standard Fallback-Umgebung.",
                "role": "FALLBACK"
            })

    return {
        "current_environment": {
            "type": env_type,
            "name": env_name,
            "path": str(env_path),
            "python_version": py_ver,
            "python_executable": str(py_exec)},
        "available_venvs": available_venvs,
        "multi_venv_concept": "Das Projekt nutzt eine Multi-Venv-Strategie zur Trennung von Core-Logik, Build-System und Testing.",
        "recommended_environment": {
            "name": ".venv_core",
            "type": "venv",
            "reason": "Empfohlene Umgebung fr den stabilen Betrieb der App."}}



# --- [heartbeat] ---
def heartbeat():
    """Explicit heartbeat for window health monitoring (v1.41.00)."""
    GLOBAL_CONFIG["frontend_last_heartbeat"] = time.time()
    return {"status": "ok", "timestamp": time.time()}



# --- [kill_stale_and_restart] ---
def kill_stale_and_restart():
    """
    Kills all project-related processes (v1.35.98 Integrated) and restarts.
    """
    from src.core.process_manager import ProcessController
    from pathlib import Path

    log.info(f"[RESTART] Using ProcessController for emergency cleanup. Root: {PROJECT_ROOT}")
    pc = ProcessController(PROJECT_ROOT, Path(GLOBAL_CONFIG["storage_registry"]["data_dir"]))

    # 1. Forceful cleanup of all project-related processes (including children & ffmpeg)
    pc.kill_stale_instances(current_pid=os.getpid())

    # 2. Restart current process
    log.warning("[RESTART] Executing os.execl...")
    python = sys.executable
    os.execl(python, python, *sys.argv)


# --- [log_gui_event] ---
def log_gui_event(category, action, details=""):
    """General purpose GUI event logging for forensic analysis."""
    log.info(f"[JS-NAV] [{category}] {action} | {details}")



# --- [log_js_error] ---
def log_js_error(error_data):
    """
    Logs JavaScript errors OR toast messages from the frontend to the backend logger.
    """
    if error_data.get('type') == 'TOAST':
        log.info(f"[JS-TOAST] {error_data.get('message')}")
    else:
        log.error(f"[JS-ERROR] {json.dumps(error_data)}")
    return {"status": "error_logged"}



# --- [log_spawn_event] ---
def log_spawn_event(component_id, status):
    """Logs the instantiation/hydration of a UI component (v1.46.03)."""
    log.info(f"🚀 [SPAWN-LOG] {component_id.upper()} -> {status}")
    return True



# --- [nuclear_restart] ---
def nuclear_restart():
    """
    @brief Nuclear Restart: Kills the current backend and reboots via script.
    @details Spawns a detached process to cleanup and restart.
    """
    import os
    import subprocess
    from pathlib import Path

    script_path = PROJECT_ROOT / "scripts" / "reboot_mwv.sh"
    log.warning(f"[REBOOT] NUCLEAR RESTART TRIGGERED. PID: {os.getpid()}")

    try:
        if script_path.exists():
            # Use start_new_session=True to detach from this process tree
            subprocess.Popen(["bash", str(script_path)], start_new_session=True)
            log.info("[REBOOT] Detached reboot script spawned. Exiting current process.")
            # Standard cleanup to close Eel then exit
            os._exit(0)
        else:
            return {"status": "error", "message": "Reboot script not found."}
    except Exception as e:
        log.error(f"[REBOOT] Spawn failed: {e}")
        return {"status": "error", "message": str(e)}



# --- [pip_install_packages] ---
def pip_install_packages(packages):
    """
    @brief Installs a list of Python packages via pip.
    @param packages List of package names to install.
    @return Dictionary with status, output, and error message if any.
    """
    if not packages:
        return {"status": "ok", "message": "No packages to install"}

    if isinstance(packages, str):
        packages = [packages]

    try:
        # Using sys.executable to ensure we install in the current environment
        cmd = [sys.executable, "-m", "pip", "install", *packages]
        log.info(f"Running pip install: {' '.join(cmd)}")

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=GLOBAL_CONFIG.get("ui_settings", {}).get("pip_installer_timeout", 300)
        )

        if result.returncode == 0:
            log.info(
                f"Successfully installed packages: {', '.join(packages)}")
            # After installation, we should probably clear the environment info
            # cache
            _ENV_INFO_CACHE["data"] = None
            _ENV_INFO_CACHE["ts"] = 0.0
            # Double check if they are really installed now
            # Assuming _get_requirements_status is defined elsewhere
            status = _get_requirements_status()
            still_missing = []
            for p in packages:
                # Normalize names for comparison (requirements.txt might have
                # case differences)
                if any(p.lower() == m.lower()
                       for m in status.get("missing", [])):
                    still_missing.append(p)

            if still_missing:
                log.error(
                    f"[PIP] Installation reported success but packages still missing: {still_missing}")
                return {
                    "status": "error",
                    "error": f"Verification failed. Packages still missing: {', '.join(still_missing)}",
                    "output": result.stdout}

            return {
                "status": "ok",
                "output": result.stdout,
                "installed": packages}
        else:
            error_msg = result.stderr or result.stdout or "Unknown pip error"
            log.error(f"Failed to install packages: {error_msg}")
            return {
                "status": "error",
                "error": error_msg,
                "output": result.stdout
            }

    except subprocess.TimeoutExpired:
        log.error("Pip install timed out")
        return {"status": "error", "error": "Installation timed out"}
    except Exception as e:
        log.error(f"Error during pip install: {str(e)}")
        return {"status": "error", "error": str(e)}



# --- [prune_playlist_orphans] ---
@eel.expose
def prune_playlist_orphans(playlist_id):
    return api_reporting.prune_playlist_orphans(playlist_id)


# --- [remove_scan_dir] ---
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



# --- [rename_media] ---
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
        return {
            "status": "error",
            "message": "Name bereits vorhanden oder Fehler"}



# --- [report_items_spawned] ---
def report_items_spawned(count, source="frontend"):
    """
    Formal DOM test reporting. Called when the frontend confirms
    that key UI elements are rendered.
    """
    if count > 0:
        msg = f"[DOM-TEST] [SUCCESS] Items in DOM: {count} (Source: {source})"
    else:
        msg = f"[DOM-TEST] [EMPTY] No items in DOM (Source: {source})."

    log.info(msg)
    return {"status": "counts_logged", "timestamp": time.time()}



# --- [report_playback_state] ---
def report_playback_state(is_playing, item_name, current_time):
    """
    Reports the current playback state from the frontend.
    Used for automated verification of playability.
    """
    msg = f"[DOM-TEST] [PLAYBACK] {'Playing' if is_playing else 'Stopped'} | Item: {item_name} | Pos: {current_time:.1f}s"
    log.info(msg)
    return {"status": "playback_logged"}



# --- [report_spawn] ---
def report_spawn():
    if not spawn_event.is_set():
        spawn_event.set()



# --- [reset_config] ---
def reset_config():
    """Performs a full workstation factory reset (v1.46.010)."""
    log.warning("[FACTORY-RESET] Initializing Full System Restoration...")
    
    # 1. Reset Parser Config
    from src.parsers.format_utils import reset_parser_config
    reset_parser_config()
    
    # 2. Reset UI Registry (Visibility Flags)
    # We essentially re-load the default UI_FLAG_REGISTRY logic 
    # (Simplified for v1.46: just returning success and letting frontend re-sync is often enough
    # if the backend doesn't persist flags to disk yet. 
    # But if it does, we'd clear the config files here.)
    
    log.info("[FACTORY-RESET] Restoration Complete.")
    return {"status": "success", "msg": "Workstation restored to v1.46.010 defaults."}



# --- [rtt_item_test] ---
@eel.expose
def rtt_item_test(data):
    """Echoes complex media-item-like data back for RTT and integrity testing."""
    log.info(f"[RTT] Item Test received: {type(data).__name__}")
    return {
        "status": "success",
        "timestamp": time.time(),
        "item_echo": data
    }



# --- [rtt_ping] ---
def rtt_ping(data):
    """
    @brief Multi-stage RTT Ping for verification.
    @details Logs receipt of specialized data structures.
    Supports 'heartbeat' mode for window health monitoring.
    """
    size = len(json.dumps(data))
    is_heartbeat = isinstance(data, dict) and data.get("type") == "heartbeat"

    if is_heartbeat:
        # Silently log pulse for watchdog health
        GLOBAL_CONFIG["frontend_last_heartbeat"] = time.time()
    else:
        log.info(f"[RTT] Ping received ({size} bytes). Data types: {type(data).__name__}")
        if isinstance(data, dict):
            log.info(f"[RTT] Stage 1 (Dict): {list(data.keys())}")

    return sanitize_json_utf8({
        "status": "pong",
        "timestamp": time.time(),
        "received_size": size,
        "echo": data,
        "is_heartbeat": is_heartbeat
    })



# --- [rtt_stress_ping] ---
@eel.expose
def rtt_stress_ping(index, total):
    """Rapid-fire ping for stress testing."""
    # Minimize logging for stress test to avoid I/O bottleneck
    if index % 10 == 0 or index == total - 1:
        log.info(f"[RTT-Stress] Ping {index + 1}/{total}")
    return {"status": "ok", "index": index}



# --- [run_debug_test] ---
@eel.expose
def run_debug_test():
    """
    Runs a simple debug test and returns result for GUI console.
    """
    import sys
    return {
        "test": "debug",
        "python_version": sys.version,
        "cwd": str(Path.cwd()),
        "result": "OK",
    }



# --- [run_direct_scan] ---
def run_direct_scan():
    """
    Triggers a full re-index from the Diagnostic Hub.
    """
    log.warning("[Diagnostic] Manual DIRECT SCAN triggered from Hub. Clearing DB...")
    try:
        _scan_media_execution(clear_db=True)
        stats = db.get_db_stats()
        return {"status": "success", "items_found": stats.get('total_items', 0)}
    except Exception as e:
        log.error(f"[Diagnostic] Direct Scan failed: {e}")
        return {"status": "error", "message": str(e)}



# --- [run_video_transcode_diagnostic] ---
def run_video_transcode_diagnostic(file_path=None):
    """
    Executes a real-time probe of the video transcoding/remuxing pipelines.
    Returns results compatible with the Diagnostics Suite UI.
    """
    from src.core import db
    import requests

    # 1. Target selection
    target_path = file_path
    if not target_path:
        items = db.get_library()
        if items:
            target_path = items[0]['path']
        else:
            return {"status": "error", "error": "No media found in library to test."}

    log.info(f"[Diagnostic] Testing video pipeline for: {target_path}")
    results = []

    # Endpoints to test (SSOT v1.35.93)
    base_url = GLOBAL_CONFIG['network_settings'].get(
        'api_root', f"http://{GLOBAL_CONFIG['network_settings']['host']}:{GLOBAL_CONFIG['network_settings']['port']}")
    encoded_path = requests.utils.quote(target_path)
    endpoints = [
        {"name": "Remux (Fast)", "url": f"{base_url}/video-remux-stream/{encoded_path}"},
        {"name": "Transcode (Safe)", "url": f"{base_url}/stream/via/transcode/{encoded_path}"}
    ]

    atom_cfg = GLOBAL_CONFIG.get("atom_detection", {"atoms": ["ftyp", "moof", "mdat", "moov"], "header_limit": 4096})

    for ep in endpoints:
        ep_result = {"name": ep['name'], "status": "unknown", "details": ""}
        try:
            r = requests.get(ep['url'], stream=True, timeout=15)
            if r.status_code == 200:
                # Read 512KB to check for atoms
                chunk = next(r.iter_content(chunk_size=GLOBAL_CONFIG["perf_settings"]["chunk_size"]), b'')
                atoms = [a.encode() if isinstance(a, str) else a for a in atom_cfg["atoms"]]
                limit = atom_cfg["header_limit"]
                found = [a.decode() if isinstance(a, bytes) else a for a in atoms if a in chunk[:limit]]

                if found:
                    ep_result["status"] = "success"
                    ep_result["details"] = f"Valid MP4 atoms found: {', '.join(found)}"
                else:
                    ep_result["status"] = "failed"
                    ep_result["details"] = f"No valid MP4 atoms in start of stream (checked {limit} bytes)."
            else:
                ep_result["status"] = "failed"
                ep_result["details"] = f"HTTP Error {r.status_code}"
            r.close()
        except Exception as e:
            ep_result["status"] = "error"
            ep_result["details"] = str(e)
        results.append(ep_result)

    return {"status": "complete", "results": results, "target": target_path}



# --- [sanitize_json_utf8] ---
@eel.expose
def sanitize_json_utf8(data):
    """
    Utility for UTF-8 sanitization of JSON data.
    Ensures all strings in nested dicts/lists are valid UTF-8.
    """
    if isinstance(data, dict):
        return {sanitize_json_utf8(k): sanitize_json_utf8(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [sanitize_json_utf8(i) for i in data]
    elif isinstance(data, str):
        try:
            return data.encode('utf-8', errors='replace').decode('utf-8')
        except Exception:
            return "[Invalid UTF-8]"
    else:
        return data



# --- [scan_media] ---
def scan_media(dir_path: str | None = None, clear_db: bool = True):
    """
    @brief Scans a directory recursively and indexes audio files.
    """
    if getattr(eel, 'js_set_scanning_status', None):
        eel.js_set_scanning_status(True)

    try:
        _scan_media_execution(dir_path, clear_db)
    finally:
        if getattr(eel, 'js_set_scanning_status', None):
            eel.js_set_scanning_status(False)



# --- [set_app_mode] ---
def set_app_mode(mode):
    """Updates the app mode and saves to disk."""
    PARSER_CONFIG["app_mode"] = mode
    save_parser_config()
    return {"status": "success"}



# --- [set_footer_element_state] ---
def set_footer_element_state(element_key: str, is_active: bool):
    """
    Dedicated high-level bridge to toggle footer components and persist state.
    Example element_key: 'enable_sync_anchor'
    """
    log.info(f"[UI-ORCHESTRATION] Requesting state change for footer component: {element_key} -> {is_active}")

    # Validation
    valid_keys = [
        "enable_diagnostics_hud", "enable_dom_auditor", "enable_technical_hud",
        "enable_sync_anchor", "enable_footer_hud_cluster", "enable_zen_mode",
        "enable_footer_db_status"
    ]

    if element_key not in valid_keys:
        log.warning(f"[UI-ORCHESTRATION] REJECTED: Invalid footer component key: {element_key}")
        return False

    return set_ui_config_value(element_key, is_active)



# --- [set_hydration_mode] ---
@eel.expose
def set_hydration_mode(mode: str) -> bool:
    """Sets the hydration mode for library retrieval (v1.41.67)."""
    mode_normalized = mode.lower()
    GLOBAL_CONFIG["forensic_hydration_registry"]["mode"] = mode_normalized
    log.info(f"[HYDR-TRACE] Centralized Hydration mode updated to: {mode_normalized}")
    return True



# --- [set_language] ---
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



# --- [set_log_level] ---
def set_log_level(level):
    """
    Dynamically updates the application log level and persists it.
    """
    import logging
    valid_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }

    if level in valid_levels:
        new_lvl = valid_levels[level]
        logging.getLogger().setLevel(new_lvl)

        # Update all active handlers
        for handler in logging.getLogger().handlers:
            handler.setLevel(new_lvl)

        # Persist to config
        PARSER_CONFIG["log_level"] = level
        save_parser_config()

        log.warning(f"[System] Log level changed to {level} and persisted.")
        return {"status": "success", "level": level}

    return {"status": "error", "message": f"Invalid level: {level}"}



# --- [set_mock_data_enabled] ---
@eel.expose
def set_mock_data_enabled(enabled):
    """Updates the mock data enabled state and saves to disk."""
    PARSER_CONFIG["enable_mock_data"] = enabled
    save_parser_config()
    return {"status": "success"}



# --- [set_parser_mode] ---
def set_parser_mode(mode):
    """Updates the parser mode and saves to disk."""
    PARSER_CONFIG["parser_mode"] = mode
    save_parser_config()
    return {"status": "success"}



# --- [set_start_page] ---
def set_start_page(page):
    """Updates the global start page and saves to disk."""
    PARSER_CONFIG["start_page"] = page
    save_parser_config()
    return {"status": "success"}



# --- [set_ui_config_value] ---
@eel.expose
def set_ui_config_value(key: str, value: Any):
    """
    Sets a configuration value in GLOBAL_CONFIG (v1.38.05).
    Special handling for nested ui_fragments and functional modules.
    """
    from core.config_master import set_config_value as master_set

    log.info(f"[CONFIG] UI Request: {key} -> {value}")

    # Check if it's a nested ui_fragment toggle
    if key.startswith("ui_fragments."):
        frag_key = key.split(".")[1]
        if "ui_settings" in GLOBAL_CONFIG and "ui_fragments" in GLOBAL_CONFIG["ui_settings"]:
            GLOBAL_CONFIG["ui_settings"]["ui_fragments"][frag_key] = value
            log.info(f"[CONFIG] Fragment {frag_key} toggled: {value}")
            return True

    # Check if it's a nested footer_settings toggle (v1.41.158 Extension)
    if key.startswith("footer_settings."):
        feat_key = key.split(".")[1]
        if "ui_settings" in GLOBAL_CONFIG and "footer_settings" in GLOBAL_CONFIG["ui_settings"]:
            GLOBAL_CONFIG["ui_settings"]["footer_settings"][feat_key] = value
            log.info(f"[CONFIG] Granular Footer Feature {feat_key} toggled: {value}")
            return True

    # Generic set
    return master_set(key, value)



# --- [set_ui_setting] ---
def set_ui_setting(key: str, value: Any):
    """Updates a specific UI setting in the global config."""
    if "ui_settings" not in GLOBAL_CONFIG:
        GLOBAL_CONFIG["ui_settings"] = {}
    GLOBAL_CONFIG["ui_settings"][key] = value
    log.info(f"[UI-CONFIG] Set {key} = {value}")
    return {"status": "success"}



# --- [shutdown_backend] ---
def shutdown_backend():
    """Nuclear Shutdown Sequence (Delegated to api_core_app)."""
    api_core_app.shutdown_application()



# --- [sync_library_atomic] ---
def sync_library_atomic():
    """
    Forces a fresh read of the entire library from SQLite and pushes to UI.
    """
    log.info("[Diagnostic] ATOMIC SYNC triggered from Hub.")
    try:
        items = db.get_all_media()
        return {"status": "success", "count": len(items), "items": items}
    except Exception as e:
        log.error(f"[Diagnostic] Atomic Sync failed: {e}")
        return {"status": "error", "message": str(e)}



# --- [terminate_worker_process] ---
def terminate_worker_process(pid):
    return api_reporting.terminate_worker_process(pid)



# --- [trigger_db_reconnect] ---
def trigger_db_reconnect():
    """
    Exposed wrapper to re-initialize the database connection (v1.36.02).
    """
    log.warning("[System] Database Reconnect triggered via Eel.")
    from src.core.db import init_db
    init_db()
    return True



# --- [trigger_factory_reset] ---
def trigger_factory_reset():
    """
    Exposed wrapper to perform a database reset from the UI.
    """
    log.warning("[System] Factory reset triggered via Eel.")
    from src.core.db import factory_reset
    return factory_reset()



# --- [update_browse_dir] ---
@eel.expose
def update_browse_dir(path):
    """Updates the default browse directory."""
    PARSER_CONFIG["browse_default_dir"] = path
    save_parser_config()
    return {"status": "success"}



# --- [update_library_dir] ---
@eel.expose
def update_library_dir(path):
    """Updates the primary library/media directory."""
    PARSER_CONFIG["library_dir"] = path
    save_parser_config()
    return {"status": "success"}



# --- [update_startup_config] ---
def update_startup_config(config):
    """Updates the startup configuration and saves to disk."""
    if "browser_choice" in config:
        PARSER_CONFIG["browser_choice"] = config["browser_choice"]
    if "browser_flags" in config:
        PARSER_CONFIG["browser_flags"] = config["browser_flags"]
    if "env_vars" in config:
        PARSER_CONFIG["env_vars"] = config["env_vars"]

    save_parser_config()
    return {"status": "success"}



# --- [update_tags] ---
def update_tags(name, tags_dict):
    """
    @brief Saves customized tags for a media item in the database.
    @details Speichert angepasste Tags fr ein Item in der DB.
    @param name Media record name / Datenbank-Name des Eintrags.
    @param tags_dict Dictionary of tags to update / Zu aktualisierende Tags.
    @return Status dictionary / Status-Dictionary.
    """
    if DEBUG_FLAGS["db"] or DEBUG_FLAGS["metadata"]:
        logger.debug("metadata", f"Updating tags for {name}: {tags_dict}")
    db.update_media_tags(name, tags_dict)
    return {"status": "ok"}


