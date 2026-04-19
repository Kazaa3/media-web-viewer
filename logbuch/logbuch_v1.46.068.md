# Logbuch: Layout Hygiene & System Identity Sync (v1.46.067)

## Date: 2026-04-18

---

## Implementation Plan

### Scrollbar Lockdown
- Enforced a "One-Scroll" policy:
  - Set `overflow: hidden !important;` on both `<html>` and `<body>` in `main.css`.
  - Ensured main layout containers use `height: 100%` and only internal content areas are scrollable.
  - This eliminates redundant browser scrollbars, leaving only the intended media list scrollbar visible.

### Dynamic Versioning
- Removed the hardcoded `data-mwv-version` attribute from `<body>` in `app.html`.
- Updated `app_core.js` to set `document.body.setAttribute('data-mwv-version', config.version)` dynamically as soon as the configuration is received from the backend.

---

## Verification Plan
- **Visual Audit:** Confirm only one professional scrollbar is visible on the right when scrolling the library.
- **Inspect DOM:** Verify `<body>` correctly reflects the current version (e.g., 1.46.066) in the browser console.

---

## Status
- [x] Scrollbar lockdown complete
- [x] Dynamic versioning implemented
- [ ] Manual verification pending

---

## Notes
- These changes ensure a clean, professional UI with a single-scroll experience and accurate, dynamic system identity.
- Awaiting user review and manual verification.
