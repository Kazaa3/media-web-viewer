# Implementation Plan: Audio Player Engine "Clean Split" Restoration (v1.38.10)

## Objective
Resolve the persistent "Black Hole" in the Audio Player tab by consolidating split HTML/JS logic into a single, robust Audio Player Engine fragment. This eliminates cross-interference between static app.html code and dynamic fragment loading.

---

## User Review Required
**IMPORTANT**
- Several hardcoded sections will be removed from app.html (player sub-nav and detailed sidebar) and moved into a dedicated fragment.
- The entire Audio Player UI will initialize as an atomic unit, preventing naming mismatches like `switchPlayerView` vs `switchPlayerInternalView`.

---

## Proposed Changes

### UI Consolidation (The "Clean Split")
**[NEW]**
- `audio_player_engine.html`
  - Unified Logic: Combine the player-sub-nav-shell, player-detailed-sidebar, and the main viewport into one file.
  - Consistent View Switching: Use a single, authoritative `switchPlayerView` function defined within the fragment context or bridged correctly from `ui_nav_helpers.js`.

**[MODIFY]**
- `app.html`
  - Eliminate Redundancy: Remove the duplicated player-sub-nav-shell and player-detailed-sidebar blocks (approx. lines 380-473).
  - Placeholder Implementation: Simplify the `state-orchestrated-active-queue-list-container` to a single fragment target: `#audio-player-engine-target`.

### Frontend Logic & Monitoring
**[MODIFY]**
- `ui_nav_helpers.js`
  - Update `FRAGMENT_HYDRATION_REGISTRY`: Point the 'player' fragment to the new `audio_player_engine.html`.
  - Harden UISentinel: Add a specific check for `#audio-player-engine-target` to ensure the core engine container is visible and the fragment is successfully "hydrated."
  - Coordinate `switchTab`: Ensure that when switching to 'player', the fragment load is prioritized before executing initial view setup.

---

## Verification Plan

### Automated Verification
- Observe the BOOT tab -> FRAGMENT INTEGRITY AUDIT. The new AUDIO-PLAYER-ENGINE status should show ACTIVE.
- Check the console for `[Sentinel] CRITICAL FIX` logs related to the player engine.

### Manual Verification
- Confirm that the Audio Player tab is no longer black upon initial launch.
- Confirm that the top sub-menu (Queue, Playlist, Lyrics) is visible and switches views correctly.
- Verify the vertical splitter in the Player tab is functional.

---

## Notes
- The sidebar (split left: queue, right: main player) separation remains logical and will be preserved.
- There are three main components: Audio Player Engine, Tab, and Sidebar. All will be registered in the `FRAGMENT_HYDRATION_REGISTRY`.

---

(See <attachments> above for file contents. You may not need to search or read the file again.)
