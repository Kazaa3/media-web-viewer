# [PLAN] Log Forensic Suite: Advanced Filtering (v1.37.21)

## Objective
Upgrade the System Logs (LOG) suite with professional-grade filtering and triage controls for rapid forensic analysis.

---

### User Review Required
**NOTE:**
- **Performance Optimization:** Filtering will be performed on the frontend log cache to ensure zero-latency switching between log levels without additional backend overhead.

---

## Proposed Changes

### Sidebar UI (`diagnostics_sidebar.html`)
- **[MODIFY]** Add a filter control bar to the LOG (System Logs) pane header.
- Include buttons for **ERROR**, **WARN**, and **INFO** levels.

### Controller (`sidebar_controller.js`)
- **[MODIFY]** Update `refreshDebugLogs` to support log-level filtering.
- Implement `filterForensicLogs(level)` to toggle visibility of log entries in the viewport.
- Enhance log entry rendering with high-visibility chromatic labels.

---

## Open Questions
- Should we include a "Live Scroll" lock toggle for the logs? (Recommendation: Add a small "SCROLL LOCK" indicator to ensure the viewport doesn't jump during an active forensic audit.)

---

## Verification Plan

### Automated Tests
- Verify `filterForensicLogs` correctly hides/shows items based on their log-level tags.

### Manual Verification
- Navigate to LOG tab → Click [ERROR].
  - Verify only error-level logs are visible.
- Click [RESET] → Verify all logs return.
- Inspect the SENTINEL trace to ensure filter actions are documented.

---

## Implementation Notes
- Filtering logic will be implemented in the frontend for instant response.
- All filter actions will be logged in the SENTINEL trace for auditability.
- Chromatic labeling will improve log readability and triage speed.

---

## Status
- [ ] UI filter controls designed
- [ ] Filtering logic implemented
- [ ] SENTINEL trace integration complete
- [ ] Verification steps passed

---

"Nur ergänzen und nichts entfernen" — Rebuilding the technical heartbeat now. (Continue / "weiter")



## Implementation Checklist

- Update LOG header in diagnostics_sidebar.html with filter buttons
- Add forensic search input to diagnostics_sidebar.html
- Implement setForensicLogLevel(level) in diagnostics_helpers.js
- Update updateLogFilters logic to handle high-density controls
