# Implementation Plan: Technical Status HUD & PID Pills Restoration (v1.37.11)

## Elite Status Restoration

### Goals
- Restore all technical observability layers (PID, Boot, Uptime, FE/BE/DB clusters, health modals) without removing any new modular overlay features.
- Ensure all status indicators are always accessible, non-intrusive, and visually integrated.

---

## Implementation Steps

- **[ ] Add Status Button to app.html header**
  - Dedicated button in the top-right header toggles the floating Mini-HUD.
- **[ ] Merge PID/BOOT/UP Pills into a floating header HUD**
  - Compact, always-accessible pills for PID, Boot, and Uptime.
- **[ ] Merge Swiss HUD clusters (FE/BE/DB) into the unified footer**
  - Status lights for Frontend, Backend, and Database are always visible, merged into the player footer.
- **[ ] Re-enable status notifications for Item DB health**
  - Restore and verify all modal feedback for system integrity and Item DB health checks.

---

## Execution Principle
- **"Nur ergänzen und nichts entfernen":** Only add or restore features—no removals or regressions.

---

## Next Steps
- Begin immediate restoration of all technical HUD and modal features as outlined.

**Date:** 2026-04-06
**Author:** GitHub Copilot
