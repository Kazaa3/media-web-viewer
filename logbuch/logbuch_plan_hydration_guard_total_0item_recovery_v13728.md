# [PLAN] Hydration Guard: Total 0-Item Recovery (v1.37.28)

## Objective
Implement a professional-grade recovery dashboard in the main library viewport for cases where the database is completely empty, ensuring immediate re-hydration and constant media availability.

---

## User Review Required
**IMPORTANT:**
- **Resilience:** This upgrade ensures that even if your library is 100% empty, you are never stuck. You will have instant access to the forensic workstation's restoration tools directly in the center of the application.

---

## Proposed Changes

### Library Renderer (`bibliothek.js`)
- **[MODIFY]** Overhaul the `coverflowItems.length === 0` logic in `renderLibrary()`.
- Implement a high-density Forensic Recovery Dashboard for `allLibraryItems.length === 0`.
- Integrate triggers for:
  - `triggerMasterScan()` (Direct FS Scan)
  - `triggerMasterSync()` (Atomic SQLite Sync)
  - `triggerNuclearRecovery()` (Bypass All Filters)
- Maintain and stylize the existing "Filtered Black Hole" logic for when items exist but are hidden.

### Diagnostics Helper (`sidebar_controller.js`)
- **[MODIFY]** (Verified: Master triggers are already exposed via window).

---

## Open Questions
- Should the Hydration Guard also offer a "Demo Mode" trigger for technical testing? (Recommendation: Keep it strictly forensic for v1.37.28, focusing on actual data recovery).

---

## Verification Plan

### Automated Tests
- Verify that `renderLibrary()` correctly identifies both "Filtered" and "Total" empty states.
- Confirm button clicks in the new dashboard correctly call the global workstation triggers.

### Manual Verification
- Manually clear the SQLite index (via the REC tab or GHOST CHECK) → Verify the Total Recovery Dashboard appears.
- Click [DIRECT SCAN] from the main UI → Verify the library hydrates instantly.
- Apply a heavy filter (search for 'xyz123') → Verify the Filtered Black Hole dashboard appears.
- Inspect the SENTINEL trace for the results.

---

## Implementation Checklist
- [ ] Overhaul coverflowItems.length === 0 logic in renderLibrary()
- [ ] Add Forensic Recovery Dashboard for allLibraryItems.length === 0
- [ ] Integrate Direct Scan, Atomic Sync, Nuclear Recovery triggers
- [ ] Maintain/stylize Filtered Black Hole logic
- [ ] Integrate SENTINEL trace logging for all recovery events

---

"Nur ergänzen und nichts entfernen" — Rebuilding the technical heartbeat now. (Continue / "weiter")
