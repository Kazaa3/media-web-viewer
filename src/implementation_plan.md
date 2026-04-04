# Implementation Plan - Logbuch Restoration and v1.34 Standardization

## Review Outcome

Status: Approved with minor adjustments.

### Approved Scope
- Branding refinement to title `dict`.
- Version standardization to `v1.34`.
- Redirect `Logbuch` navigation to the markdown-based Journal panel.
- Deep-dark glassmorphic Journal UI.
- Premium action styling for `Sync` and `New Entry`.

### Minor Adjustments
1. Keep the migration split into small, verifiable commits per phase to reduce regression risk in sidebar navigation.
2. Validate title changes in both document title and visible shell headings to avoid branding mismatch.
3. Keep Journal route fallback-safe: if fragment loading fails, show a non-blocking error and preserve current tab.

---

## Restoration Highlights

- **Branding Refinement:** Standardize application title as `dict` and all visible version identifiers as `v1.34`.
- **Journal Restoration:** Redirect `Logbuch` from system-log behavior to markdown Journal behavior.
- **Modernized Interface:** Convert Journal UI to deep-dark glassmorphic design using Inter (UI) and JetBrains Mono (metadata).
- **Premium Actions:** Upgrade `Sync` and `New Entry` controls to premium pill-style action components.

---

## Execution Checklist

### [x] Phase 1: Branding and Versioning
- [x] Update `web/app.html` with title `dict` and version `v1.34`.
- [x] Update `web/fragments/options_panel.html` version badge.

### [ ] Phase 2: Logbook (Journal) Restoration
- [ ] Update `web/js/ui_nav_helpers.js` to redirect `logbuch` to `logbook_panel.html`.
- [ ] Modernize `web/fragments/logbook_panel.html` with glassmorphism and deep-dark styles.

### [ ] Phase 3: JavaScript Refinement
- [ ] Update `web/js/logbook_helpers.js` for premium list items and rounded buttons.
- [ ] Ensure status icons align with the v1.34 design system.

### [ ] Phase 4: Verification and Polish
- [ ] Test sidebar navigation and fragment loading.
- [ ] Verify markdown rendering and editor functionality.

---

## Verification Notes

Manual checks to run after implementation:
1. Sidebar: `Logbuch` opens the markdown journal panel reliably.
2. Rendering: Entry list loads and markdown preview renders in dark theme.
3. Editor: `New Entry` opens editor modal and save flow still works.
4. Branding: Title and all version badges display `dict` and `v1.34` consistently.

---

## Latest Update (1 April 2026)

User-reported final adjustments completed:
- Hamburger menu moved into the top header (next to theme toggle).
- Startup auto-scan added for empty libraries (`/media` initial discovery).
- UI terminology standardized from "Items" to:
	- "Titel" in player, queue, and playlists.
	- "Medien / Mediathek" in counts and management views.

Recommendation: keep the manual verification checklist above as the final acceptance gate before closing all remaining phases.

---

## Automated Playback Testing Suite Plan (Playwright/DOM)

### Review Outcome
Status: Approved to proceed.

### Objective
Create a dedicated diagnostic tool that automatically opens the app in an isolated browser window, starts playback from the first available Titel in queue, and validates playback state via DOM assertions.

### Proposed Implementation
- Add new script: tests/ui/playback_verify.py
- Use existing Playwright environment in ./venv_selenium
- Launch browser in standalone mode (separate window/session)
- Wait for app readiness and queue visibility
- Select first available Titel and trigger playback
- Assert playback state in DOM (for example Playing status, active player class, or transport-state indicator)
- Emit structured result (PASS/FAIL) with failure reason and timestamp

### Execution Flow
1. Start target app URL.
2. Wait for primary shell + queue container.
3. Detect first playable Titel row.
4. Trigger click/play action.
5. Poll DOM for playback state transition within timeout.
6. Return PASS on confirmed playback, otherwise FAIL with diagnostics.

### Acceptance Criteria
- Script exits 0 on successful playback verification.
- Script exits non-zero on timeout or DOM mismatch.
- Output includes key checkpoints: app loaded, Titel found, play triggered, status observed.
- Runs in an isolated browser context independent from manually opened pages.

### Risks and Safeguards
- If queue is empty, report SKIP/FAIL with explicit message instead of false PASS.
- Use resilient selectors (data attributes preferred) to reduce flakiness.
- Include retry window for delayed media initialization.

### Next Action
Proceed with implementation and run one baseline diagnostic pass after script creation.

---

## Latest Update (Navigation Restoration & Logging)

Completed items reported:
- Restored sidebar tabs: `Edit`, `Reporting`, `Debug & DB`, `Testing`.
- Activated Library domain navigation for `Mediathek`, `Dateibrowser`, and `Inventar`.
- Added backend/frontend trace flow via `log_gui_event` and `mwv_trace`.
- Mirrored browser console output into the Playwright diagnostic stream.
- Fixed Library shorthand-navigation overwrite so domain switches no longer fall back to `Visual` unintentionally.

Reported verification outcome:
- Sidebar categories reachable.
- Library domains switch correctly.
- Server logs and automated browser diagnostics confirm the navigation fix.

---

## Latest Update (Menu Entry Restoration & Dynamic Sub-Navigation)

Completed items reported:
- Restored the missing top-menu entries `Reporting` and `System Test` in the toggleable program menu.
- Expanded the top menu so it mirrors all primary sidebar categories:
	- `Editor`
	- `Core Tools`
	- `Reporting`
	- `System Test`
- Added a global, dynamic sub-navigation bar below the main header.
- Enabled category-based sub-navigation groups for:
	- `Reporting`: `Dashboard`, `DB Stats`, `Video Health`, `Parser Hub`
	- `Tests`: `System Health`, `Debug DB`, `Latency Profile`
	- `Media`: `Audio Player`, `Library Browser`, `Playlists`
	- `Edit`: `Metadata Tags`, `Artwork Lab`, `Media Analysis`
- Added automatic active-state tracking for the new sub-navigation pills.
- Standardized the visual treatment of the new bar to the v1.34 glassmorphic design system.

Affected implementation files:
- `app.html`
- `ui_nav_helpers.js`
- `main.css`

Reported verification outcome:
- `Alt` toggles the program menu and exposes the restored entries.
- Selecting `Reporting` or `System Test` reveals the matching sub-navigation pills.
- Sub-module switching keeps the active state synchronized.
- `Editor` and `Tools` also populate the sub-navigation correctly.
