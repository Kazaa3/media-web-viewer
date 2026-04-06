# Logbuch: Media Viewer Footer UI & Diagnostics Toggle Finalization (v1.37.05)

## Overview
Die Footer-Oberfläche von Media Viewer v1.37.05 wurde finalisiert. Der rechte Footer-Cluster entspricht jetzt der gewünschten visuellen Reihenfolge und integriert den neuen Diagnosezugang für die Analyse des "0-item"-Bibliotheksproblems.

## Finalisierte Footer UI (Right Cluster)
**Referenzdatei:** [web/app.html](web/app.html)

Die Bedienelemente im rechten Cluster wurden in der finalen Anordnung umgesetzt:
- `Theme Toggle` (Sun Icon) bleibt am Anfang des Clusters für Hell-/Dunkelmodus.
- `Program Menu` als runder Hamburger-Button im restaurierten v1.34-Stil.
- `Main Sidebar` / Split-View-Toggle für die Standardnavigation.
- `System Diagnostics` mit Pulse-Icon als schneller Zugang zur technischen Overlay-Diagnostik.

Damit ist der Diagnosezugang direkt im Footer verankert und optisch an die bestehende UI angepasst.

## Neue Diagnosefunktion für das "0-item"-Problem
**Betroffene Bereiche:** [web/app.html](web/app.html), [web/js/ui_nav_helpers.js](web/js/ui_nav_helpers.js), [web/js/diagnostics_helpers.js](web/js/diagnostics_helpers.js), [web/css/main.css](web/css/main.css)

Der neue Pulse-Button öffnet die mehrstufige Diagnostics-Overlay-Ansicht. Diese dient als primäres Werkzeug zur Analyse des Hydration- und Filterproblems in der Bibliothek.

### Enthaltene Debug-Werkzeuge
- **Data Flow Probes**
  - Zeigt, an welcher Stelle Medienobjekte aus der Pipeline herausfallen.
- **Action Center**
  - `Manual Sync` zur Rehydrierung der Bibliothek.
  - `Deep Scan` für einen vollständigen Re-Index des Dateisystems.
- **Observability Parity**
  - Live-Abgleich zwischen Datenbankzeilen und tatsächlich im GUI sichtbaren Einträgen.

## Ergebnis
Die Footer-Navigation ist nun nicht nur optisch finalisiert, sondern auch funktional auf schnelle Diagnose ausgelegt. Der neue Diagnose-Toggle verbessert die Erreichbarkeit der technischen Werkzeuge erheblich und verkürzt den Weg zur Ursachenanalyse des Bibliotheksfehlers.

## Empfohlener Debug-Flow
1. Pulse-Button im Footer anklicken.
2. Diagnostics Overlay öffnen.
3. `Data Flow Probe` ausführen.
4. `Database` vs. `GUI` im Observability-Bereich vergleichen.
5. Falls nötig `Manual Sync` oder `Deep Scan` starten.

## Dokumentationsstatus
- Footer UI v1.37.05 dokumentiert.
- Diagnosezugang im Footer dokumentiert.
- Bezug zur "0-item"-Analyse festgehalten.
- Ergänzend siehe [logbuch/walkthrough_supercharged_diagnostics_sidebar_v13705.md](logbuch/walkthrough_supercharged_diagnostics_sidebar_v13705.md).
