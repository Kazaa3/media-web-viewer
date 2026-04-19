# Implementation Plan: Forensic UI Sentinel & WindowManager Registration (v1.45.180)

## app_core.js
- **Module Registration:**
    - Alle fehlenden Module (tools, options, reporting, logbuch, parser, tests) im WindowManager registriert.
    - Jedes Modul erhält eine eindeutige shellId, fragmentId und fragmentPath für automatisiertes Monitoring.

## visibility_sentinel.js
- **Visibility Monitoring:**
    - Die audit()-Schleife fragt jetzt WindowManager.activeWindow ab.
    - Sichtbarkeitsdurchsetzung: Das Shell des aktiven Fensters muss sichtbar und opak sein.
    - Hydration Enforcement: Ist der Fragment-Container >2s leer oder auf "Loading...", wird WindowManager.activate(name, true) forciert.
    - mwv_trace-Logging für alle Recovery-Aktionen.

## ui_nav_helpers.js
- **Navigation Orchestration:**
    - switchTab und switchMainCategory sind strikt an den WindowManager-Lifecycle gekoppelt.
    - Redundante/legacy Sichtbarkeits-Overrides entfernt, die mit dem Sentinel konkurrieren könnten.

---

## Open Questions
- Soll ein "Maximum Recovery Attempts"-Limit eingeführt werden, um Endlosschleifen zu verhindern, falls ein Fragment physisch fehlt?
- Soll die "Black Hole"-Recovery einen sichtbaren Toast anzeigen oder im Hintergrund bleiben?

---

## Verification Plan
- **Automatisierte Tests:**
    - DOM Auditor (web/js/ui_integrity_verify.js) prüft, dass alle registrierten Shells je nach Aktivität display:flex oder display:none sind.
    - Browser-Konsole auf [SENTINEL] RESCUE-VISIBILITY-Logs prüfen, nachdem ein Container manuell versteckt wurde.
- **Manuelle Prüfung:**
    - Schnelles Navigieren zwischen Tabs (Player → Library → Tools) darf keine Blackouts erzeugen.
    - Im Hydration Audit (Diagnostics Sidebar) müssen alle Module den Status "success" zeigen.

---

**Status:**
- Sentinel und WindowManager sichern die UI-Struktur, Blackouts werden automatisch erkannt und repariert.
