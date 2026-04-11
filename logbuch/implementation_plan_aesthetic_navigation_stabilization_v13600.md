# Media Viewer v1.36.01 — Finalized Hybrid Technical Footer

The Hybrid Technical Footer for v1.36.01 is finalized, restoring high-resolution visibility while removing previous overload.

## Final Hybrid Layout

- **Restored Diagnostic Transparency:**
    - The footer center now shows the full triple-parity anchor using the new terminology: `[FS: -- | Stored: 541 | Displayed: 541]`.
- **Persistent Action Cluster:**
    - The Pulsing LED, SYNC button, and LOGS toggle are all available in the right-hand footer cluster for immediate developer access.
- **De-cluttered Interface:**
    - The FLAGS (System Flags) button is now in the Technical Sidebar (Diagnostics tab), keeping the main bar focused on live status while deep-dive controls are one click away.
- **Professional "Dock" Aesthetic:**
    - The centered glassmorphic pill remains, providing a sleek, iPad-inspired home for the restored diagnostic data.

The full visual summary is available in the updated `walkthrough.md`. The interface now perfectly balances technical transparency with a premium, uncluttered design.
# Implementation Plan — Aesthetic & Navigation Stabilization (v1.36.00)

This plan focuses on making the Media Viewer's diagnostic and navigation systems feel professional, reliable, and aesthetically premium. We are moving from "functional debug blocks" to a "polished technical cockpit."

## User Review Required

**IMPORTANT**

- **Footer Uplift: The "Dock" Console**
    - Redesign the footer into a segmented "Dock":
        - **Left:** App Version & Title.
        - **Center:** Minimalist DB Count (e.g., `DB: 541`).
        - **Right:** Action buttons featuring a new Sync LED (Green/Pulse) immediately before the Sync button.

**TIP**

- **Clarified Terminology**
    - In the sidebar diagnostics, replace "GUI" and "DB" with clearer labels:
        - **Stored:** Items in the database
        - **Displayed:** Items currently filtered and rendered

## Proposed Changes

### Phase 1: CSS-Driven Sidebar Stabilization (`ui_nav_helpers.js` & `main.css`)
- **[MODIFY] main.css**
    - Define a `.sidebar-collapsed` class that handles `width: 0`, `opacity: 0`, and `visibility: hidden`.
    - Use `transition: all var(--transition-fluid)` for a buttery-smooth feel.
- **[MODIFY] ui_nav_helpers.js**
    - Update `toggleSidebar()` and `applySidebarState()` to simply toggle the class on the body or main container. This is significantly more reliable than inline style manipulation.

### Phase 2: Beautiful Footer & LED Status (`app.html`)
- **[MODIFY] app.html**
    - Flatten the footer structure.
    - Add `<div id="sync-led" class="led-pulse"></div>` before the SYNC button in the right cluster.
    - Simplify `footer-sync-anchor` to only show the DB count.
- **[MODIFY] main.css**
    - Style the Sync LED with a subtle pulse animation.
    - Polish the footer status area as a centered glassmorphic "Pill."

### Phase 3: Terminology & Data Sync (`diagnostics_helpers.js`)
- **[MODIFY] diagnostics_helpers.js**
    - Update sidebar labels:
        - **Stored** instead of DB.
        - **Displayed** instead of GUI.
    - Ensure the sync-led color reflects the data health (Green for healthy, Orange for filter drops, Red for empty/error).

## Open Questions
- **LED Location:** The LED will be placed before the sync button in the same flex-container group.
- **Pill Alignment:** Should the `DB: 541` count be centered in the footer or remain on the left? (Recommendation: center for a "Dock" feel).

## Verification Plan

### Automated Tests
- `python3 scripts/verify_ui_state.py`: Confirming the correct classes are toggled in the DOM.

### Manual Verification
- **Check Sidebar Toggle:** Click bottom right Pulsar → Sidebar should slide smoothly every time.
- **Check Footer LED:** Does it pulse green when synchronized?
- **Check Terminology:** Open Sidebar → Is it clear what "Stored" vs "Displayed" means?
