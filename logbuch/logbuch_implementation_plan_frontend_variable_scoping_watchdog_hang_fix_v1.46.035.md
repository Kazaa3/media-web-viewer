# Implementation Plan: Frontend Variable Scoping & Watchdog Hang Fix (v1.46.035)

## Purpose
Resolve fatal UI crash and [Boot-Watchdog] timeout caused by `Uncaught ReferenceError: CATEGORY_MAP is not defined` in `renderAudioQueue` (audioplayer.js). This error is due to improper scoping of global variables across scripts, leading to a broken rendering queue and startup hang.

## Key Issues
- **Watchdog Hang:** Frontend JS error prevents UI handshake with Eel, causing application hang.
- **Temporal Dead Zone (TDZ):** `let`-declared variables at the top level are not reliably exposed as globals.

## Proposed Changes

### [Frontend] web/js/common_helpers.js [MODIFY]
- Attach global registries explicitly to the `window` object:
  - `window.TECH_MAP = tech;`
  - `window.CATEGORY_MAP = CATEGORY_MAP;`

### [Frontend] web/js/audioplayer.js [MODIFY]
- Update `renderAudioQueue` to reference globals safely:
  ```javascript
  const catInfo = window.CATEGORY_MAP[window.activeQueueFilter] || { aliases: [] };
  const markers = window.TECH_MAP[window.activeQueueFilter] || [];
  ```

## Verification Plan
- **Automated Tests:**
  - N/A (frontend JS syntax only)
- **Manual Verification:**
  - Restart app and confirm [BOOT-WATCHDOG EXCEPTION] is resolved.
  - Library/queue renders without timing out `start_app()` orchestrator.

## Status
- User review required before implementation.
- Ensures robust global variable scoping and prevents startup hangs.
