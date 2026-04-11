# Diagnostics Sidebar Restoration & Enhancement (v1.37.09)

## Context
A regression occurred where the diagnostics sidebar was reduced to only the two new tabs (Hydration Chain, Item Track), removing the original suite of diagnostic tools. This plan documents the restoration and enhancement process.

## Restoration & Enhancement Plan

### 1. Full Sidebar Restoration
- **Restore all original tabs:**
  - Overview (reiter-overview)
  - Tests (reiter-tests)
  - Video Health (reiter-video-health)
  - Logs (reiter-logs)
  - Latency (reiter-latency)
  - Recovery (reiter-recovery)
- **Persistent Layout:**
  - All recovery/action buttons (Force Sync, Deep Scan, etc.) are restored to their original sidebar locations.

### 2. Integrated Expansion
- **Hydration Chain** and **Item Track** are retained as new, additional diagnostic tabs.
- The sidebar now offers a "Swiss Army" suite: all legacy diagnostics plus the new deep-dive tools.

### 3. Navigation Logic
- **js/ui_nav_helpers.js:**
  - `switchDiagnosticsSidebarTab` is updated to support both legacy and new tabs seamlessly.
  - Tab switching and state persistence are verified for all modules.

## Verification
- All tabs are visible and functional in the diagnostics sidebar.
- Recovery and action buttons are present and working.
- Hydration Chain and Item Track are accessible as new tabs.

---

**Date:** 2026-04-06
**Author:** GitHub Copilot
