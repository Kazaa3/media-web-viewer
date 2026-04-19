# Logbuch: Process PID Differentiation (v1.46.084)

## Date: 2026-04-19

---

## Implementation Plan

### Aggressive Browser Discovery
- Extended the global system scan in `main.py` to specifically target the UI browser process (Chrome/Chromium/etc.), even if launched as a detached system process.
- Integrated browser signature detection into the global `psutil.process_iter` loop to capture detached UI windows.
- Added sorting by `create_time` to prioritize the most recent browser instance.

### PID Collision Guard
- Implemented an explicit filter in `get_system_forensics()` to prevent the Backend PID from ever being assigned to a Frontend or Media Tool slot (`if pid == be_pid: continue`).

### Configuration
- Set `VERSION = "1.46.084"` in `config_master.py`.

### UI Logic
- Updated `version.js` to synchronize with the refined forensic payload.
- Added a visual fallback (color change) if the browser PID remains in N/A state, signaling a discovery delay.

---

## Verification Plan
- **Workstation Audit:** After restart, verify that the BE LED and FE LED tooltips display two distinct, unique PIDs.

---

## Status
- [x] Aggressive browser discovery implemented
- [x] PID collision guard added
- [x] UI logic updated for PID differentiation
- [x] Version incremented
- [ ] Manual verification pending

---

## Notes
- These changes ensure absolute differentiation between Backend and Frontend PIDs, resolving previous collisions and improving forensic accuracy.
- Awaiting user review and manual verification.
