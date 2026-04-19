# Implementation Plan – Forensic UI Stabilization & Black Hole Recovery (v1.45)

## Zielsetzung
Die "Black Fragments" (UI-Blackouts) werden durch eine einheitliche Stabilitäts-Schicht aus Tab-Registrierung, Sichtbarkeitsüberwachung und Diagnostik-Audit strukturell verhindert.

---

## Changes Accomplished

### 1. Expanded Forensic Module Registry
- Alle fehlenden Workstation-Tabs im WindowManager registriert (tools, options, reporting, logbuch, parser, tests).
- Jeder View hat jetzt einen getrackten Lifecycle und einen Recovery-Pfad.
- **Ort:** app_core.js

### 2. Intelligent Visibility Sentinel (v1.45)
- VisibilitySentinel überwacht jetzt global alle Tabs, nicht nur #rebuild-stage.
- Drei Integritätslevel:
    - Shell Visibility: Tab-Container muss sichtbar und opak sein.
    - Fragment Hydration: Bleibt ein Fragment >4s leer oder auf "Loading", wird ein Recovery Pulse ausgelöst.
    - Loop Protection: Erkennt Recovery-Loops und triggert Atomic Emergency Reload.
- **Ort:** visibility_sentinel.js

### 3. Navigation Orchestration Cleanup
- Hauptkategorie-Switching delegiert Sichtbarkeit vollständig an den WindowManager.
- Verhindert Flicker und Race Conditions zwischen Engine und Sentinel.
- **Ort:** ui_nav_helpers.js

### 4. Forensic Chain Tracing
- mwv_trace-Punkte im gesamten Hydrationsprozess injiziert.
- Debug-Log zeigt jetzt die exakte "Kette":
    - WM:REGISTER → WM:ACTIVATE-START → FRAGMENT:FETCH → FRAGMENT:EXECUTION-COMPLETE
- **Ort:** fragment_loader.js, window_manager.js

---

## Verification Results
- **Manual Test:** Tab-Container im Inspector verstecken → Sentinel erkennt und stellt Sichtbarkeit in <2s wieder her.
- **Audit Log:** Browser-Konsole zeigt [SENTINEL] RESCUE-VISIBILITY oder [SENTINEL] Recovery pulse... für Hintergrund-Maintenance.

**Status:**
- "Black Hole"-Rendering ist strukturell unmöglich, solange der Sentinel aktiv ist.
- Architektur ist selbstheilend und auditierbar.
