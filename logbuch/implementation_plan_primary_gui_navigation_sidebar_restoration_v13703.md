# Media Viewer v1.37.03 — Primary GUI Navigation & Recovery Suite Finalized

The Primary GUI Navigation & Recovery Suite (v1.37.03) is now finalized, providing the high-density "Swiss Army" center for technical observability and system stability.

## Final Technical Configuration

- **Main Sidebar Toggle Restoration:**
    - The critical Side Menu (Square Icon) toggle is re-integrated into the bottom-right footer cluster, correctly triggering the primary split-layout media navigation sidebar.
- **Multi-Tabbed Technical Sidebar (Left):**
    - Diagnostics sidebar is now a professional 4-tabbed "Reiter" system for high-observability technical work:
        - **Details:** Real-time media file metadata and parser metrics.
        - **Health (Technical):** 7-point technical HUD analytics, system health LEDs, and persistent PID/Boot tracking.
        - **Recovery (Emergency):** Mission-control suite to solve the "0 Item" bug. Use CLEAR ALL FILTERS or DEEP SYNC to re-hydrate the media library if it enters an empty "Black Hole" state.
        - **Tools (Environment):** Options for refreshing startup duration and re-exposing backend environment variables.
- **Final Icon Progression:**
    - Footer cluster now features the finalized, logical sequence: Details → Sidebar (Main) → Theme → Grid → Program Menu → Technical Pulsar (Diagnostics).

The final diagnostic summary and visual documentation are available in the updated `walkthrough.md`. The technical environment is now fully synchronized, observable, and recoverable.
# Implementation Plan — Primary GUI Navigation & Sidebar Restoration (v1.37.03)

This plan restores the critical "Side Menu" (Main Sidebar) toggle button to the bottom-right footer cluster and enhances the Technical Sidebar with the requested diagnostics.

## User Review Required

**IMPORTANT**

- **Navigation Cluster Restoration:**
    - Re-integrate the `toggleSidebar()` command (Main Sidebar) into the bottom-right footer cluster.

- **Multi-Tabbed Technical Sidebar (Left):**
    - Diagnostics Sidebar will feature a tabbed 'Reiter' system for high-density navigation:
        - **Health (Technical):** 7-point HUD analytics, PID tracking, LEDs.
        - **Recovery (Emergency):** Tools for "0 item" problem (Reset Filters, Sync Force, Library Purge).
        - **Media Tools:** Advanced media manipulation and environment options.

## Proposed Changes

### Phase 1: Footer Navigation Restoration (`app.html`)
- **[MODIFY] app.html**
    - Restore the `toggleSidebar()` button (Square icon) to the bottom-right icon cluster.
    - Ensure proper ordering: Details → Sidebar → Theme → Grid → Menu → Pulsar (Diag).

### Phase 2: Technical Sidebar Enhancement (`app.html` & `diagnostics_helpers.js`)
- **[MODIFY] app.html**
    - Add a new "STARTUP & ENVIRONMENT" section to the `sidebar-view-diagnostics` tab.
    - Include a "GUI Refresh" button within this section (mirroring the FE RESET from the footer).
- **[MODIFY] diagnostics_helpers.js**
    - Ensure `refreshStartupInfo()` populates the new sidebar section in addition to the footer pill.

### Phase 3: Visual Polish (`main.css`)
- **[MODIFY] main.css**
    - Refine the sidebar diagnostic styling for the new sections.
    - Ensure the right-hand footer icons are perfectly aligned and legible.

## Open Questions
- **Icon Order:** Sidebar Toggle (Square) will be placed before the Burger Menu for more frequent split-view action.
- **Startup Display:** Sidebar will show formatted strings (not full Boot JSON) for clarity.

## Verification Plan

### Manual Verification
- Click Bottom-Right "Square" Icon: Does the main sidebar toggle?
- Click Bottom-Right "Pulsar" Icon: Does the diagnostics sidebar toggle and show the new "Startup & Environment" sections?
- Confirm Sync: Does the footer HUD (FE, BE, DB) still show its 7-point metrics on hover?
# Implementation Plan — Primary GUI Navigation & Sidebar Restoration (v1.37.03)

This plan addresses feedback for v1.37.03, focusing on navigation clarity and sidebar observability.

## Key Restoration Actions

- **Sidebar Toggle Restoration:**
    - Re-integrate the `toggleSidebar()` command ("Square with vertical line" icon) into the bottom-right footer cluster, correcting the previous omission.

- **Diagnostics Enhancement:**
    - Add dedicated sections for Startup Analytics (Boot/PID) and Environment Options directly into the left-aligned technical sidebar for high-observability "options".

- **Correct Icon Order:**
    - Footer cluster will now feature a logical progression:
        - Media Info → Main Sidebar (Standard) → Theme → Grid → Program Menu → Technical Pulsar (Diagnostics)

## Next Steps

Please review and approve these navigation fixes to proceed with implementation.
