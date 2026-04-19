# Logbuch: Branch-Aware Playlist Orchestration (v1.45.110)

## Overview
This release finalizes the unified, branch-aware playlist system for the Forensic Media Workstation, supporting all build flavors: audio, multimedia, and extended. The architecture now ensures a Single Source of Truth (SSOT) for playlist state and robust synchronization between backend and frontend.

---

## Key Changes

### 1. Unified State & SSOT
- **app_core.js:**
  - Holds authoritative definitions for `window.currentPlaylist` and `window.playlistIndex`.
  - Centralized `syncQueueWithLibrary` logic to orchestrate hydration pulses for all modules.
- **audioplayer.js:**
  - Removed redundant local state to prevent synchronization drift.

### 2. Forensic Handshake Refinement
- **db.js:**
  - `getLibrary()` now accepts an explicit `activeBranch` argument.
- **bibliothek.js:**
  - `loadLibrary()` passes `active_branch` from `GLOBAL_CONFIG` to the backend, ensuring primary filtering by build flavor.

### 3. Player-Specific Rendering Logic
- **audioplayer.js:**
  - Renamed `renderPlaylist` to `renderAudioQueue` for parity with `renderVideoQueue`.
  - Updated `renderAudioQueue` to filter out video items using `!isVideoItem(item)`.
- **video.js:**
  - Updated `renderVideoQueue` to reference the global `window.currentPlaylist` and filter for video items.

### 4. Code Health & Cleanup
- Fixed syntax error in `audioplayer.js` (unmatched closing braces in old `syncQueueWithLibrary`).
- Mass-renamed `renderPlaylist` to `renderAudioQueue` for architectural consistency.

---

## Open Questions
- Should `syncQueueWithLibrary` remain in `audioplayer.js` or move to `app_core.js` for central orchestration?
- Is the new naming (`renderAudioQueue`/`renderVideoQueue`) preferred for clarity and parity?

---

## Verification Summary

### Manual Verification
- In audio mode, only audio assets appear in the queue.
- In multimedia/extended modes, the shared queue is populated with both audio and video assets as appropriate.
- The "Sync" HUD in the footer reports identical counts for database and GUI in parity states.

### Automated Tests
- Checked for zero-item "black holes" during branch transitions; heartbeat and watchdog now verify re-hydration.
- Console logs ([Sync-Audit]) confirm correct counts for each branch.

---

## Status
- The branch-aware playlist system is now robust, branch-respecting, and fully synchronized across all players and build flavors.

**Details and test results are documented in the implementation walkthrough.**
