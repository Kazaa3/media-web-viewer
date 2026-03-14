**API Documentation**

This document lists the backend Eel-exposed API endpoints available in the application (implemented in `main.py`). Each entry shows the function signature and a concise description of purpose, parameters and return values.

**General / App Info**
- **handle_click(event_type, payload)**: Generic click dispatcher for simple actions (pin/play/etc.). Returns action result dict.
- **get_imprint_info()**: Returns license, version and maintainer info.
- **get_version()**: Returns application version string.
- **get_app_name()**: Returns application name ("dict").

**Environment & Debug**
- **get_environment_info_dict()**: Full environment dictionary (python, platform, venv, cwd, debug flags).
- **get_environment_info(force_refresh=False)**: More comprehensive environment info with optional refresh and caching.
- **api_ping(client_ts=None, payload_size=0)**: Lightweight latency/payload echo endpoint for diagnostics.
- **run_debug_test()**: Simple debug/test payload (python version, cwd).
- **get_debug_console()**: Returns UI debug logs and environment info for the in-app console.
- **get_debug_logs()**: Returns log history string.
- **get_debug_flags()**: Returns current internal debug flags.
- **set_debug_flag(key, value)**: Set a named debug flag.
- **set_all_debug_flags(value)**: Set all debug flags at once.

**Installation / Environment Helpers**
- **pip_install_packages(packages)**: Installs packages via pip in current interpreter; returns status and pip output.

**Library & Parser**
- **get_library()**: Returns indexed media items from the DB (filtered by `displayed_categories`).
- **get_db_stats()**: Returns DB statistics.
- **clear_database()**: Deletes all DB entries.
- **reset_app_data()**: Wipes DB + config directories and reinitializes.
- **update_tags(name, tags_dict)**: Save custom tags for a media item.
- **rename_media(old_name, new_name)**: Rename a DB record.
- **delete_media(name)**: Delete a DB record.

**Scan / Parser Configuration**
- **get_parser_config()**: Returns current parser configuration dict.
- **get_parser_mapping()**: Returns parser-to-filetype mapping.
- **get_slow_parsers()**: Returns list of parsers flagged as slow.
- **update_parser_config(new_config)**: Merge and persist parser config.
- **get_default_media_dir()**: Returns configured default media directory.
- **ensure_default_scan_dir()**: Ensures default directory present in scan list and returns updated dirs.
- **add_scan_dir() / remove_scan_dir(dir_path)**: Add or remove a scan directory (UI folder picker used by add_scan_dir).

**Scan Execution / Browser**
- **scan_media(dir_path=None, clear_db=True)**: Recursively scan directories, (optionally clear DB), index media files and return media+stats.
- **browse_dir(dir_path=None)**: List folders and audio/video files for in-app file browser.
- **pick_folder()**: Open native folder picker (Tkinter) and return chosen path.
- **add_file_to_library(file_path)**: Add a single file from browser to the library.

**Playback / Playlist**
- **play_media(path)**: Trigger frontend playback for a given path/URL (best-effort updates MediaSession via Eel).
- **play_vlc(file_path)**: Play media with external VLC (requires `python-vlc`).
- **stop_vlc()**: Stop VLC playback.

- **Playlist state & control** (in-memory playlist maintained by backend):
  - **set_current_playlist(items, start_index=0, replace=True)**: Set or append items (list of dicts or names). Returns playlist count and current index.
  - **get_current_playlist()**: Returns `{"items": [...], "index": N}`.
  - **next_in_playlist()**: Advance to next item and trigger playback; returns play status.
  - **prev_in_playlist()**: Play previous item.
  - **jump_to_index(index)**: Play a specific index.

**Platform / UX Helpers**
- **open_in_explorer(path_str)**: Open a file/folder in OS native explorer (xdg-open/open/startfile), returns status.

**Playlist / Import Helpers**
- **import_vlc_playlist(m3u_path)**: Import an m3u/m3u8 playlist into the library (requires `m3u8` package).

Notes
- This list documents the Eel-exposed functions implemented in `main.py` as of this change. Some endpoints perform best-effort calls to the frontend (e.g., `play_media()` attempts `eel.set_media_session()` if available).
- Error handling: most endpoints return dictionaries with `status` or `error` fields; see the implementation in `main.py` for exact keys and additional behavior.
- For UI integration examples, see web/app.html where the frontend calls these endpoints and implements `set_media_session(meta)`.

If you want, I can:
- add example call snippets for each endpoint (JS `eel.foo(...)().then(...)`) or
- generate a small OpenAPI-like JSON for machine consumption.
