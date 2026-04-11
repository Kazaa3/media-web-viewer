# Logbuch v1.37.56 – Swiss HUD Footer: Hydration & GUI Refresh Control

**Datum:** 2026-04-06

## Ziel
Einführung eines "Hydration Master Control" in den Swiss HUD Footer: 3-Wege-Toggle für Mock/Real/Both und dedizierter GUI-Refresh-Button (F5) für das Eel-Frontend.

## Maßnahmen & Änderungen

### 1. UI-Komponenten (Swiss HUD Footer)
- **app.html**
  - Neuer hud-group: "HYDR"-Gruppe im Footer-Diagnostics-Cluster.
  - Hydration-Toggles: Drei Mini-Buttons [M | R | B] (Mock, Real, Both).
  - Hover-Tooltip: Detaillierte Erklärung der 4 Stages (Hardcoded, FS-Mock, Realistic, Database).
  - GUI-Refresh: [↻]-Button rechts im Cluster, triggert kompletten Browser-Reload.

### 2. Logik & Synchronisation (JavaScript)
- **audioplayer.js**
  - `setHydrationMode(mode)`: Aktualisiert window.__mwv_hydration_mode, persistiert in localStorage, triggert syncQueueWithLibrary() für sofortiges UI-Update.
  - `refreshGui()`: Führt window.location.reload() aus.

### 3. Backend-Integration (Library API)
- **main.py**
  - Konsolidierte API: `get_library` liefert alle nötigen Items (Real + Mocks) in einem Call, damit das Frontend nahtlos umschalten kann.

## Offene Frage
- Soll beim Umschalten auf M (Mock) automatisch das erste Mock-Item abgespielt werden, oder nur die Queue befüllt werden? (**Vorschlag:** Nur befüllen/syncen, kein Autoplay.)

## Verifikation
- **Manuell:**
  - Toggle: M, R, B klicken, Queue-Titel (z.B. "541 Titel") aktualisiert sich sofort.
  - GUI-Reload: [↻]-Button klicken, App startet neu mit Splash-Screen.
  - Tooltip: Hover über HYDR-Gruppe zeigt Stage-1-4-Legende.

---
**Status:** Hydration-Master-Control & GUI-Refresh dokumentiert (v1.37.56)
