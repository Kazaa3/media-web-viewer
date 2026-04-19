# Implementation Plan - High-Density Asset Modeling & Workstation Governance (v1.54.002)

This plan expands the workstation's architecture with localized release tracking, specialized asset classification, centralized quality thresholds, and granular bootstrap governance.

---

## 1. High-Density Asset Modeling
- **[MODIFY] `objects.py`**
  - **ObjectAsset:** New class to model a single file attribute (e.g., "Front Cover (US)", "Disk Art (JP)").
  - **ObjectRelease:** New class to group assets by country, media type (DVD/BD/CD), and edition.
  - **MediaObject Refactor:** Update `FilmObject` and `AlbumObject` to use the new Release/Asset hierarchy instead of flat lists.

---

## 2. Global Quality & Bootstrap Configuration
- **[MODIFY] `config_master.py`**
  - **BITRATE_QUALITY_THRESHOLDS:** Centralized SSOT for quality classification:
    - `high`: 1000 kbps (Lossless/Hi-Res)
    - `standard`: 320 kbps (High Quality)
    - `low`: 192 kbps (Standard Quality)
  - **BOOTSTRAP_GOVERNANCE:**
    - `skip_updates`: Default `False`.
    - `force_updates`: Default `False`.
    - `update_on_version_change`: Default `True`.
    - `last_updated_version`: Tracked to prevent redundant venv activity.

---

## 3. Bootstrap Logic & Runtime Updating
- **[MODIFY] `startup_auditor.py`**
  - **Flag Enforcement:** Respect `--no-update` and `--force-update` CLI arguments.
  - **Version Lock:** Compare current `VERSION` with `last_updated_version` before triggering pip.
- **[MODIFY] `main.py`**
  - `eel.trigger_workstation_update()`: Exposed method to trigger the self-healing cycle during runtime.

---

## 4. UI Synchronization
- **[MODIFY] `app_core.js`**
  - Update `getBitrateQualityClass` to fetch thresholds from the backend config instead of hardcoded values.

---

## Open Questions
- **Runtime Update Strategy:** Should the app restart automatically after a runtime update, or just notify the user that the venv is now synchronized?
- **UI Button:** Should "Update ausführen" (Run Update) be a button in the UI footer next to the version number?

---

**Status:**
- Pending implementation and review.
- This plan ensures high-density asset modeling, centralized quality logic, and robust, user-controlled bootstrap governance.
