# Logbuch: Forensic Log-Based Repairs (v1.46.089)

## Date: 2026-04-19

---

## Implementation Plan

### Backend: Process Tracking & PID Resolution
- Implemented a global `ACTIVE_FORENSIC_PROCESSES` dictionary in `main.py` to track child PIDs (FFmpeg, VLC, etc.).
- Updated `subprocess.Popen` wrappers to register PIDs upon spawning and remove them on completion/error.
- Added `get_startup_info` extension to resolve the Frontend PID (Browser) using `psutil` by searching for child processes of the main Python app.

### Frontend: UI Structural Alignment & HUD
- **shell_master.html**
  - Corrected header structure to match the 3-slot layout (primary-cluster, header-center-title, secondary-cluster), resolving the "shifted icons" bug.
  - Split the single PID monitor into BE (Backend) and FE (Frontend) labels in the HUD.
  - Removed redundant elements causing the "Extra scroll field" at the bottom.
- **shell_master.css**
  - Hardened `overflow: hidden` on master containers to prevent ghost scrollbars.
  - Ensured correct padding and flex alignment for the secondary-cluster in the header.
- **diagnostics_helpers.js**
  - Updated `refreshStartupInfo` to parse the new dual-PID data from the backend.
  - Enhanced HUD tooltips with the list of active background processes (e.g., "Active: FFmpeg [1234]").

---

## Verification Plan
- **PID Verification:** Confirm that FE and BE PIDs are different in the HUD.
- **UI Alignment:** Verify that top-right icons are perfectly right-aligned and not shifted.
- **Scrollbar Audit:** Use browser tools to confirm no vertical scrollbar appears on the main body.
- **Process List:** Spawn a transcoding task and verify the PID appears in the HUD tooltip.

---

## Status
- [x] Backend process registry implemented
- [x] Dual-PID HUD and tooltips added
- [x] UI alignment and overflow fixes complete
- [ ] Manual/automated verification pending

---

## Notes
- This update provides full forensic process tracking, resolves UI alignment, and eliminates ghost scrollbars for a polished workstation experience.
- Awaiting user review and verification.
