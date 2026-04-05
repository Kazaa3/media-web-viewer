# Implementation Plan — Modular Recovery Architecture (v1.35.42)

## Overview
To satisfy the requirement for independent files and a control file, the diagnostic and recovery logic will be refactored into a modular "Recovery Engine." This separates data hydration (Stages) from UI verification (GUI Integrity), enabling flexible, testable, and maintainable diagnostics.

## Key Goals
- **Recovery Manager (Control File):**
  - `recovery_manager.js` orchestrates all diagnostic stages and integrity checks.
  - Acts as the central brain, enabling/disabling stages via registration.
- **Independent Stage Modules:**
  - `stages/missing_files.js`: Handles Stage 1 & 2 (Missing files, mock fallback).
  - `stages/real_assets.js`: Handles Stage 3 & 4 (Real media asset hydration).
- **GUI Integrity Module:**
  - `gui_integrity.js`: Manages the HUD overlay, MutationObserver, and CSS locks for persistent diagnostics.
- **Extensible Design:**
  - New modules (e.g., `library_diagnostics.js`) can be added by registering in the manager.

## Proposed Directory Structure
```
web/js/diagnostics/recovery_manager.js        # The Brain / Control File
web/js/diagnostics/gui_integrity.js           # The Eyes / HUD & Locks
web/js/diagnostics/stages/missing_files.js    # Stage 1 & 2
web/js/diagnostics/stages/real_assets.js      # Stage 3 & 4
```

## Registration Pattern
- Each stage module exports an `activate()` function.
- The manager imports and calls `activate()` for each enabled stage.
- GUI integrity runs independently and is always enabled.

## Expected Outcome
- Diagnostics are modular, testable, and easy to extend.
- Stages can be enabled/disabled by editing a single control file.
- GUI integrity checks (HUD, MutationObserver, CSS locks) are always active, regardless of data source.

---

*This plan enables robust, maintainable diagnostics and recovery for all future versions.*
