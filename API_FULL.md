API — Extended Reference
=======================

This document expands the short API summary with explicit function signatures, parameter descriptions, example responses, and short usage snippets for the Eel-exposed backend functions implemented in `main.py`.

Usage note (frontend JS): all calls use Eel RPC style. Example:

```
// JS example
eel.api_ping(Date.now(), 10)().then(res => console.log('pong', res));

// If you call from Python (tests), call the function directly (it's in main.py namespace).
```

General conventions
- Most endpoints return a dictionary with either `status`/`ok` or `error` keys.
- Some functions perform best-effort operations (e.g., calling frontend functions via `eel.*`) and silently ignore failures.

1. General / App Info
---------------------

- handle_click(event_type: str, payload: dict) -> dict
  - Purpose: Generic click dispatcher. Recognized `event_type` values in current implementation: `pin`, `play`. `payload` is action-specific.
  - Returns: action result dict, e.g. `{"ok": True, "action": "play", "path": "/tmp/song.mp3"}` or error dict.
  - JS example:
    ```js
    eel.handle_click('play', {path: '/media/song.mp3'})().then(res => console.log(res));
    ```

- get_imprint_info() -> dict
  - Purpose: Return version, developer and license info.
  - Example response: `{"version": "1.34", "developer": "kazaa3", "license": "GNU GPL-3.0"}`

- get_version() -> str
- get_app_name() -> str

2. Environment & Debug
----------------------

- get_environment_info_dict() -> dict
  - Purpose: Lightweight environment snapshot (platform, venv, python_executable, debug flags).

- get_environment_info(force_refresh: bool=False) -> dict
  - Purpose: Comprehensive environment info, cached for a short TTL. Use `force_refresh=True` to bypass cache.

- api_ping(client_ts=None, payload_size=0) -> dict
  - Purpose: Echo endpoint for latency and payload sizing tests.
  - Returns: `{"status": "ok", "server_ts": <ms>, "client_ts": <client_ts>, "payload_size": N, "payload": "x..."}`

- run_debug_test() -> dict
- get_debug_console() -> dict
- get_debug_logs() -> str
- get_debug_flags() -> dict
- set_debug_flag(key: str, value: bool) -> None
- set_all_debug_flags(value: bool) -> None

3. Installation / Environment Helpers
------------------------------------

- pip_install_packages(packages: list|str) -> dict
  - Purpose: Run `pip install` in the current interpreter. `packages` may be a single package string or a list.
  - Important: This runs subprocess pip inside the running interpreter — use with care. Response contains `output` and `installed` or `error` details.
  - Example response on success: `{"status": "ok", "output": "...", "installed": ["m3u8"]}`

4. Library & Database
---------------------

- get_library() -> dict
  - Purpose: Returns `{"media": [...]}` with records from the DB filtered by `PARSER_CONFIG["displayed_categories"]`.

- get_db_stats() -> dict
- clear_database() -> dict
  - Example: `{"status": "ok", "message": "Datenbank geleert", "media": []}`

- reset_app_data() -> dict
  - Purpose: Remove DB and config directories, reinitialize. Returns list of deleted paths.

- update_tags(name: str, tags_dict: dict) -> dict
- rename_media(old_name: str, new_name: str) -> dict
- delete_media(name: str) -> dict

5. Parser / Scan Configuration
------------------------------

- get_parser_config() -> dict
- update_parser_config(new_config: dict) -> dict
- get_parser_mapping() -> dict
- get_slow_parsers() -> list

- get_default_media_dir() -> str
- ensure_default_scan_dir() -> dict
- add_scan_dir() -> dict  (opens native folder dialog)
- remove_scan_dir(dir_path: str) -> dict

Notes:
- `add_scan_dir()` uses a Tkinter folder picker via `pick_folder()` (may fail in headless envs).

6. Scanning & Browser
----------------------

