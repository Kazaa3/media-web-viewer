# Implementation Plan - Trace Routing & Navigation Hardening

UI instability and "Black Screen" issues are linked to navigation deadlocks and silent fragment loading failures. This plan routes all confirmation logs to the backend and implements a 5-second navigation safety timeout to prevent deadlocks.

---

## Proposed Changes

### 1. Unified Log Routing
- **File:** fragment_loader.js
  - Replace `console.info([FL] STAGE X...)` with `mwv_trace('FRAGMENT', 'STAGE-X', { path, targetId })` to ensure all stages are logged in the Python backend and diagnostic audits.

### 2. Navigation Safety (Deadlock Prevention)
- **File:** ui_nav_helpers.js
  - Safety Timeout: When setting `isNavigating = true` in `switchTab`, also start a `setTimeout` (5000ms). If the lock isn't released by `finishSwitchTab` within 5s:
    - Release the lock (`isNavigating = false`).
    - Reset the cursor to default.
    - Log a `[TIMEOUT] Navigation deadlocked` warning to the backend.
  - Button IDs: Assign formal IDs to Top-Nav buttons in app.html if missing (e.g., `id="nav-btn-library"`).

### 3. Error State Hardening
- **File:** fragment_loader.js
  - Ensure the `error()` method also releases the global `isNavigating` lock so a failed load doesn't lock the user out.

---

## Open Questions
- Should a "Reset UI" emergency button be added to the header if a deadlock is detected? (The 5s timeout should solve this automatically.)

---

## Verification Plan

### Automated Tests
- Run the audit and confirm `[FRAGMENT] [STAGE-4]` now appears in the backend output (check via `tail logs/app.log`).

### Manual Verification
- Rapidly click across tabs to trigger the lock.
- Disconnect the network or use a non-existent fragment to verify the 5s timeout releases the UI.
