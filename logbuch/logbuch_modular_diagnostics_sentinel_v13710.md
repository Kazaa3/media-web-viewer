# Modular Diagnostics & SENTINEL Integration (v1.37.10)

## Overview
This plan modularizes the GLOBAL DIAGNOSTICS OVERLAY SIDEBAR and introduces the SENTINEL live-trace feature, providing a premium, timestamped observability layer for the application.

---

## Key Points
- **Modular Architecture:**
  - Sidebar moved to `web/fragments/diagnostics_sidebar.html`.
  - Dynamically loaded via FragmentLoader, keeping `app.html` clean.
- **SENTINEL (The Listener):**
  - Dedicated tab for a live, timestamped feed of internal application pulses (DB queries, filter results, UI sync events).

---

## Implementation Plan

### 1. HTML Fragment
- **diagnostics_sidebar.html**
  - Move the entire diagnostics sidebar structure here.
  - Add SENTINEL viewport: auto-scrolling log container for live events.

### 2. Sidebar Controller
- **sidebar_controller.js**
  - Handle tab switching and sidebar visibility.
  - SENTINEL engine: capture and render live system events (hook into mwv_trace, log utilities).

### 3. Application Integration
- **app.html**
  - Remove old diagnostics HTML blocks.
  - Add `<div id="diagnostics-overlay-container"></div>` as a placeholder.
  - Ensure dynamic load on boot or first interaction.

### 4. Navigation Logic
- **ui_nav_helpers.js**
  - Update `toggleDiagnosticsSidebar` to work with the modularized sidebar.

---

## Open Questions
- **SENTINEL Persistence:**
  - Should the log persist across sessions or reset on reload? (Recommended: Reset on reload, but add an "Export" option.)

---

## Verification Plan
- **Automated:**
  - Module injection: FragmentLoader injects HTML and executes controller JS.
  - SENTINEL pulse: Mock event appears in the live log with correct timestamp.
- **Manual:**
  - Pulse icon opens the modular sidebar instantly.
  - All 7 tabs (Hydration, Track, Overview, Logs, Video, Latency, Recovery) are fully functional.

---

**Date:** 2026-04-06
**Author:** GitHub Copilot
