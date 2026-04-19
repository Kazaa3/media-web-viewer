# Workstation Infrastructure & API Decoupling Refactor

This plan outlines the transition from a monolithic architecture to a professional, modular infrastructure. We will centralize binary discovery, formalize platform support for forensics tools, and decouple the core application logic into specialized API modules.

---

## User Review Required
**IMPORTANT**

### API Decoupling
Large blocks of logic (streaming, parsing, lifecycle) will be moved from `main.py` and `api_reporting.py` into new dedicated modules. This will significantly change the import structure.

### Tool Discovery
`discover_binary` will now explicitly prioritize `tools/linux/` and `tools/windows/` subfolders.

### Browser Expansion
We will implement a multi-browser discovery registry (Chrome, Chromium, Firefox, etc.) with support for developer editions.

---

## Proposed Changes

### [Core Configuration]
**[MODIFY]**
- `config_master.py`
  - Refactor `discover_binary`:
    - Add platform-aware logic (detecting Linux vs. Windows).
    - Prioritize search in `tools/linux/bin` or `tools/windows/bin` based on OS.
  - Implement `PROGRAM_REGISTRY`:
    - Centralize paths for: VLC, CVLC, FFmpeg, FFprobe, FFplay, Handbrake, MKVToolNix suite, MediaMTX, Spotifyd, SPT, etc.
  - Implement `BROWSER_REGISTRY`:
    - Support for Chrome (stable/dev), Chromium, and Firefox.
  - Implement `MEDIA_RESOURCE_REGISTRY`:
    - Group references to real, mock, and ISO media files for auditing and forensics.

### [Infrastructure Architecture]
**[NEW]**
- `tools/linux`
- `tools/windows`
  - Establish standard subfolders for platform-specific binaries.

### [API Modularization]
**[NEW]**
- `api_tools.py`
  - Move binary discovery helpers, version checks, and tool health diagnostics here.
  - Functionality: `kill_stalled_ffmpeg_streams`, `get_binary_version`, `check_tool_availability`.
- `api_transcoding.py`
  - Move all FFmpeg and MKVMerge remuxing/transcoding logic here.
  - Functionality: `ffmpeg_stream`, `video_remux_stream`, `get_best_hw_encoder`, `play_with_pipekit`.
- `api_core_app.py`
  - Move application lifecycle, startup guards, and core environment logic here.
  - Functionality: `ensure_stable_environment`, startup profiler bridge, lifecycle hooks.
- `api_parsing.py`
  - Move metadata extraction orchestration and parser chain management here.
  - Functionality: `get_media_info`, parser chain resolution logic.

### [Monolith Refactor]
**[MODIFY]**
- `main.py`
  - Replace inline logic with imports from the new `api_*` modules.
  - Maintain eel and bottle route definitions but delegate the heavy lifting to the new APIs.

---

## Open Questions
- **Browser Priority:** Should we prioritize "Google Chrome Developer" over "Google Chrome Stable" if both are found during discovery?
- **Tool Versions:** Do you want the `discover_binary` function to also verify the version is compatible, or just find any version of the tool?

---

## Verification Plan

### Automated Tests
- Run `python3 src/core/config_master.py` (after adding a main block) to verify that the `PROGRAM_REGISTRY` correctly resolves paths on the current system.
- Run `pytest tests/engines/suite_toolchain.py` to ensure all migrated tools are still accessible.

### Manual Verification
- Verify the "BOOT" diagnostic tab still correctly lists all tool versions and paths.
- Perform a "Live Remux" and "Transcode" test in the UI to ensure `api_transcoding.py` is correctly integrated.
