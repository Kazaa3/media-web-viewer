# Walkthrough: Media Journey & 0-Item Resolution (v1.37.08)

## Overview
The "Audit Track (Journey)" suite transforms the media loading process from a "Black Box" into a transparent, auditable pipeline. This tool enables you to trace any media item's path through the system and pinpoint exactly where it is lost or filtered out.

---

## 1. The Journey Timeline
- **Access:** Open the Diagnostics Sidebar (top-right pulse icon) and switch to the ITEM TRACK tab.
- **Function:** Search for any filename to view its life-cycle across the stack:
  1. **DATABASE:** Presence in the SQLite index.
  2. **MODELS (SSOT):** Category detection in models.py.
  3. **BACKEND FILTER:** Pass/fail status in backend filters (category/search).
  4. **FRONTEND MEMORY:** Loaded in browser RAM (allLibraryItems).
  5. **DISPLAY FILTER:** Pass/fail in UI filters (search/genre/category).
  6. **LIVE DOM:** Actual rendering as a visible grid node.

---

## 2. Stability & SSOT Fixes
- **ImportError Resolved:** Restored DSD_EXTENSIONS in models.py for backward compatibility.
- **Modularized Sidebar:** Diagnostics sidebar is now tabbed (Hydration vs. Item Track) for clear separation of stats and file audits.
- **Footer Restoration:** Footer icon cluster refined; theme toggle and navigation buttons are now correctly positioned and functional.

---

## 3. Verification
- **Backend Audit:** Correctly identifies the specific reason an item was dropped (e.g., extension_mismatch, genre_filter).
- **DOM Auditor:** Alerts if an item is present in memory but not rendered in the UI.

---

## TIP
Use the ITEM TRACK feature whenever a file is missing from the UI. The green/red timeline will show exactly which filter or code line is responsible for hiding it.

---

**Date:** 2026-04-06
**Author:** GitHub Copilot
