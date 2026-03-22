# Task Checklist – Video Player Overhaul & MP4 Fix

**Datum:** 17. März 2026

## 1. Research & Debugging
- [x] Investigate current `playMedia` and `startEmbeddedVideo` logic
- [x] Identify cause of MP4 black screen (Audio works, Video doesn't)
- [x] Research Video.js integration and CSS constraints
- [x] Map out file-type specific context menu requirements

## 2. Implementation: Player Overhaul
- [x] Fix MP4 Playback: Ensure Video.js properly displays the video track
- [x] Global Playback: Enable playback from all views (Library, Item, File)
- [x] Dynamic Context Menu: Implement file-extension-aware dropdown menu
- [x] Multi-Mode Support:
  - Chrome Native / Video.js
  - MediaMTX (HLS/WebRTC)
  - ffmpeg FragMP4
  - pyvidplayer2 / VLC Embedded

## 3. UI/UX Refinement
- [x] Improve Video Player tab layout for all modes
- [x] Ensure proper responsive behavior for the video viewport

## 4. Verification & Testing
- [x] Unit Tests:
  - Test media serving logic with mocks
  - Test backend mode detection logic
- [x] Selenium Tests:
  - Verify MP4 playback (non-black screen)
  - Verify multi-mode switching (HLS vs Native)
  - Test context menu sensitivity to file types
- [x] Manual Verification:
  - Test with real MP4/MKV/ISO files from the library

---

**Kommentar:**
Alle Aufgaben zur Video-Player-Überarbeitung und MP4-Fix wurden erfolgreich umgesetzt und getestet. Siehe walkthrough.md für Details und Testergebnisse. (Ctrl+Alt+M)
