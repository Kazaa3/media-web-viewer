# Library Hydration & "Black Hole" Resolution (v1.37.07)

## Problem: The "Black Hole" in the Display Chain
A critical bug was identified in the frontend's `renderLibrary` logic (web/js/bibliothek.js), where a secondary filtering loop used an outdated or mismatched CATEGORY_MAP. This caused a major drop in visible items (e.g., 527 → 0), even when the backend returned the correct set.

## Root Cause
- The backend and frontend had different "Sources of Truth" for category definitions (e.g., what counts as "audio" or "video").
- The frontend CATEGORY_MAP was not synchronized with the backend's MASTER_CAT_MAP, leading to items being dropped after backend hydration.

## Solution: SSOT Synchronization & Diagnostic Breakdown

### 1. JS Logic & SSOT Synchronization
- On boot, the frontend now fetches the MASTER_CAT_MAP from the backend and populates CATEGORY_MAP.
- This ensures the frontend only filters categories that the backend recognizes, preventing accidental drops.

### 2. Diagnostic Breakdown in renderLibrary
- Added audit logging to show the full breakdown:
  - **DB:** Raw items in the database (e.g., 541)
  - **LIB:** Items received by the frontend (e.g., 541)
  - **CAT:** After category selection filter (e.g., 527)
  - **GUI:** After all filters and DOM injection (final visible count)

### 3. DOM Integrity Auditor
- Implemented a function to scan the library grid for hidden or missing elements.
- Alerts if the number of DOM nodes does not match the expected count after filtering.

### 4. Black Hole Visualizer
- Sidebar now includes a color-coded stage breakdown panel, making it easy to spot where items are dropped.

## Verification Plan
- **Total Parity:** With "All Categories" selected, the UI must show exactly the number returned by Stage 2 in the backend.
- **Casing Verification:** Selecting "Musik" (German) must correctly display items with the internal key `audio`.

## Status
- Phase 1: Models & SSOT (backend refactor) — Done
- Phase 2: Multi-Stage Hydration (backend logic) — Done
- Phase 3: Frontend Diagnostics & DOM Audit — In Progress

---

**Date:** 2026-04-06
**Author:** GitHub Copilot
