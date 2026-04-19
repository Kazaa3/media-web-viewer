# Implementation Plan - Forensic Boot Guard & 5-Mode Navigation (v1.53.003)

This plan resolves the pyautogui startup crash and expands the library navigation to support five independent filtering modes: Route, Category, Items, Objects, and Context.

---

## 1. Boot Sequence Stabilization
- **[MODIFY] `main.py`**
  - Import `src.core.startup_auditor` directly after path injection.
  - Execute `startup_auditor.run_audit()` before importing `api_diagnostics`.
  - Ensures missing packages like pyautogui are installed before any other module attempts to import them, preventing `ModuleNotFoundError`.

---

## 2. Taxonomy Expansion (v1.53.003)
- **[MODIFY] `config_master.py`**
  - Expand `library_filter_mode_registry` to include all 5 modes:
    - ROUTE (Technical Pipelines)
    - CATEGORY (General Forensic Groups)
    - ITEMS (Technical File Units: audio, video, bilder, zip, ebooks, dokumente, iso image)
    - OBJECTS (Semantic Entities: album, film, serie, hörbuch, doku)
    - CONTEXT (Advanced Metadata Context)
  - Define the specific ID mapping for items and objects modes as requested.
  - Update `VERSION` to v1.53.003.

---

## 3. Frontend Multi-Mode Toggle
- **[MODIFY] `app_core.js`**
  - Update `toggleLibraryFilterMode` to cycle through the 5-mode array: `['route', 'category', 'items', 'objects', 'context']`.
  - Update `hydrateCategoryDropdown` to correctly pull IDs from the expanded mode registry.

---

## Verification Plan

### Automated Tests
- `python3 src/core/main.py` (Verify successful boot without manual pip install)
- `python3 -m py_compile src/core/config_master.py`

### Manual Verification
- Click the filter toggle button repeatedly.
- Verify the labels cycle: ROUTE -> CATEGORY -> ITEMS -> OBJECTS -> CONTEXT.
- Confirm the category dropdown hydrates with the specific sub-sets for each mode.

---

**Status:**
- Pending implementation and review.
- This plan ensures robust bootstrapping and a flexible, multi-mode forensic navigation experience.
