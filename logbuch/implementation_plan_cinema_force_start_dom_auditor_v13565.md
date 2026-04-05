# Implementation Plan — Cinema Force-Start & Diagnostic Auditor (v1.35.65)

## Objective
Eliminate navigation and playback race conditions, add a native playback override, enable real/diagnostic library toggling, and introduce a 7-point DOM diagnostic suite for robust UI auditing.

---

## Key Goals
- **"Hyper-Nav" Implementation [FIXED]:**
  - Discovery: `isNavigating` lock was blocking some tab switches.
  - Fix: Use `force: true` for all diagnostic routing to guarantee tab jumps are never ignored.
- **Native Playback Override [NEW]:**
  - Feature: Add a "Force Native" toggle. When active, `playVideo` bypasses backend eel analysis and streams directly to the browser's native engine.
- **Library Toggle: REAL vs. DIAG [NEW]:**
  - UI: Add a glassmorphic switch in the Queue header.
  - Logic: Toggle between the Real Database (actual files) and the Diagnostic Suite (15 stages) with one click.
- **7-Point DOM Diagnostic Suite [NEW]:**
  - Audit: Implement a real-time monitor that checks:
    1. Viewport Visibility: Are main panels on screen?
    2. Splitter Health: Are sidebar widths valid?
    3. Context Menu Stack: Is Z-Index high enough?
    4. Fragment Integrity: Is `video_player.html` loaded?
    5. Active Collision: Are multiple tabs "active" at once?
    6. Layout Offsets: Are header heights correct?
    7. Modal Layering: Are overlays blocking interactions?
- **Version Increment:**
  - Bump to v1.35.65, targeting total cinema control and robust diagnostics.

---

## Components to Modify
- `web/js/ui_nav_helpers.js`: Harden navigation lock release, always allow forced tab switches.
- `web/js/video.js`: Implement "Force Native" streaming logic.
- `web/fragments/dom_auditor.html`: Add the 7-point health dashboard.
- `web/js/version.js`: Increment to v1.35.65.

---

## Expected Outcome
- "Native" button allows bypassing all backend logic for direct playback.
- Glassmorphic switch toggles between real and diagnostic libraries.
- DOM Auditor HUD provides real-time feedback on UI health and visibility issues.

---

## Verification
1. Use the "Native" button: Video streams directly, bypassing backend.
2. Toggle between Real and Diagnostic libraries: Queue updates instantly.
3. DOM Auditor: All 7 checks update in real time, highlighting any UI issues.

---

*Ready to proceed with the Native Force and DOM Auditor implementation as described above.*
