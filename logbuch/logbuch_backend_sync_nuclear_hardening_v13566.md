# Backend Sync & Nuclear Hardening (v1.35.66)

## Problem
- The backend was reporting an outdated version (v1.35.63), causing confusion and version mismatch with the frontend.
- The Nuclear Restart (reboot) was unreliable: the backend process exited too quickly, preventing the reboot script from properly initializing a new session.

## Restoration Plan

### 1. Full Stack Version Sync [FIXED]
- **Discovery:** Backend version constant and VERSION file were not updated in sync with the frontend.
- **Fix:** Updated both `main.py` and the `VERSION` file to `1.35.66`, ensuring all APIs and the HUD report the correct version.

### 2. Nuclear Reset Reliability [FIXED]
- **Issue:** `os._exit(0)` was terminating the backend before the reboot script could claim the process group.
- **Fix:** Introduced a 500ms handshake delay in `main.py` after spawning the reboot script, allowing the new process to initialize reliably.

### 3. Path Normalization
- **Fix:** The reboot script path is now resolved absolutely from the project root, preventing directory desync during restarts.

### 4. Version Increment
- **System version** incremented to `v1.35.66` for both backend and frontend, achieving full stack parity.

## Files Patched
- `src/core/main.py`: Version constant, handshake delay, and script path normalization.
- `VERSION`: Updated to `1.35.66`.
- `web/js/version.js`: Ensured HUD displays `v1.35.66`.

## Verification
- Clicking NUCLEAR RESTART now reliably reboots the application.
- The DATA-HUD and all API endpoints report `v1.35.66`.
- No more version mismatch between backend and frontend.

## Outcome
- **Restored:** Full stack version parity and reliable nuclear reboot.
- **Verified:** HUD and backend both show `v1.35.66` after restart.
- **Status:** System stable and synchronized at `v1.35.66`.
