# [PLAN] Recovery Action Audit: Session Trace (v1.37.26)

## Objective
Upgrade the Recovery (REC) tab with a professional audit trail to track all system restoration and stabilization actions during the session.

---

## User Review Required
**NOTE:**
- **Action Verifiability:** This upgrade provides an instant overview of all tactical "fixes" applied during your session. If you prune ghost items or reset a pipeline, it will be documented here for immediate reference.

---

## Proposed Changes

### Sidebar UI (`diagnostics_sidebar.html`)
- **[MODIFY]** Add a high-density viewport (`diag-rec-action-log`) to the REC (Recovery) tab.
- Maintain the existing MASTER CONSOLE buttons for tool parity.

### Controller (`sidebar_controller.js`)
- **[MODIFY]** Implement `logRecoveryAction(name, status, details)`: handles session-level state management for recovery events.
- Hook into all recovery triggers:
  - Master Scan / Master Sync / Nuclear Recovery
  - Ghost Pruning / Database Resilience
  - Pipeline Recovery / Surgical Worker Kill
- Render the action history with forensic chromatic markers (Success-Green / Error-Red) and technical timestamps.

---

## Open Questions
- Should the Recovery Log persist across application restarts? (Recommendation: Keep it session-only for the REC tab to ensure it reflects current stabilization efforts, while the Sentinel trace maintains the permanent history).

---

## Verification Plan

### Automated Tests
- Verify `logRecoveryAction` correctly updates the REC viewport when triggered by a mock sync.

### Manual Verification
- Navigate to the REC tab → Perform a Master Sync.
- Verify the action appears instantly in the REC Action History with workstation styling.
- Perform a Ghost Check → Verify the "Pruning" action is documented with correct item counts.
- Inspect the SENTINEL trace to confirm dual-entry logging is synchronized.

---

## Implementation Checklist
- [ ] Add diag-rec-action-log viewport to REC tab in diagnostics_sidebar.html
- [ ] Implement logRecoveryAction(name, status, details) in sidebar_controller.js
- [ ] Hook logRecoveryAction into all recovery triggers
- [ ] Render action history with chromatic markers and timestamps
- [ ] Integrate SENTINEL trace logging for all recovery actions

---

"Nur ergänzen und nichts entfernen" — Rebuilding the technical heartbeat now. (Continue / "weiter")
