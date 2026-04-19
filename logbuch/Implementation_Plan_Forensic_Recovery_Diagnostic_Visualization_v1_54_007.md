# Forensic Recovery & Diagnostic Visualization Plan (v1.54.007)

This plan addresses workstation startup failures and implements requested diagnostic visualizations for media quality, with a focus on robust dependency checks and forensic clarity in quality mapping.

---

## Phase 1: Startup & Dependency Refortification
**Goal:** Ensure `pyautogui` and `playwright` are installed and verified before the UI boots.

- **[MODIFY] `main.py`**
  - Update the bootstrap guard to check the return value of `startup_auditor.run_audit()`.
  - Add an emergency exit or fallback mode if `run_audit` fails (block startup if critical dependencies are missing).
- **[MODIFY] `startup_auditor.py`**
  - Implement `playwright install` as a post-installation step for the playwright package.
  - Improve logging for `_restore_packages` to show exact pip output on failure.
  - Ensure the version check correctly identifies `v1.54.006` as needing an update vs `v1.54.003`.

---

## Phase 2: SSOT & Quality Mapping
**Goal:** Centralize quality thresholds and forensic object subtypes.

- **[MODIFY] `config_master.py`**
  - Standardize `BITRATE_QUALITY_THRESHOLDS` with the requested values (1000, 320, 192).
  - Update `last_updated_version` to `v1.54.007` to trigger a final comprehensive audit.
  - Refine `AudioObject` vs `AudioRelease` nomenclature in the taxonomy.

---

## Phase 3: Digital Forensic UI Components
**Goal:** Implement the "Audit Pulse" and bitrate indicators.

- **[MODIFY] `main.css`**
  - Add `@keyframes audit-pulse` for the sidebar animation.
  - Add `.quality-high`, `.quality-std`, and `.quality-low` classes with forensic color coding.
- **[MODIFY] `common_helpers.js`**
  - Implement `getBitrateQualityClass(kbps)` following the requested logic.
  - Integrate this class into the library item rendering logic.
- **[MODIFY] `ui_nav_helpers.js`**
  - Add the `triggerAuditPulse()` function to animate the sidebar when filtering or switching domains.

---

## Open Questions
- **Q1:** Should the 1000kbps+ threshold use a "Lossless" badge in addition to the color?
- **Q2:** Should the "Audit Pulse" be automatically triggered on EVERY library filter, or only when the "Forensic Auditor" mode is active?

---

## Verification Plan

### Automated Tests
- `python3 src/core/startup_auditor.py`: Run standalone to verify dependency restoration.
- `npx playwright test`: Use the browser tool to verify UI rendering and quality badges if possible.

### Manual Verification
- Verify that `app.log` shows `[Audit-Deps] SUCCESS` on startup.
- Observe the sidebar for the "Audit Pulse" animation during category switching.
- Inspect media items in the "Grid" or "Coverflow" view to confirm bitrate color-coding.

---

**Status:**
- Pending implementation and review.
- This plan ensures robust startup, clear forensic quality mapping, and professional diagnostic visualization.
