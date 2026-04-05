# [RECOVERY PLAN] Lifecycle Visibility & Data Flow Hardening (v1.35)

## Problem Statement
The application is experiencing a "Black Screen" due to a `ReferenceError: initActions is not defined`. This occurred because the navigation initialization map was localized, breaking access for internal fragment scripts. The plan is to restore visibility and implement the promised data-flow tracing.

---

## User Review Required
**IMPORTANT**

All Initialization Actions will be moved to a global registry (`mwv_init_registry`). This ensures that regardless of how a fragment is loaded (via navigation or automatic sync), the required setup logic (Library loading, Queue rendering) is globally accessible and traceable.

---

## Proposed Changes

### 1. Lifecycle Visibility Restoration
- **Fix the ReferenceError** that is currently stalling the UI initialization.
- **[MODIFY] `ui_nav_helpers.js`**
    - Move the `initActions` object out of `finishSwitchTab` and declare it at the top-level as `window.mwv_init_actions`.
    - Update `finishSwitchTab` to reference this global registry.
    - Add exhaustive logging to the registry execution to track "init success" for every tab.

### 2. Data Flow Tracing (As Planned)
- **Diagnose why items are missing even when the UI is stable.**
- **[MODIFY] `bibliothek.js`**
    - Instrumentalize `renderLibrary` with `mwv_trace_render`.
    - Log the counts of Raw Items vs Filtered Items.
- **[MODIFY] `audioplayer.js`**
    - Instrumentalize `renderPlaylist` and `syncQueueWithLibrary` with `mwv_trace_render`.

### 3. Presence Watchdog
- **Implement an automated report for "Empty UI" states.**
- **[MODIFY] `app_core.js`**
    - Implement a post-load check that audits the DOM for media elements and logs a `DATA-VACUUM` alarm if the Library remains empty for more than 3 seconds after boot.

---

## Open Questions
- **Fragment Collision:** Are multiple fragments trying to use `initActions` simultaneously? The global registry will solve this.

---

## Verification Plan

### Automated Tests
- **Log Probe:** Verify that `logs/app.log` no longer contains the `ReferenceError: initActions is not defined` string.
- **Rendering Audit:** Run `tests/ui/headless_audit_v135.sh` and expect `Data Flow: > 0 items rendered`.

### Manual Verification
- Boot the app.
- Observe the Player Tab.
- Confirm that the default song/queue is rendered.

---

**[Artifact: implementation_plan]**
ArtifactMetadata: ArtifactType: implementation_plan  
RequestFeedback: true  
Summary: Lifecycle and data-flow recovery plan to fix the ReferenceError and trace library items from the database to the UI.
