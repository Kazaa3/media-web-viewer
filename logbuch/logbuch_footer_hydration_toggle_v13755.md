# Logbuch v1.37.55 – Technical Footer: Hydration Mode Toggle

**Datum:** 2026-04-06

## Ziel
Einführung eines "Hydration Toggle" im technischen Footer, um zwischen Mock-, Real- und Hybrid-Ansicht in Echtzeit zu wechseln. Inklusive Stage-1-4-Erklärung als Tooltip.

## Maßnahmen & Änderungen

### 1. UI-Komponenten (Technischer Footer)
- **index.html** (bzw. Footer-Fragment)
  - Toggle-Button [M | R | B] (Mock, Real, Both) im Diagnostic-Pill-Cluster ergänzt.
  - Tooltip: Hover zeigt Erklärung der 4 Stages:
    1. Connection (Hardcoded)
    2. FS-Aware (Local ./media)
    3. Realistic (Classic Bypass Set)
    4. Database (Production Data)

### 2. State Management & Hydration Logic (JS)
- **audioplayer.js**
  - Globaler State: window.__mwv_hydration_mode (persistiert in localStorage).
  - Hybrid-Logik: syncQueueWithLibrary merged/filtered die Items je nach Footer-Toggle.

### 3. Backend API (Response Refinement)
- **main.py**
  - Data Union: get_library liefert bei "Hybrid"-Request immer echte Items + Stage-3-Mocks, für nahtloses Umschalten ohne Latenz.

## Offene Frage
- Soll "Mock"-Modus auch das Backend in den Bypass zwingen (keine DB-Calls), oder reicht das reine Ausblenden im Frontend? (**Vorschlag:** Backend-aware für maximale Performance-Isolation.)

## Verifikation
- **Manuell:**
  - Toggle: Klick auf M zeigt nur Mocks, auf B alle Items, auf R nur echte Medien.
  - Tooltip: Hover über Toggle zeigt die Stage-1-4-Erklärung.

---
**Status:** Hydration-Toggle im technischen Footer dokumentiert (v1.37.55)
