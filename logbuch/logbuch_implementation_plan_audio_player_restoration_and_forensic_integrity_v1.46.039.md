# Implementation Plan: Audio Player Restoration & Black Hole Fix

## Purpose
Resolve the persistent issue where the media queue remains empty (item = 0) even when the library contains indexed media. The root cause is an overly aggressive filter in the v1.35.68 diagnostic sync logic.

## User Review Required
**IMPORTANT**

### Unified Sync
- Refactor `syncQueueWithLibrary` to treat "Real" and "Diagnostic" items as a single unified pool unless explicitly toggled otherwise.

### Filter Reset
- Ensure that if the queue is empty, the UI provides an immediate "Clear All Filters" rescue action.

### Auto-Hydration
- The player will proactively check if it's empty during tab switching and force a re-load of the library if necessary.

## Proposed Changes

### [Component] Audio Engine (JS)
**audioplayer.js**
- **syncQueueWithLibrary Refactor:**
  - Remove the hard block that drops real items when `isDiagnosticMode` is active.
  - Implement a "Hybrid Sync" that prioritizes real media but keeps diagnostic stages visible in the list.
  - Add an emergency fallback: If the result is 0 and `allLibraryItems` has data, bypass ALL filters to show raw items.
- **renderPlaylist Hardening:**
  - Ensure the `filteredItems` count is correctly mirrored across all UI count labels.
  - Fix the `.synced-queue-target` injection to handle multiple viewports (legacy vs modern).
- **mwv_library_ready Integration:**
  - Ensure this event always triggers a `renderPlaylist()` call after syncing.

### [Component] Common Helpers (JS)
**common_helpers.js**
- **isVideoItem Stability:** Ensure that `item.category` is the absolute source of truth before falling back to extension-based guessing.

### [Component] Library Proxy (JS)
**bibliothek.js**
- **Global Reference Guard:** Explicitly sync `window.allLibraryItems` inside `loadLibrary` to prevent reference drift between the Library and Player modules.

## Open Questions
- Should "Diagnostic Stages" be mixed into the normal queue, or should they have their own section/filter? (Proposed: Mixed but highlighted).

## Verification Plan
- **Automated Tests:**
  - Run `quick_signoff_test.py` to ensure the player UI is visible.
- **Manual Verification:**
  - Verify that real media items (Audio/Video) appear in the "Warteschlange" tab.
  - Toggle "Diagnostic Mode" and verify that items don't disappear.
  - Check the item count in the "Queue" header.

---

# Implementation Plan: Restoring Forensic Integrity & Hydration (v1.46.039)

## Purpose
The migration to `shell_master.html` (the v1.46 Atomic Shell) has resulted in a "logic blackout" where critical JavaScript utilities were omitted from the template. This plan restores the mission-critical forensic stack to ensure that HUD buttons, hydration pulses, and the backend bridge are fully functional.

## User Review Required
**IMPORTANT**

### Script Sequencing
- Restore the scripts in a specific order to avoid ReferenceError dependencies (e.g., `common_helpers.js` must precede `bibliothek.js` where possible, or follow the established v1.41 boot order).

**WARNING**
- Performance Impact: Adding ~15 scripts back will slightly increase initial load time (~200ms), but it is mandatory for the "Forensic Elite" features (Hydration, HUD, Monitoring) to work.

## Proposed Changes

### [Frontend]
**shell_master.html**
- Inject missing core scripts before the bootstrap trigger.
- Add `common_helpers.js` (Restores setHydrationMode).
- Add `diagnostics_helpers.js` (Restores HUD & Pulse monitoring).
- Add `forensic_hydration_bridge.js` (Restores Stage 0->1->2 handshake).
- Add specialized diagnostic stages (BIBLIOTHEK, REAL, etc.) to support the forensic dashboard.

## Open Questions
- Should I remove the legacy `app.html` entirely once stability is confirmed to avoid future confusion?

## Verification Plan
- **Automated Tests:**
  - Refresh the browser via the browser tool (if available) or verify via logs that HYD-CHANGE events now trigger `loadLibrary()`.
  - Run the previously created `test_api.py` to confirm the backend is still responding correctly.
- **Manual Verification:**
  - User should verify that clicking "B" on the footer HUD now correctly hydrates the library with real items.
  - Verify that the LOGS button correctly opens the diagnostics overlay.
