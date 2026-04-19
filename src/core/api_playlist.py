import os
import json
import logging
from pathlib import Path
from typing import List, Dict, Any, Optional

import eel
from src.core.config_master import GLOBAL_CONFIG, PROJECT_ROOT
from src.core import db

log = logging.getLogger("api_playlist")

# --- In-Memory Playlist State (v1.46.135 Centralized) ---
CURRENT_PLAYLIST: List[Dict[str, Any]] = []
CURRENT_INDEX: int = -1

def get_state() -> Dict[str, Any]:
    """Returns the current internal state (for internal API users)."""
    return {"items": CURRENT_PLAYLIST, "index": CURRENT_INDEX}

@eel.expose
def set_current_playlist(items: list, start_index: int = 0, replace: bool = True):
    """Set the active playlist. `items` is a list of media dicts or names."""
    global CURRENT_PLAYLIST, CURRENT_INDEX
    normalized = []
    for it in items:
        if isinstance(it, str):
            normalized.append({"name": it})
        elif isinstance(it, dict):
            normalized.append(it)
    
    if replace:
        CURRENT_PLAYLIST = normalized
    else:
        CURRENT_PLAYLIST.extend(normalized)

    if not CURRENT_PLAYLIST:
        CURRENT_INDEX = -1
    else:
        CURRENT_INDEX = max(0, min(len(CURRENT_PLAYLIST) - 1, int(start_index or 0)))

    log.info(f"[Playlist] Set/Updated: {len(CURRENT_PLAYLIST)} items (Index: {CURRENT_INDEX})")
    return {"status": "ok", "count": len(CURRENT_PLAYLIST), "index": CURRENT_INDEX}

@eel.expose
def get_current_playlist():
    """Returns the current playlist and active index."""
    return {"items": CURRENT_PLAYLIST, "index": CURRENT_INDEX}

@eel.expose
def get_current_playlist_exposed():
    """Alias for frontend refresh compatibility."""
    return get_current_playlist()

def _play_index(idx: int):
    """Internal: update index and trigger media playback via main bridge."""
    global CURRENT_INDEX
    if not CURRENT_PLAYLIST:
        return {"status": "error", "message": "no playlist"}
    if idx < 0 or idx >= len(CURRENT_PLAYLIST):
        return {"status": "error", "message": "index out of range"}
    
    CURRENT_INDEX = idx
    item = CURRENT_PLAYLIST[CURRENT_INDEX]
    path = item.get("path") or item.get("name")
    
    # Resolve DB shortcut names to actual paths
    try:
        if path and not Path(path).exists():
            match = db.get_media_by_name(path)
            if match:
                path = match.get("path") or path
    except Exception:
        pass

    # We call back into main for the actual playback orchestration
    from src.core.main import play_media
    return play_media(path)

@eel.expose
def jump_to_index(index: int):
    try:
        idx = int(index)
        return _play_index(idx)
    except Exception as e:
        return {"status": "error", "message": f"Invalid index: {e}"}

@eel.expose
def next_in_playlist():
    global CURRENT_INDEX
    if not CURRENT_PLAYLIST:
        return {"status": "error", "message": "no playlist"}
    next_idx = CURRENT_INDEX + 1 if CURRENT_INDEX + 1 < len(CURRENT_PLAYLIST) else -1
    if next_idx == -1:
        return {"status": "end"}
    return _play_index(next_idx)

@eel.expose
def prev_in_playlist():
    global CURRENT_INDEX
    if not CURRENT_PLAYLIST:
        return {"status": "error", "message": "no playlist"}
    prev_idx = CURRENT_INDEX - 1 if CURRENT_INDEX - 1 >= 0 else -1
    if prev_idx == -1:
        return {"status": "start"}
    return _play_index(prev_idx)

@eel.expose
def move_item_up(index: int):
    global CURRENT_PLAYLIST, CURRENT_INDEX
    try:
        idx = int(index)
        if idx <= 0 or idx >= len(CURRENT_PLAYLIST):
            return {"status": "error", "message": "Index out of range"}
        
        CURRENT_PLAYLIST[idx-1], CURRENT_PLAYLIST[idx] = CURRENT_PLAYLIST[idx], CURRENT_PLAYLIST[idx-1]
        
        if CURRENT_INDEX == idx: CURRENT_INDEX = idx - 1
        elif CURRENT_INDEX == idx - 1: CURRENT_INDEX = idx
        
        return {"status": "ok", "items": CURRENT_PLAYLIST, "index": CURRENT_INDEX}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@eel.expose
def move_item_down(index: int):
    global CURRENT_PLAYLIST, CURRENT_INDEX
    try:
        idx = int(index)
        if idx < 0 or idx >= len(CURRENT_PLAYLIST) - 1:
            return {"status": "error", "message": "Index out of range"}
        
        CURRENT_PLAYLIST[idx], CURRENT_PLAYLIST[idx+1] = CURRENT_PLAYLIST[idx+1], CURRENT_PLAYLIST[idx]
        
        if CURRENT_INDEX == idx: CURRENT_INDEX = idx + 1
        elif CURRENT_INDEX == idx + 1: CURRENT_INDEX = idx
        
        return {"status": "ok", "items": CURRENT_PLAYLIST, "index": CURRENT_INDEX}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@eel.expose
