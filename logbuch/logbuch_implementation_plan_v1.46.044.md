# Implementation Plan: Centralized Media Pipelines (v1.46.044)

## Context
This plan migrates the hardcoded audio and video pipeline parameters (MIME types, extensions, orchestration rules) into `config_master.py`. The goal is a pure configuration-driven architecture, simplifying forensic tuning and future adjustments.

---

## User Review Required

### Dynamic Pipeline Resolution
- Replace hardcoded lists in `main.py` and `handlers/` with lookups to `GLOBAL_CONFIG["media_pipeline_registry"]`.
- Changing a MIME mapping or adding a new audio extension will require only a config tweak, not code changes.

### Orchestration Tuning
- Engine-specific logic (e.g., when to trigger MPV WASM vs. Chrome) is moved to `orchestration_flags` in the config for real-time performance adjustments.

---

## Proposed Changes

### [Backend]
#### [MODIFY] `config_master.py`
- [NEW] `media_pipeline_registry`:
    - **audio:** Define `extensions`, `mime_map`, and `default_mode`.
    - **video:** Define `extensions`, `mime_map`, `engines`, and `orchestration_flags` (e.g., `mse_threshold_mbps`).

#### [MODIFY] `main.py`
- Update `server_file_direct`: Remove hardcoded MIME if/elif block; replace with a dictionary lookup from `GLOBAL_CONFIG`.

#### [MODIFY] `mode_router.py`
- Update `smart_route`: Use `orchestration_flags` from the registry to determine thresholds for MSE, DASH, and MPV WASM.

#### [MODIFY] `handlers/__init__.py`
- Update `get_handler_for_file`: Use `GLOBAL_CONFIG["media_pipeline_registry"]["audio"]["extensions"]`.

---

## Open Questions
- Should we also move the player-type defaults (e.g., VLC as fallback for ISO) to the config? (Proposed: Yes, added to the video registry).

---

## Verification Plan

### Automated Tests
- Run `verify_ultimate.py` (if available) to ensure the `GLOBAL_CONFIG` remains valid JSON/Dict structure.
- Verify `server_file_direct` still returns the correct header for `.mp3`.

### Manual Verification
- Toggle a flag in `config_master.py` (e.g., change `.mp3` MIME to `audio/x-test`) and verify it reflects in the backend logs upon restart.

---

(See <attachments> above for file contents. You may not need to search or read the file again.)
