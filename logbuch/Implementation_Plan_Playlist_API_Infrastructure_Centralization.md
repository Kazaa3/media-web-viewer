# Implementation Plan: Playlist API & Infrastructure Centralization

This plan addresses the modularization of playlist logic, the centralization of hardcoded infrastructure strings, and the enhancement of forensic process management.

---

## Proposed Changes

### 1. Playlist API Modularization
**[NEW]**
- `api_playlist.py`:
  - Centralize `CURRENT_PLAYLIST` and `CURRENT_INDEX` state.
  - Migrate all playlist functions from `main.py` and `api_reporting.py` (e.g., `set_current_playlist`, `get_current_playlist`, `prune_playlist_orphans`).
  - Expose necessary functions to Eel.

### 2. Config Master Centralization
**[MODIFY]**
- `config_master.py`:
  - Add `WINDOW_SIZE = (1280, 800)` and `FORCE_RESOLUTION_MODE = True`.
  - Add `PORT_CLEANUP_CMD = 'fuser -k 8345/tcp > /dev/null 2>&1'`.
  - Add `DEFAULT_TIME_FORMAT = '%H:%M:%S'`.
  - Add `EEL_KEEPALIVE_CONF = {'sleep_times': {'keepalive': 1.0}}`.
  - Group `MEDIA_DIR`, `MOCK_FILES`, and `FORENSIC_SAMPLES` into `MEDIA_RESOURCE_REGISTRY`.
- `logger.py`:
  - Replace local `PROJECT_ROOT` calculation with import from `config_master`.
- `main.py`:
  - Replace hardcoded `fuser` call with `PORT_CLEANUP_CMD`.
  - Replace hardcoded `%H:%M:%S` with `DEFAULT_TIME_FORMAT`.
  - Use `WINDOW_SIZE` in `eel.start`.

### 3. Forensic Process Management
**[MODIFY]**
- `api_tools.py`:
  - Implement `kill_stalled_forensic_processes(binary_name=None)` to support killing any forensic tool (FFmpeg, VLC, MKVMerge, etc.).
  - Implement `super_kill()` for emergency system-wide cleanup.

---

## User Review Required
**IMPORTANT**
- **Resolution Change:** Centralizing window resolution may change the default app size. Standard is set to 1280x800 (iPad-like). Please confirm if a different resolution is preferred.

**WARNING**
- **PROJECT_ROOT Centralization:** Removing the local calculation in `logger.py` and `verify_refactor.py` and relying on `config_master` assumes `config_master` is ALWAYS available and won't cause circular imports (already guarded in `logger.py`).

---

## Open Questions
- Are there specific "Frontend Options" beyond resolution and keepalive that you want to centralize (e.g. browser paths already exist, maybe theme settings)?

---

## Verification Plan

### Automated Tests
- Run `verify_refactor.py` (after updating it to use centralized `PROJECT_ROOT`).
- Run a new `verify_playlist.py` to ensure the state is correctly shared between `main.py` and `api_playlist.py`.

### Manual Verification
- Launch the app and verify the window size matches the new centralized config.
- Trigger a playlist update and verify it correctly hydrates the UI.
- Verify that `fuser` cleanup still works on port 8345 during startup.
- Test the new generic "kill" function via diagnostic logs.
