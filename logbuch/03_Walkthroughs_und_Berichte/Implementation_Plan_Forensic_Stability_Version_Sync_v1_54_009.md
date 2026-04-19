# Implementation Plan – Forensic Stability & Version Sync (v1.54.009)

## Objective
Resolve secondary boot failures and formalize version synchronization between backend and forensic UI.

---

## User Review Required

### IMPORTANT
- **JSON Serialization:** Update `ConfigJSONEncoder` in `format_utils.py` to handle `set` objects by converting them to lists. This is required due to recent taxonomy updates introducing set types into `PARSER_CONFIG` (bitrate extensions), which caused serialization crashes.
- **Version Sync:** Synchronize the footer version text (`mwv-footer-version`) with `GLOBAL_CONFIG["version"]`. The user requested this to be "in die gloable config" (synced to global config).

---

## Proposed Changes

### [Core] format_utils.py
- [MODIFY] Update `ConfigJSONEncoder.default` to handle `set` types.
- [MODIFY] Add `set` to the `isinstance` check and return `list(obj)`.

### [Core] object_discovery.py
- [MODIFY] Add the missing `from src.core.logger import get_logger` import.

### [Core] config_master.py
- [MODIFY] Ensure `GLOBAL_CONFIG["version"]` is mapped to the authoritative `APP_VERSION_FULL` or similar.

### [Core] main.py
- [MODIFY] Update `get_version_info` to return the version from `GLOBAL_CONFIG["version"]` as the primary app version.

### [Web] app.html
- [MODIFY] Update the `#mwv-footer-version` span text to include the SYNC marker or version placeholder as requested.

---

## Verification Plan

### Automated Tests
- Run `/home/xc/#Coding/gui_media_web_viewer/.venv/bin/python3 src/core/startup_auditor.py` to verify the workstation integrity audit passes.
- Inspect `logs/app.log` for any remaining JSON serialization errors during config saving.

### Manual Verification
- Check the UI footer and verify the version string correctly represents the current workstation version (e.g., v1.54.009).
- Verify that clicking "REFRESH" or "SCAN" in the UI does not trigger a backend crash.
