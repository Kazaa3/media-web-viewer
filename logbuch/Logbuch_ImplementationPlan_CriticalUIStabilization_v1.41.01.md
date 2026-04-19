# Implementation Plan – v1.41.01 Critical UI Stabilization

This plan addresses three critical regressions: the "black window" (hidden content), misaligned header icons, and missing sub-menus.

---

## User Review Required
**CAUTION**
- **Inline Style Overrides:** I identified that hardcoded `style="display: none"` on tab containers is overriding the new CSS-based orchestration. I will remove these inline styles to let the active class safely manage visibility.

**IMPORTANT**
- **Flexbox Restoration:** I will enable `display: flex` on the main header to ensure the "Mega-Nav" is correctly partitioned between the left buttons and the right icon cluster.

---

## Proposed Changes

### UI Geometry & Alignment
- **[MODIFY] app.html**
  - **Header:** Add `display: flex !important` to `#master-persistent-header` to restore the "Between" layout.
  - **Sub-Nav:** Update `#sub-nav-container` to use `height: var(--active-sub-nav-height)` instead of the static height, allowing the Orchestrator to hide it completely when not needed.
  - **Content Visibility:** Remove `style="display: none;"` from all `.tab-content` elements. This is the primary cause of the "Black Screen".

### Orchestration Logic
- **[MODIFY] ui_core.js**
  - Ensure `updateGeometry()` is called after a category switch to re-align the viewport instantly.

---

## Open Questions
None. These are foundational fixes for regressions.

---

## Verification Plan

### Manual Verification
- **Header:** Verify "dict" is on the far left and the icon cluster (Pulsar, Split, Trash) is on the far right.
- **Sub-Nav:** Verify the second row (pills) appears when clicking "Player".
- **Black Screen:** Verify the content (e.g., Library Browser) is visible when selecting it.
