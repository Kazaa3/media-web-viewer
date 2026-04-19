# Logbuch: Atomic UI Stabilization (v1.46.01) – Implementation Plan

## Overview
This plan outlines the final resolution for the "Black Fragment" UI failure by hardening the loadAtomic engine and enforcing the forensic liveness protocol across all fragments.

---

## Key Changes & Proposed Steps

### 1. Core Framework Hardening
- **fragment_loader.js:**
  - Upgrade `loadAtomic` to include script extraction and execution logic.
  - Implement a `waitForLiveness` polling loop (max 3s) that inspects the shadow buffer.
  - Perform the `innerHTML` swap ONLY when liveness is achieved or a timeout occurs.
  - Add detailed `mwv_trace` logging for each atomic stage.

### 2. Fragment Forensic Audit
- **library_explorer.html:**
  - Add `data-liveness="ready"` to the root container.
  - Ensure the `init()` script explicitly sets this attribute after dynamic sidebar rendering.
- **audioplayer.html:**
  - Add `data-liveness="ready"` to the root atomic shell.
  - Ensure audio engine initialization sets the liveness marker.

### 3. Sentinel Optimization
- **visibility_sentinel.js:**
  - Refine audit logic to be less aggressive during active atomic transitions.
  - Improve diagnostic logging to distinguish "Missing Attribute" vs "Empty Fragment" failures.

---

## Open Questions
- **Timeout Failover:** If a fragment fails to reach "Ready" state in the shadow buffer within 3 seconds, should a "Diagnostics Required" placeholder be shown or should a legacy reload be attempted?

---

## Verification Plan

### Automated Tests
- **No Selenium/Playwright:** Verification will be done via manual inspection and `mwv_trace` log analysis.

### Manual Verification
- Navigate through all tabs (Audio, Multimedia, Extended) and verify smooth fragment transitions without "black hole" flickering.
- Inspect browser console for `[FL] ATOMIC SWAP: SUCCESS` logs.
- Verify that the VisibilitySentinel does not trigger unnecessary rescues during normal navigation.

---

**Awaiting user input on timeout failover strategy before implementation.**
