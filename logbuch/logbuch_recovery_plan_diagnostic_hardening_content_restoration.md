# RECOVERY PLAN: Diagnostic Hardening & Content Restoration

The interface is experiencing "Black Screen" regressions where fragments load (sub-nav visible) but main content containers remain hidden or empty. This plan implements exhaustive trace logging to the backend and fixes activation logic.

---

## Proposed Changes

### 1. Diagnostic Trace Routing
- **File:** trace_helpers.js
  - Add `mwv_trace_render(component, stage, metadata)` to capture DOM integrity checks.
  - Add `log_js_error(error, context)` to capture silent crashes within fragments.
- **File:** fragment_loader.js
  - Ensure every STAGE result (success or failure) is emitted as a backend trace.

### 2. Player View Restoration
- **File:** player_queue.html
  - Add `console.info` and `mwv_trace` in the <script> block to track when `switchPlayerInternalView` fires.
  - Implement a "Force Reveal" loop to ensure one view is ALWAYS displayed if the container is visible.

### 3. Navigation Lock Hardening
- **File:** ui_nav_helpers.js
  - Wrap `initActions` in a try...catch block.
  - Log every successful action in the initialization chain.
  - Ensure navigation lock is released even if a fragment script crashes.

---

## Open Questions
- Is the black screen persistent on every reload, or only after switching from another tab (e.g., Library)?
- Are there any global `!important` rules in main.css that might be hiding the `.player-view-container`?

---

## Verification Plan

### Automated Tests
- **Trace Audit:** Run the app and verify logs show `[FL] STAGE-4` followed by `[UI-RENDER] SUCCESS: warteschlange`.
- **Headless Probe:** Run a script to dump the computed style of `#player-view-warteschlange` to confirm it is `display: flex`.

### Manual Verification
- Click Player → Verify sub-nav and content (deck/queue) appear.
- Check logs/app.log for any `[JS-ERROR]` entries.

---

**ArtifactMetadata:**
- ArtifactType: implementation_plan
- RequestFeedback: true
- Summary: Recovery plan to resolve the "Black Screen" regression in the Player interface and implement exhaustive diagnostic logging routed to the backend for auditing.
