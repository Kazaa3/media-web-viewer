# Hydration Flow Auditor & Master Sync Plan (v1.37.14)

## Modernizing the Hydration Chain Tab

- **Native 7-Stage Flow Auditor:**
  - Provides a high-performance visual audit of the library's path from database to DOM.
- **Filter Forensics:**
  - Integrates a high-visibility "Dropped Reasons" forensic list for backend filtering events.
- **Master Sync Console:**
  - Moves SCAN MEDIA, SYNC LIBRARY, and NUCLEAR RECOVERY controls from the Options panel into the HYD tab, creating a centralized "Control Tower" for library anomaly resolution.

---

## Proposed UI & Logic Changes
- diagnostics_sidebar.html:
  - Add "Command Master" header to HYD tab with [SCAN], [SYNC], [RECOVERY] buttons.
  - Create `diag-pane-hydration-flow` container for the 7-stage report.
  - Integrate "Dropped Reasons" forensic list.
- sidebar_controller.js:
  - Implement `runHydrationAuditProbe()` for backend filter-chain stats and hydration latency.
  - Implement `renderNativeHydrationReport()` for high-performance flow reporting.
  - Implement `triggerMasterScan()` and `triggerMasterSync()` as navigation helpers.
- diagnostics_helpers.js:
  - Deactivate legacy `renderLogicAuditSummary` to ensure a single technical "Source of Truth".

---

## Verification Plan
- Automated: HYD tab triggers flow analysis and "Dropped Reasons" list; SCAN triggers SENTINEL hydration timestamps.
- Manual: "Nuclear Recovery" populates library and is documented in HYD flow report.

---

**Open Question:** Should the Hydration Audit run automatically on tab open, or use a manual [AUDIT] button? (Manual recommended for session stability.)
