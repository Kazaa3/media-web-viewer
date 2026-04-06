# Diagnostics Sidebar Restoration & SENTINEL Live Log (v1.37.09)

## Context
A partial truncation of the Diagnostics Overlay Sidebar removed its multi-tab structure. This update restores the full diagnostics suite and introduces the new "SENTINEL" live log tab for real-time event monitoring.

---

## Implementation Plan

### 1. Diagnostics Sidebar (UI Restoration)
- **Restore all tabs:**
  - HYDRATION
  - ITEM TRACK
  - OVERVIEW
  - LOGS
  - RECOVERY
- **Add new tab:**
  - **SENTINEL:** A live, auto-scrolling feed of system heartbeats (syncs, filter triggers, playback handshakes).
- **Layout Fix:**
  - Repair the HTML structure in the global-diagnostics-sidebar container to ensure all tabs render correctly.

### 2. SENTINEL Integration
- **initSentinelLog():**
  - Listen for `mwv_trace` and `console.warn` events, piping them into the SENTINEL UI.
- **renderSentinelTab():**
  - Create the UI for the live-scrolling log, with persistence (last 50 events in localStorage).

### 3. Navigation Logic
- **js/ui_nav_helpers.js:**
  - Update `switchDiagnosticsSubView` to support the SENTINEL view and all restored tabs.

---

## Open Questions
- **Naming:** Defaulting to "SENTINEL" (alternatives: PULSE, OVERSIGHT).
- **Persistence:** Log will persist last 50 events in localStorage.

---

## Verification Plan
- **Functional Parity:** All 7 diagnostic tabs switch views without closing the sidebar.
- **Live Feed:** Triggering a "Sync" event immediately appears in the SENTINEL tab.

---

**Date:** 2026-04-06
**Author:** GitHub Copilot
