# Restoration Plan: Technical Status HUD & Modals (v1.37.11)

## Overview
To address the accidental removal of high-density technical status pills and Item-DB recovery modals, this plan restores all essential technical HUD elements and modals, ensuring no loss of observability or recovery features.

---

## 🛠️ Restoration Steps

### 1. Top-Right Status HUD
- **Status Button:** Add a new button to the top-right header.
- **Mini-HUD:** Clicking the button toggles a compact overlay showing PID, Boot, and Uptime pills—always accessible, never cluttering player controls.

### 2. Universal HUD Restoration
- **Swiss HUD Clusters:** Re-integrate FE/BE/DB status lights into the unified footer, ensuring proper layout and no overlap with player controls.

### 3. Modal Reactivation
- **Item DB / Health Modals:**
  - Verify and restore the pop-up modals for Item DB and Health checks in diagnostics_helpers.js and app.html.
  - Ensure they trigger correctly on relevant system events.

---

## Implementation Principle
- **"Nur ergänzen und nichts entfernen":** All technical tools are layered back in without removing or hiding any existing features.

---

**Date:** 2026-04-06
**Author:** GitHub Copilot
