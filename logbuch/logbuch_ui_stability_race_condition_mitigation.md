# Implementation Plan - UI Stability & Race Condition Mitigation

Rapid user interaction ("clicking everywhere") has revealed race conditions in the navigation and fragment loading pipeline. This plan introduces strategic locks and guards to ensure UI structural integrity under load.

---

## Proposed Changes

### 1. Global Navigation Lock
- **File:** ui_nav_helpers.js
  - State Guard: Introduce `let isNavigating = false;`.
  - switchTab Hardening: At the start of `switchTab`, check `isNavigating`. If true, return (unless forced).
  - Completion Hook: Set `isNavigating = false` in `finishSwitchTab` after Stage 4 is confirmed.

### 2. FragmentLoader In-Flight Guard
- **File:** fragment_loader.js
  - Pending Map: Track `inFlightLoads` (TargetID -> Promise).
  - Redundancy Filter: If a load for the same targetId is already active, return the existing Promise instead of starting a new one.

### 3. Sub-Nav Click Safety
- **File:** ui_nav_helpers.js
  - Event Delegation: Ensure `updateGlobalSubNav` pills explicitly stop propagation or the parent `sub-nav-container` has a "no-op" click sink to prevent accidental category switches or layout shifts from background clicks.

---

## Open Questions
- Should we show a Spinner or Wait Cursor while the lock is active? (Recommendation: subtle CSS `cursor: wait` on the body.)

---

## Verification Plan

### Automated Tests
- Run `bash tests/ui/headless_audit_v135.sh` with a specific test for concurrent requests (if possible, otherwise confirm no regression).

### Manual Verification
- Rapidly click across Music, Library, and Video tabs.
- Confirm that the UI handles requests sequentially or ignores "flooding" clicks without screen corruption.
