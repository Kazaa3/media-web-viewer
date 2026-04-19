# Implementation Plan – v1.41.11 Ghost Purge & Logic Hardening

This plan addresses the persistent "no effect" issues by purging all ghost processes and hardening the sub-navigation rendering logic.

---

## User Review Required
**CAUTION**
- **Ghost Process Purge:** I have created a "Super Kill" utility to definitively terminate all stale application instances. You must run this command to ensure you are seeing the latest version of the application.

**IMPORTANT**
- **Sub-Menu Restoration:** I found a duplicate key and potential crash in the sub-menu population logic. I will simplify the rendering code to ensure it never fails silently.

---

## Proposed Changes

### Emergency Utilities
- **[NEW] super_kill.py**
  - A standalone script to kill all processes matching `main.py` or port 8345.

### Navigation Logic (Hardening)
- **[MODIFY] ui_nav_helpers.js**
  - **Map Cleanup:** Remove duplicate `'status'` keys in `subNavMap`.
  - **Atomic Render:** Ensure the `.map().join('')` logic is wrapped in a try/catch and has a non-empty fallback.
  - **Normalization:** Force the category to lowercase before look-up.

### Backend Synchronization
- **[MODIFY] main.py**
  - **Shutdown Guard:** Improve the "Off" button logic to ensure a clean process exit (`os._exit(0)`).

---

## Open Questions
None.

---

## Verification Plan

### Manual Verification
- **Run Purge:** Run `python3 src/core/super_kill.py`.
- **Start Fresh:** Start the application and verify the footer definitely says v1.41.00.
- **Status Check:** Click "STATUS" and verify the diagnostic buttons (Logs, Health) appear.