def remove_playlist_item(index: int):
    global CURRENT_PLAYLIST, CURRENT_INDEX
    try:
        idx = int(index)
        if not CURRENT_PLAYLIST or idx < 0 or idx >= len(CURRENT_PLAYLIST):
            return {"status": "error", "message": "Invalid index"}
        
        CURRENT_PLAYLIST.pop(idx)
        if CURRENT_INDEX == idx: CURRENT_INDEX = -1
        elif CURRENT_INDEX > idx: CURRENT_INDEX -= 1
        
        return {"status": "ok", "items": CURRENT_PLAYLIST, "index": CURRENT_INDEX}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@eel.expose
def clear_playlist():
    global CURRENT_PLAYLIST, CURRENT_INDEX
    CURRENT_PLAYLIST = []
    CURRENT_INDEX = -1
    return {"status": "ok"}

@eel.expose
def save_playlist(media_names: list, output_path: str):
    """Saves the current playlist to a JSON file."""
    try:
        data = {"version": "v1.46", "items": media_names}
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
        return True
    except Exception as e:
        log.error(f"[Playlist] Save failed: {e}")
        return False

@eel.expose
def load_playlist(input_path: str):
    """Loads a playlist from a JSON file."""
    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data.get("items", [])
    except Exception as e:
        log.error(f"[Playlist] Load failed: {e}")
        return []

@eel.expose
def move_item_to(old_index: int, new_index: int):
    """Move an item from old_index to new_index within CURRENT_PLAYLIST."""
    global CURRENT_PLAYLIST, CURRENT_INDEX
    try:
        o, n = int(old_index), int(new_index)
        if not CURRENT_PLAYLIST or o < 0 or o >= len(CURRENT_PLAYLIST) or n < 0:
            return {"status": "error", "message": "Index out of range"}
        
        length = len(CURRENT_PLAYLIST)
        if n > length: n = length
        if o == n or (o == n - 1 and o < n):
            return {"status": "ok", "items": CURRENT_PLAYLIST, "index": CURRENT_INDEX}

        item = CURRENT_PLAYLIST.pop(o)
        if n > len(CURRENT_PLAYLIST): n = len(CURRENT_PLAYLIST)
        CURRENT_PLAYLIST.insert(n, item)

        if CURRENT_INDEX == o: CURRENT_INDEX = n
        else:
            if o < CURRENT_INDEX <= n: CURRENT_INDEX -= 1
            elif n <= CURRENT_INDEX < o: CURRENT_INDEX += 1

        return {"status": "ok", "items": CURRENT_PLAYLIST, "index": CURRENT_INDEX}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def _matches_key(it, key):
    if not isinstance(it, dict): return False
    for f in ('name', 'filename', 'path', 'id'):
        if it.get(f) == key: return True
    tags = it.get('tags') or {}
    if tags.get('title') == key: return True
    for f in ('name', 'filename', 'path'):
        v = it.get(f)
        if v and isinstance(v, str) and key in v: return True
    return False

@eel.expose
def move_item_up_by_key(key: str):
    global CURRENT_PLAYLIST
    for idx, it in enumerate(CURRENT_PLAYLIST):
        if _matches_key(it, key):
            return move_item_up(idx)
    return {"status": "error", "message": "item not found"}

@eel.expose
def move_item_down_by_key(key: str):
    global CURRENT_PLAYLIST
    for idx, it in enumerate(CURRENT_PLAYLIST):
        if _matches_key(it, key):
            return move_item_down(idx)
    return {"status": "error", "message": "item not found"}

def _extract_key(item_obj: dict) -> str:
    if not isinstance(item_obj, dict): return ""
    for k in ['id', 'path', 'filepath', 'url', 'key']:
        if item_obj.get(k): return str(item_obj[k])
    return ""

@eel.expose
def move_item_up_by_obj(item_obj):
    return move_item_up_by_key(_extract_key(item_obj))

@eel.expose
def move_item_down_by_obj(item_obj):
    return move_item_down_by_key(_extract_key(item_obj))

# --- Forensic & Reporting Bridge (v1.46.135) ---

def get_playlist_forensics():
    """Playlist Forensic Audit: Integrity & Repair."""
    playlists = db.get_all_playlists()
    results = {"status": "ok", "playlists": []}
    for pl in playlists:
        items = db.get_playlist_items(pl['id'])
        orphans = db.get_playlist_orphans(pl['id'])
        results["playlists"].append({
            "id": pl['id'],
            "name": pl['name'],
            "item_count": len(items),
            "orphan_count": len(orphans),
            "status": "HEALTHY" if len(orphans) == 0 else "DEGRADED"
        })
    return results

def prune_playlist_orphans(playlist_id):
    """Surgical Pruning for Playlist Relational Orphans."""
    try:
        count = db.prune_playlist_orphans(playlist_id)
        log.info(f"[Forensic-Repair] Pruned {count} orphans from playlist {playlist_id}")
        return {"status": "ok", "pruned_count": count}
    except Exception as e:
        log.error(f"[Forensic-Repair] Pruning failed: {e}")
        return {"status": "error", "message": str(e)}
