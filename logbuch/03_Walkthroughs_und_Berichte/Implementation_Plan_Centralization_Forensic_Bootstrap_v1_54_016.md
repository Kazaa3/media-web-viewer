# Implementation Plan – Centralization & Forensic Bootstrap (v1.54.016)

## Objective
Centralize media queue configurations and implement a high-priority recovery sentinel to eliminate persistent "Wird geladen" (is loading) stalls.

---

## User Review Required

### IMPORTANT
- **Nuclear Bootstrap Sentinel:** Introduce an aggressive recovery mode that forcibly re-injects UI fragments if they fail to hydrate within 12 seconds. Ensures the app never remains stuck in a "Loading" state, even if the initial handshake fails.

---

## Proposed Changes

### [Component] Backend Orchestration (Python)
- **config_master.py**
  - Centralize Queues: Add a `queues` registry to `GLOBAL_CONFIG`.
  - Navigation Sync: Add "All Formats" to the media `level_2` navigation.
  - Protocol: Standardize item filtering logic based on centralized categories.

### [Component] Frontend Recovery & Sentinel (JS)
- **app_core.js**
  - [NEW] `initNuclearBootstrapSentinel()`: Watchdog that scans for stalled hydration nodes.
  - Recovery Pulse: Implement `forceNuclearHydration(targetId, fragmentPath)` using cache-busting techniques.
- **audioplayer.js**
  - Mixed Discovery: Update `renderAudioQueue` to support the `all` filter without type-pruning video items.
  - Config Injection: Pull discovery rules from `window.CONFIG.queues`.
- **shell_master.html**
  - Version HUD: Correct the hardcoded version in the footer to match the current iteration.
  - Safety Markers: Add data-attributes to track the current bootstrap phase.

---

## Open Questions
- Should the "Nuclear Pulse" also trigger a backend process restart, or should it remain frontend-only for the first attempt?

---

## Verification Plan

### Automated Tests
- `startup_auditor.py`: Ensure config centralization hasn't introduced regression.
- Manual DOM Check: Trigger a simulated hydration failure and verify the Sentinel recovers the view within the timeout window.

### Manual Verification
- Navigate across all categories and verify that the "All Formats" queue shows mixed media.
- Confirm that the "Loading" stalls are automatically resolved by the sentinel.
