# Implementation Plan: Forensic Workforce Modularization (Phase 3)

This plan outlines the next major evolution of the Forensic Media Workstation, focusing on deep infrastructure centralization and the final decoupling of high-level features.

---

## Proposed Changes

### 1. Config Master: Infrastructure SSOT (Single Source of Truth)
**[MODIFY]**
- `config_master.py`:
  - **Logging Registry:** Implement `LOGGING_REGISTRY` mapping log roots, file names, and rotation policies.
  - **Tool Registry Expansion:** Consolidate `FORENSIC_TOOLS_LIST` (ffmpeg, vlc, mkvmerge, etc.) into a centralized constant.
  - **App Launch Profiles:** Centralize command-line flag logic (`--n`, `--ng`, `--debug`) into a `LAUNCH_PROFILE` configuration.
  - **Browser Registry:** Refine browser channel discovery and paths.

### 2. Logging System Upgrade
**[MODIFY]**
- `logger.py`:
  - Refactor to import `LOGGING_REGISTRY` from `config_master.py`.
  - Eliminate local path calculations in favor of the registry.

### 3. Modular API Expansion
We will create four new API modules to absorb the remaining complexity from `main.py`:
- **[NEW]** `api_frontend.py`: Handles browser discovery, "set browser" logic, and UI settings.
- **[NEW]** `api_orchestrator.py` (proposed name for `api_mediaserving.py`): Manages Bottle/Eel routes for direct file serving, transcoding, and remuxing.
- **[NEW]** `api_logbuch.py`: Handles CRUD operations for the forensic logbuch (Markdown files).
- **[NEW]** `api_testing.py`: Consolidates benchmarks, QA integrity checks, and test hooks.

### 4. Monolith Clean-up (`main.py`)
**[MODIFY]**
- Delegate all related logic to the new `api_*` modules.
- Standardize the `start_app` routine to use the new `LAUNCH_PROFILE`.
- Cleanup redundant imports.

### 5. API Tools Alignment
**[MODIFY]**
- `api_tools.py`:
  - Update kill functions to use the centralized `FORENSIC_TOOLS_LIST`.

---

## User Review Required
**IMPORTANT**
- **API Naming:** Proposed `api_orchestrator.py` instead of `api_mediaserving.py` because it orchestrates complex streaming pipelines (remux/transcode) in addition to serving. Please confirm if this name is acceptable.

**WARNING**
- **Logging Bootstrap:** Centralizing logging into `config_master` creates a direct dependency between the logger and the config registry. This is safe due to existing guards but is a critical structural change.

---

## Verification Plan

### Automated Tests
- Run `verify_refactor.py` (updated to check the new modules).
- Verify log file generation in the new centralized `logs/` directory.

### Manual Verification
- Launch the app with various flags (`--ng`, `--n`) and verify the `LAUNCH_PROFILE` handles them correctly.
- Verify that Logbuch entries can still be created/read/deleted.
- Test media playback across all delivery modes (Direct, Remux, Transcode).
