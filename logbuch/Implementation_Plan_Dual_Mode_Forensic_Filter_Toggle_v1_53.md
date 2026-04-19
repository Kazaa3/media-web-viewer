# Implementation Plan: Dual-Mode Forensic Filter Toggle (v1.53)

This plan implements a high-fidelity toggle system for the media library, allowing operators to switch between Technical Media Routes and Contextual Object Categories with a clear, hierarchical UI.

---

## 1. Problem Statement

- Operators need to filter the media library by both technical route and contextual category.
- UI must support hierarchical, content-aware groupings while remaining compatible with standard HTML selects.

---

## 2. Proposed Changes

### Configuration SSOT
- **[MODIFY] `config_master.py`**
  - Define `LIBRARY_FILTER_MODES`:
    - **Route Mode:** `all`, `audio_native`, `audio_transcode`, `video_native`, `video_transcode`, `iso_image`, `bilder`
    - **Category Mode:** `all`, `audio` (Header), `album`, `single`, `hörbuch`, `soundtrack`, `video` (Header), `series`, `documentation`

### UI Integration
- **[MODIFY] `player_queue.html`**
  - Inject the Mode Toggle Button next to the queue-type-filter dropdown.
  - Implement `toggleLibraryFilterMode()` to cycle between ROUTE and CATEGORY states.
  - Ensure aesthetic sync with existing tab-btn styling for "Forensic Elite" consistency.

### Logic Orchestration
- **[MODIFY] `app_core.js`**
  - Update `hydrateCategoryDropdown(branchId)` to be state-aware.
  - Implement hierarchical label rendering: In category mode, prepend non-parent items with `↳` or `  -` to denote sub-category status.

---

## 3. Verification Plan

### Automated UI Test
- Trigger the toggle button and verify that the dropdown's innerHTML updates correctly between technical and contextual sets.
- Select a sub-category (e.g., Hörbuch) and verify that the library re-syncs based on that specific filter ID.

### Manual Verification
- Review the aesthetic alignment of the new toggle button in the gallery header.
- Confirm that the current selection is gracefully handled when switching modes (falling back to 'ALL' if the previous selection is invalid in the new mode).

---

## 4. User Review Required

- Confirm that the hierarchical filter mode is intuitive and visually clear.
- Validate that all technical and contextual filters are correctly defined and functional.

---

**Status:**
- Pending implementation and review.
- This plan ensures the media library is filterable by both technical route and contextual category, with a professional, user-friendly UI.