- scan_media(dir_path: str|None=None, clear_db: bool=True) -> dict
  - Purpose: Recursively scans configured scan dirs (or `dir_path`) and inserts found media into DB.
  - Behavior: Optionally clears DB if `clear_db` is True. Returns `{"media": [...], "stats": {"count": N, "time_seconds": T}}`.

- browse_dir(dir_path: str|None=None) -> dict
  - Returns listing `{"path": "...", "parent": "...", "items": [...]}` where items have `name`, `path`, `type`, and optionally `size`.

- pick_folder() -> str|None
  - Opens OS folder selection using Tkinter. Returns selected path or `None`.

- add_file_to_library(file_path: str) -> dict
  - Adds a single file to DB after basic validation. Returns `{"status": "added", "item": {...}}` or error.

7. Playback & Playlist (detailed)
--------------------------------

Playback Helpers:

- play_media(path: str) -> dict
  - Purpose: Trigger frontend playback. The frontend is responsible for playing media in the browser. Backend will attempt a best-effort call to `eel.set_media_session({...})` to update the browser Media Session.
  - Returns: `{"status": "play", "path": path}`.
  - Note: If path refers to a DB record name rather than a filesystem path, the playlist helpers attempt DB resolution.

- play_vlc(file_path: str) -> dict
  - Requires `python-vlc`. Spawns an external VLC instance on the host and plays the given file. Returns `{"status": "ok"}` or `{"error": "..."}`.

- stop_vlc() -> dict

Playlist state (backend-managed in-memory):

- set_current_playlist(items: list, start_index: int = 0, replace: bool = True) -> dict
  - `items` may be a list of `str` names or `dict` entries like `{"name":"...","path":"..."}`.
  - If `replace` is False the list is appended. Returns `{"status":"ok","count":N,"index":idx}`.

- get_current_playlist() -> dict
  - Returns current `{"items": [...], "index": N}`.

- next_in_playlist() -> dict
  - Advances to next index and calls `play_media()` for the resolved path. Returns play result or `{"status":"end"}` at list end.

- prev_in_playlist() -> dict
  - Plays previous item or returns `{"status":"start"}` when at beginning.

- jump_to_index(index: int) -> dict
  - Plays the item at `index` after validation; returns play result or error if invalid.

Example integration (JS):

```
// Set playlist and play first item
eel.set_current_playlist([{name:'song1', path:'/media/song1.mp3'}, {name:'song2', path:'/media/song2.mp3'}], 0)().then(res => console.log(res));
eel.get_current_playlist()().then(p => console.log(p));
eel.next_in_playlist()().then(r => console.log('next', r));
```

8. Import / Utility
-------------------

- import_vlc_playlist(m3u_path: str) -> dict
  - Purpose: Parse a playlist file (m3u/m3u8) and import referenced files into the library. Requires `m3u8` package.

- open_in_explorer(path_str: str) -> dict
  - Opens OS-native file viewer. On Linux uses `xdg-open`, on macOS `open -R`, on Windows `os.startfile`.

9. Error Handling & Edge Cases
-----------------------------

- Headless / CI: UI-related calls (folder picker, eel frontend callbacks) may fail in headless/CI. Functions try/except and return friendly errors or `None`.
- Permissions: `browse_dir()` returns `{"error": "Keine Berechtigung"}` on permission errors.
- pip_install: may require elevated permissions or network; prefer virtualenv usage for safety.

10. Next steps I can do for you
------------------------------

- Add JS example snippets for every endpoint (I can add them inline to `docs/API_FULL.md`).
- Produce a JSON or OpenAPI-like machine-readable descriptor for automated client generation.
- Generate a tiny `examples/api_client.html` demonstrating several common calls.

File locations
- Short summary: /home/xc/#Coding/gui_media_web_viewer/docs/API.md
- Extended reference (this file): /home/xc/#Coding/gui_media_web_viewer/docs/API_FULL.md

If you'd like, I can now update the todo list to mark this extended doc complete and then run the repo-tracked test or prepare a commit. Which next step do you want?
