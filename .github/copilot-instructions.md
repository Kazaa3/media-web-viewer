# Copilot Agent Instructions for Media Web Viewer

## Big Picture & Architecture
- **Media Web Viewer** is a desktop media player/library manager with a Python backend (Bottle, Eel) and a browser-based frontend (HTML/JS).
- Core backend modules: `main.py` (entry/API), `models.py` (media abstraction), `db.py` (SQLite), `env_handler.py` (environment validation), `logger.py` (logging), `media_format.py` (format logic), `parsers/` (metadata extraction).
- Frontend is served via Eel; backend exposes APIs for media management, playback, and environment info.
- Media parsing is modular: each parser (e.g. `ffprobe_parser.py`, `mutagen_parser.py`) implements a `parse()` function, orchestrated by `extract_metadata()` in `parsers/media_parser.py`.

## Developer Workflows
- **Build artifacts** (Debian, PyInstaller) require passing a targeted test gate (see `build_system.py`, `build.py`, `build_deb.sh`).
- **Test gate**: runs `tests/test_performance_probes.py`, `tests/test_bottle_health_latency.py`, `tests/test_installed_packages_ui.py`, `tests/test_environment_packages_fallback.py`, `tests/test_ui_session_stability.py`.
- **Build commands**:
  - `python build_system.py --build deb|pyinstaller|all` (Debian, PyInstaller, or all)
  - `python build.py` (PyInstaller helper)
  - Override test gate: `SKIP_BUILD_TESTS=1 python build.py`
- **Testing**: `python build_system.py --test` or `pytest tests/`
- **Lint/type-check**: `python build_system.py --lint --type-check`
- **Release pipeline**: `python build_system.py --pipeline` (includes version sync, build, reinstall validation)
- **Version update**: `python update_version.py --new-version <ver>`

## Project Conventions
- **Metadata extraction**: Use `extract_metadata()` for orchestrating parser chains. Each parser must accept `(path, file_type, tags, filename, mode)`.
- **Environment validation**: Always validate via `env_handler.py` before running builds/tests.
- **Logging**: Use `logger.get_logger("component")` for component-specific logs. UI logs are buffered for frontend access.
- **Database**: Use `db.py` for all SQLite access; legacy DB cleanup is handled via `cleanup_legacy_databases()`.
- **Media abstraction**: Use `MediaItem` (in `models.py`) for all media file logic.
- **Build/test gate**: Never skip unless explicitly overridden for emergency/dev.

## Integration & External Dependencies
- **Media tools**: Mutagen, pymediainfo, FFmpeg, python-vlc, m3u8.
- **Browser**: Chrome/Chromium/Firefox required for frontend.
- **CI/CD**: GitHub Actions workflows build/upload artifacts on push/tag.
- **Environment**: Conda or venv supported; validate with `env_handler.py`.

## Patterns & Examples
- **API exposure**: Use `@eel.expose` for backend functions callable from frontend.
- **Parser pattern**: See `parsers/media_parser.py` for orchestrating multiple parsers.
- **Build/test workflow**: See `build_system.py` for pipeline order and quality gate logic.
- **Version sync**: Always update `VERSION` and verify with `tests/test_version_sync.py`.

## Key Files & Directories
- `main.py`: Entry, API, environment detection
- `models.py`: Media abstraction
- `db.py`: SQLite logic
- `env_handler.py`: Environment validation
- `logger.py`: Logging
- `media_format.py`: Format logic
- `parsers/`: Modular metadata extraction
- `tests/`: Test suite (targeted gate, coverage)
- `build_system.py`, `build.py`, `build_deb.sh`: Build logic
- `web/`: Frontend assets

---

**For more details, see [README.md](../README.md) and [DOCUMENTATION.md](../DOCUMENTATION.md).**
