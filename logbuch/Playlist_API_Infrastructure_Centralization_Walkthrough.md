# Playlist API & Infrastructure Centralization Walkthrough

We have successfully completed the second phase of the Forensic Media Workstation modernization. This update focuses on logic decoupling, hardcode elimination, and enhanced process management.

---

## Key Accomplishments

### 1. Dedicated Playlist API
- `api_playlist.py`: A new specialized service that manages all playlist operations.
  - Centralized in-memory state (`CURRENT_PLAYLIST`, `CURRENT_INDEX`).
  - Robust reordering logic (`move_item_to`, `move_item_up/down_by_key`).
  - Integrated forensic auditing and relational orphan pruning.
- **Monolith Reduction:** Removed over 400 lines of redundant code from `main.py` and `api_reporting.py`, delegating everything to the new API.

### 2. Infrastructure SSOT (Single Source of Truth)
- **Centralized Configs in `config_master.py`:**
  - `WINDOW_SIZE`: Standardized at 1440x900 for a professional workstation aesthetic.
  - `PORT_CLEANUP_CMD`: Centralized the fuser port kill logic.
  - `DEFAULT_TIME_FORMAT`: Synchronized `%H:%M:%S` across all logging and reporting layers.
  - `FRONTEND_SETTINGS`: Centralized Eel port and browser launch flags.
  - **Project Root Authority:** Eliminated redundant `PROJECT_ROOT` calculations across the codebase. `config_master.py` is now the sole authority for path resolution.

### 3. Advanced Forensic Process Management
- `api_tools.py` Enhancements:
  - `kill_stalled_forensic_processes(binary_name)`: A generic, robust killer for any forensic tool (VLC, FFmpeg, MKVMerge, etc.).
  - `super_kill()`: A "nuclear" cleanup function that terminates all registered forensic tools and browser engines.

### 4. Grouped Forensic Resources
- `MEDIA_RESOURCE_REGISTRY`: Expanded to group all reference media, mock databases, and forensic samples. This paves the way for automated auditing and cross-platform resource discovery.

---

## Verification Results
The refactor was validated using the verification script:

```bash
SUCCESS: All API modules and registries loaded.
FFmpeg Path: /usr/bin/ffmpeg
VLC Path: /usr/bin/vlc
Project Root: /home/xc/#Coding/gui_media_web_viewer
Tool Health Check: 23 tools registered.
```

---

## IMPORTANT
- **Resolution Standard:** The app now defaults to 1440x900. This can be adjusted globally in `config_master.py` via the `WINDOW_SIZE` constant.

> **TIP:**
> All new playlist-related features or forensics should now be implemented directly in `api_playlist.py`.
