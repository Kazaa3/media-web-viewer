# [PLAN] SENTINEL Forensic Search: Trace Triage (v1.37.23)

## Objective
Upgrade the Sentinel Live-Trace suite with a professional search interface for rapid event isolation and triage.

---

## User Review Required
**NOTE:**
- **Triage Efficiency:** This upgrade allows you to instantly isolate specific forensic tags (e.g., [AUDIT], [ERROR], [BRIDGE]) within the live sentinel stream, significantly reducing post-mortem analysis time.

---

## Proposed Changes

### Sidebar UI (`diagnostics_sidebar.html`)
- **[MODIFY]** Add a forensic search input to the SENTINEL LIVE-TRACE pane header.
- Maintain the existing EXPORT and CLEAR buttons for tool parity.

### Controller (`sidebar_controller.js`)
- **[MODIFY]** Implement `filterSentinelTrace(query)` logic to toggle visibility of trace entries in the viewport.
- Ensure the `sentinelPulse` engine respects the active search filter when injecting new events.
- Enhance trace entry rendering to ensure search keywords are easily identifiable.

---

## Open Questions
- Should we include Regex Support for the sentinel search? (Recommendation: Keep it as a literal substring search for v1.37.23 to ensure maximum performance, adding regex in a future workstation iteration.)

---

## Verification Plan

### Automated Tests
- Verify `filterSentinelTrace` correctly hides/shows items based on the search query.

### Manual Verification
- Navigate to the SNT tab → Perform a system action (e.g., Scan) to generate logs.
- Type a keyword (e.g., "AUDIT") → Verify only relevant trace entries remain visible.
- Perform a new action while filtered → Verify new entries are correctly filtered or shown based on the active query.

---

## Implementation Checklist
- [ ] Add forensic search input to SENTINEL LIVE-TRACE pane header in diagnostics_sidebar.html
- [ ] Implement filterSentinelTrace(query) in sidebar_controller.js
- [ ] Update sentinelPulse to respect active search filter
- [ ] Enhance trace entry rendering for keyword visibility
- [ ] Document search actions in SENTINEL trace

---

"Nur ergänzen und nichts entfernen" — Rebuilding the technical heartbeat now. (Continue / "weiter")
