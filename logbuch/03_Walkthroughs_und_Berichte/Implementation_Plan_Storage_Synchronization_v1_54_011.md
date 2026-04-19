# Implementation Plan – Storage Synchronization (v1.54.011)

## Objective
Resolve `KeyError: 'media_cache_dir'` by harmonizing storage registry nomenclature.

---

## User Review Required

### IMPORTANT
- **Nomenclature Sync:** Rename `cache_media_dir` to `media_cache_dir` in `config_master.py`. This resolves the mismatch where `main.py` expects `media_cache_dir`, preventing workstation crashes during the Core-Bootstrap phase.

---

## Proposed Changes

### [Core] config_master.py
- [MODIFY] In the `storage_registry` (line 1777), rename key `cache_media_dir` to `media_cache_dir`.

---

## Verification Plan

### Automated Tests
- Run `/home/xc/#Coding/gui_media_web_viewer/.venv/bin/python3 src/core/startup_auditor.py` to verify the workstation integrity audit passes.
- Run `/home/xc/#Coding/gui_media_web_viewer/.venv/bin/python3 src/core/main.py` to verify the application reaches "Core Ready" without a `KeyError`.

### Manual Verification
- Confirm that the workstation starts and reaches the UI successfully.
