# Logbuch v1.37.64 – Implementation Plan: Media Viewer Hydration Stabilization

**Datum:** 2026-04-06

## Ziel
Synchronisation zwischen Backend-Forensik-Index (541 Items) und Frontend-UI, volle Funktionalität der "Mock/Real/Both"-Toggles und korrekte Anzeige aller realen Items in Bibliothek und Queue.

## Maßnahmen & Änderungen

### 1. Frontend Diagnostic Bridge
- **common_helpers.js**
  - `updateSyncAnchor(dbCount, guiCount, fsSize)` global definiert, damit die Sync-Stats im Footer überall aktualisiert werden können.

### 2. UI Controller & Hydration
- **audioplayer.js**
  - `setHydrationMode(mode)` triggert jetzt sofort `renderLibrary()` und `syncQueueWithLibrary()`.
  - Footer-Buttons spiegeln den aktiven Modus korrekt wider.
- **bibliothek.js**
  - `renderLibrary()` respektiert jetzt `window.__mwv_hydration_mode`.
  - "Real": Mocks werden ausgefiltert, "Both": alles wird angezeigt.

### 3. Backend Data Pipeline
- **main.py**
  - Mocks werden auf Wunsch des Frontend-Diagnosemodus in das Library-Payload injiziert, unabhängig vom audit_stage.

## Offene Frage
- Soll die App beim Kaltstart auf "Real" oder "Both" defaulten? (**Aktuell:** "Both" für maximale Sichtbarkeit während der Stabilisierung.)

## Verifikation
- **Automatisiert:**
  - Logs: [Sync-Audit] Stage 2: ... zeigt, dass der Hydration-Loop läuft.
  - Konsole: [Hydration] Switching to mode: ... beim Klick auf Footer-Buttons.
- **Manuell:**
  - App öffnen, Footer zeigt [DB: 541 | GUI: 544] (in "Both").
  - Auf "Real" toggeln, Count sinkt auf 541.
  - 541 Items sind in der Library Grid sichtbar.

## Ursachen & Korrekturen
- setHydrationMode triggert jetzt sofortigen Re-Sync.
- updateSyncAnchor global verfügbar gemacht.
- Filterlogik in bibliothek.js mit Hydration-Mode synchronisiert.

---
**Status:** Stabilisierungsplan für Media-Hydration dokumentiert (v1.37.64)
