# Logbuch v1.37.69 – Implementation Plan: Forensic Data-Flow Audit (v1.35.68)

**Datum:** 2026-04-06

## Ziel
Granulare, schrittweise Forensik des Media-Data-Flows von der SQLite-Datenbank bis zum Frontend-DOM. Ziel: Exakt identifizieren, wo die 541 indexierten Items gefiltert oder verloren gehen.

## Phase 1: Research (The Data Chain)

### 1. Database Layer (Level 0)
- **Status:** 541 Items in SQLite media table bestätigt.
- **Aktion:** Keine nötig, DB ist gesund.

### 2. Backend Filter Layer (Level 1)
- **Status:** Items passieren `_apply_library_filters`.
- **Aktion:** Server-Logs auf `[BD-AUDIT]`-Warnungen prüfen (category_mismatch, branch_mismatch).

### 3. Frontend Memory Layer (Level 2)
- **Status:** Items landen in `window.allLibraryItems`.
- **Aktion (Browser Subagent):**
  - `window.allLibraryItems.length` prüfen
  - `window.__mwv_hydration_mode` prüfen
  - `window.CATEGORY_MAP` prüfen

### 4. Frontend Render Layer (Level 3)
- **Status:** `renderLibrary()` filtert Items in den DOM.
- **Aktion (Browser Subagent):**
  - Anzahl der `#coverflow-track`-Kinder inspizieren
  - Konsole auf Fehler während `renderLibrary` prüfen

## Offene Frage
- Soll ein Factory Reset via UI erfolgen, falls der Memory-State inkonsistent ist? (Entscheidung nach Audit-Report)

## Verifikationsplan
- **Automatisiert:**
  - Browser Subagent liefert detaillierten Report zu window-State und DOM-Struktur.

---
**Status:** Forensik-Plan für Data-Flow-Audit dokumentiert (v1.37.69)
