# Implementation Plan – Workstation Stability (v1.54.010)

## Objective
Resolve remaining boot-blocking errors and ensure robust recovery from configuration corruption.

---

## User Review Required

### IMPORTANT
- **Typing Registry:** Restore missing `Optional` and `Union` imports in `object_discovery.py`. Their omission caused failures during Object Discovery initialization.
- **Configuration Resets:** Address `JSONDecodeError` by ensuring that if `parser_config.json` is corrupted, the recovery logic will immediately overwrite it with SSOT defaults.

---

## Proposed Changes

### [Core] object_discovery.py
- [MODIFY] Update the typing import block to include `Optional` and `Union`.

### [Core] format_utils.py
- [MODIFY] (Researching line 147) Ensure that when a malformed config is detected, the system not only logs the error but also explicitly overwrites the corrupted file with SSOT defaults immediately.

---

## Verification Plan

### Automated Tests
- Run `/home/xc/#Coding/gui_media_web_viewer/.venv/bin/python3 src/core/startup_auditor.py` to verify the workstation integrity audit passes.
- Manually run `python3 src/core/main.py` (simulated) to ensure imports are resolved.

### Manual Verification
- Verify that the workstation reaches the UI successfully without "Emergency Mode" or `NameError` interruptions.
