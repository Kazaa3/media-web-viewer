# v1.37.32 GUI Performance Audit: DOM & Rendering Decathlon

## Overview
This release introduces a professional-grade Performance (PER) tab in the diagnostics sidebar, providing deep observability into frontend rendering logic, DOM node counts, and technical asset distribution. This completes the "Decathlon" of the forensic cockpit, enabling instant access to real-time rendering latency (ms) and DOM health reports.

---

## Key Features
- **Performance Tab (PER):**
  - Added to diagnostics_sidebar.html navigation.
  - High-density [GUI PERFORMANCE FORENSICS] viewport.
  - Chromatic load meters for DOM bloat and latency.

- **Library Renderer Instrumentation:**
  - `bibliothek.js`: `renderLibrary()` now uses precision timers (`performance.now()`).
  - Exports `window.__mwv_last_render_ms` for forensic auditing.

- **Controller Aggregation:**
  - `sidebar_controller.js`: Implements `runPerformanceAudit()`.
  - Counts total DOM nodes, measures image load density, and reports renderer latency.
  - Tab mapping updated to include PER domain.

---

## Implementation Details
- **bibliothek.js**
  - Instrument `renderLibrary()`:
    - Capture `performance.now()` at start and end.
    - Update `window.__mwv_last_render_ms`.

- **diagnostics_sidebar.html**
  - Add PER to tab navigation.
  - Add GUI PERFORMANCE FORENSICS viewport.
  - Render chromatic meters for DOM bloat/latency.

- **sidebar_controller.js**
  - Implement `runPerformanceAudit()`:
    - Count DOM nodes (non-blocking).
    - Measure image load density.
    - Report renderer latency.
    - Update tab mapping.

---

## Verification Plan
- **Automated Tests:**
  - Verify `renderLibrary` latency tracking updates global state.
  - Confirm DOM node counting is accurate and non-blocking.
- **Manual Verification:**
  - Navigate to PER tab; verify meters update correctly.
  - Inspect SENTINEL trace for results.

---

## Open Questions
- Should a "DOM Stress Test" (injecting 1000 dummy items) be included? (Recommendation: Keep v1.37.31 observational for stability.)

---

## Status
- **User Review Required**
- **Technical Agility:** Ensures workstation responsiveness regardless of library size.

---

*See also: v1.37.30 Storage Forensic Audit (COMPLETED)*
