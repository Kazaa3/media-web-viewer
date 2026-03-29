# Implementation Plan: System Refactor & DOM Hardening

This plan outlines a complete refactor of the Media Viewer's core architecture, focusing on standardizing the app.html structure and modularizing all remaining business logic to ensure a robust "hardened" environment.

---

## User Review Required

**IMPORTANT**

This refactor will significantly change the physical structure of app.html. While functionality will remain identical, the file size will decrease as logic moves to external .js files.

**WARNING**

Moving the Eel Shim to an external file requires careful loading order. We will use a dedicated eel_shim.js that must be loaded before any other helper to ensure connectionless mode stability.

---

## Proposed Changes

### 1. Script Consolidation & Modularization
- Group all remaining inline logic into dedicated helper files.

**[NEW] eel_shim.js**
- Extract the large Proxy-based Eel shim from app.html.
- Standardize the defaults object for connectionless mode.

**[NEW] media_session_helpers.js**
- Extract all navigator.mediaSession logic (metadata updates, action handlers).
- Provide a unified window.updateMediaSession(meta) interface.

**[MODIFY] app.html**
- Remove all remaining inline <script> blocks (lines 11, 70, 88, 4101, etc.).
- Consolidate script imports in the <head> and remove duplicates (e.g., lines 158-162).
- Ensure eel_shim.js is loaded first.

### 2. Semantic HTML & DOM Hardening
- Refactor the DOM to use modern standards and consistent naming.

**[MODIFY] app.html**
- Semantic Tags: Replace top-level container divs with standard tags:
  - <div class="header-container"> -> <header class="layout-header">
  - <div class="layout-container"> -> <main class="layout-main">
  - <div class="bottom-bar"> -> <footer class="layout-footer">
- Naming Consistency: Standardize IDs to camelCase and classes to kebab-case.
- Integrity IDs: Add descriptive IDs to any major UI sections currently missing them (e.g., search bars, filter groups).

### 3. Centralized Logging & Diagnostics
- Move error handling and readiness checks to the helper layer.

**[MODIFY] system_helpers.js**
- Move window.onerror and unhandledrejection logic here.
- Implement a unified Logger object that sends errors to the backend via eel.log_js_error.

**[MODIFY] debug_helpers.js**
- Move the "DOM Watchdog" logic here.
- Integrate the "7 Stages of UI Integrity" into a single, reachable diagnostic function window.runIntegrityCheck().

### 4. Cleanup & Optimization
**[MODIFY] index.css (if exists) or main.css**
- Move inline styles from app.html (e.g., flex gaps, padding) into the stylesheet using scoped classes.

---

## Open Questions
- **Offline Assets:** Should we continue using CDNs for Video.js and Plotly, or move them to local web/vendor/ folders to fulfill the "offline build" requirement?
- **Logging Level:** Should we log every navigation event to the backend, or only errors and critical state changes?

---

## Verification Plan

### Automated Tests
- Run eel.report_spawn() to verify backend connectivity.
- Trigger a mock JS error to verify frontend_errors.log population.
- Execute window.runIntegrityCheck() in the console to verify DOM structure.

### Manual Verification
- Verify tab switching speed (should remain same or improve).
- Check MediaSession controls on a mobile or OS-level player.
- Inspect the DOM in DevTools to ensure no orphaned divs or duplicate IDs remain.
