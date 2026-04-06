# Implementation Plan — Navigation & Aesthetic Stabilization (v1.36.00)

This plan addresses feedback on the aesthetic and reliability of the navigation for Media Viewer v1.36.00.

## Highlights

- **Reliable Sidebar Toggle:**
    - Replace inline-style manipulation with a robust CSS-class system (`.sidebar-collapsed`).
    - Ensures smooth, buttery, and state-persistent transitions every time you click the pulsar.

- **Beautiful "Dock" Footer:**
    - Transform the footer into an iPad-inspired glassmorphic Dock.
    - Minimalist, centered, and premium look.

- **Sync Status LED:**
    - Add a pulsating LED indicator immediately before the Sync button.
    - Provides immediate visual feedback on the data pipeline health.

- **Clarified Terminology:**
    - Rename technical labels in the side-panel to **Stored** (Database rows) and **Displayed** (Items currently filtered and rendered).
    - Makes diagnostic data easier to interpret for all users.

## Next Steps

Please review and approve this stabilization plan to begin execution.
