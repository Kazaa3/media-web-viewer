# Logbuch: Global Sidebar & Viewport Consolidation (v1.46.02) – Implementation Plan

## Overview
This plan details the structural realignment of the Forensic Workstation to support a persistent global sidebar and resolve visibility issues with the modern Atomic Player.

---

## Key Changes & Proposed Steps

### 1. Global Shell Reconstruction
- **app.html:**
  - Relocate `#rebuild-stage` into `#main-content-area`.
  - Insert new `#global-lib-sidebar` container and `#global-lib-splitter` as first children of `#main-content-area`.
  - Apply flex styling to ensure sidebar offsets main content correctly.

### 2. UI Orchestration Refactoring
- **ui_nav_helpers.js:**
  - Update `toggleLibrarySidebar` to target `#global-lib-sidebar`.
  - Update `renderLibrarySidebar` to populate the global container.
  - Ensure sidebar visibility state syncs with the top-right toggle button.

### 3. Window Management Sync
- **window_manager.js:**
  - Update `_hideAllShells` logic to include relocated `#rebuild-stage`.
  - Verify activation pulses display the unified stage in its new layout context.

### 4. Fragment Cleanup
- **library_explorer.html:**
  - Remove redundant sidebar HTML to prevent ID collisions and simplify DOM.

---

## Open Questions
- **Sidebar Visibility per Category:** Should the sidebar auto-hide for technical categories (Parser, Report) or persist if toggled on? (Default: keep user choice/persistent.)

---

## Verification Plan

### Automated Tests
- **No Selenium/Playwright:** Manual verification only.

### Manual Verification
- Toggle forensic sidebar using top-right button and verify persistence.
- Switch to "Music Player" and confirm "Sonic Core" player is centered.
- Ensure sidebar remains visible (if toggled on) when navigating categories.
- Check console for "element not found" warnings from `renderLibrarySidebar`.

---

**Awaiting user input on sidebar auto-hide for technical categories before implementation.**
