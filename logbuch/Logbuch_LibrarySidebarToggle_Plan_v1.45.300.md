# Logbuch: Centralized Library Sidebar & Header Toggle (v1.45.300) – Implementation Plan

## Overview
This plan details the integration of the library sidebar into the central Python configuration engine and the addition of a dedicated toggle button in the top-right header cluster for granular UI control.

---

## Key Changes & Proposed Steps

### 1. Backend Configuration
- **config_master.py:**
  - Introduce `library_sidebar_orchestrator` registry.
  - Define `übersicht` items (Cinema, Series, Albums, etc.) and `ansichten` modes (Grid, Details, etc.).

### 2. Header UI Enhancement
- **app.html:**
  - Add a new round toggle button in the `secondary-cluster`.
  - Use a dedicated `sidebar-left` SVG icon.
  - Style to match the forensic icon set (pulsing effects, glassmorphic hover).

### 3. Navigation & State Management
- **ui_nav_helpers.js:**
  - Implement `toggleLibrarySidebar()` logic.
  - Persist sidebar state in `localStorage`.
  - Support automatic sidebar visibility based on tab switching (e.g., auto-show in Library mode).

### 4. Fragment Refactoring
- **library_explorer.html:**
  - Update sidebar container for configuration-driven rendering.
  - Add CSS transitions for smooth open/close.

---

## Open Questions
- **Sidebar Persistence:** Should the sidebar remember its state (open/closed) globally, or reset when switching between 'Audio' and 'Multimedia' branches?

---

## Verification Plan

### Automated Tests
- Verify that `library_sidebar_orchestrator` is correctly retrieved during frontend boot.
- Use browser tool to toggle sidebar and confirm visibility state in the DOM.

### Manual Verification
- Confirm new toggle button shows/hides the library sidebar.
- Verify clicking sidebar items triggers expected view changes (e.g., switching to 'Grid').

---

**Awaiting user input on sidebar persistence before implementation.**
