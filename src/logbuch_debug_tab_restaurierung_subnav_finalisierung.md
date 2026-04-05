# Implementation Plan – Debug Tab Restoration & Sub-Nav Finalization

## Datum
4. April 2026

## Ziel
Wiederherstellung des funktionsfähigen `Debug & DB`-Tabs mit echter Zwei-Spalten-Struktur inklusive Live-Konsole sowie Abschluss der dynamischen Sub-Navigation gemäß den v1.34-Modernisierungszielen.

## User Review Required
**IMPORTANT**

- **Developer Layout Restoration:** Der `Debug & DB`-Bereich wird wieder als komplexeres Diagnose-Panel mit linker Datenbank-/Dict-Spalte und rechter Live-Konsole aufgebaut.
- **Runtime Cost Notice:** Die Echtzeit-Konsole kann bei dauerhaft geöffneter Ansicht zusätzliche Ressourcen verbrauchen.

**NOTE**

- Die Sub-Navigation für `Reporting` und `Tests` wird auf alle gewünschten Module erweitert.
- Einzelne Einträge dürfen vorübergehend auf `under construction`-Fragmente zeigen, sofern die Views noch nicht vollständig implementiert sind.

## Proposed Changes

### [Frontend] Debug & DB Tab Restoration
**[MODIFY]** `diagnostics_suite.html`

- Rekonstruiere `#diagnostics-debug-db-view` als Zwei-Spalten-Grid:
  - `display: grid`
  - `grid-template-columns: 1fr 1fr`
- Linke Spalte:
  - `Item DB (Übersicht)` mit Entry-Counts und Kategorieverteilung
  - `Python Dict (Details)` mit JSON-Selektor und syntaxhervorgehobener Terminal-Ansicht
- Rechte Spalte:
  - `Konsole / Logs` als kontraststarker Terminal-Block
  - Log-Level-Selektor: `DEBUG`, `INFO`, `WARN`, `ERROR`
  - `Clear`-Aktion zum Leeren der Ansicht

**[MODIFY]** `diagnostics_helpers.js`

- Führende Fehl-Einrückung entfernen (gemeldete 8-Space-Verschiebung).
- `renderDebugDatabase()` erweitern, um:
  - DB-Kategorien zu laden und darzustellen
  - den JSON-Selektor auf `change` sauber zu verdrahten
  - Log-Streaming oder Polling für die Konsole zu initialisieren
- Helper ergänzen:
  - `setLogLevel(level)`
  - optional `clearDebugConsole()` bzw. Listener-Rebind, falls die bestehende Struktur dies erfordert

### [Frontend] Navigation & Sub-Menu Finalization
**[MODIFY]** `ui_nav_helpers.js`

- `subNavMap` auf die gewünschte Zielstruktur anheben:
  - `Reporting`: `Dashboard`, `Database`, `Video Health`, `Audio Health`, `Performance`
  - `Tests`: `System-Health`, `Debug DB`, `Latency`
  - `Media`: `Player`, `Library Browser`, `Video Cinema`
- Sicherstellen, dass alle neuen Sub-Entries korrekt verdrahtet sind, z. B. über:
  - `switchReportingView(...)`
  - `switchTab(...)`
  - vorhandene Media-/Diagnostics-Switcher
- Active-State- und Fallback-Handling prüfen, damit Hauptnavigation und Sub-Navigation synchron bleiben.

### [Frontend] Bug Fixes (White-Out Prevention)
**[MODIFY]** `app_core.js`

- Header-Blöcke auf streunende Zeichen, unvollständige Bedingungen oder beschädigte DOM-Blöcke prüfen.
- Sicherstellen, dass ein `switchTab()`-Fallback nicht fälschlich greift, wenn `ui_nav_helpers.js` korrekt geladen wurde.
- Boot-Sequenz so absichern, dass fehlende Sub-Nav-Metadaten nicht mehr zum White-Screen führen.

## Open Questions
1. Soll `Video Cinema` in `Media` den bisherigen `Playlists`-Eintrag ersetzen, oder sollen beide parallel existieren?
   - **Arbeitsannahme:** `Video Cinema` ersetzt `Playlists` nur dann, wenn die Playlist-Funktionen bereits anderweitig erreichbar bleiben. Andernfalls sollten vorerst beide sichtbar bleiben.
2. Soll die `Konsole` im Debug-Tab alle System-Logs oder nur `UI-Trace`-Events anzeigen?
   - **Arbeitsannahme:** Standardmäßig alle Logs filtern können, initial jedoch auf `UI-Trace` bzw. frontend-relevante Events fokussieren, um Rauschen zu vermeiden.

## Verification Plan

### Automated Tests
- `pytest tests/ui/navigation_verify.py` ausführen, falls die Datei vorhanden ist.
- Alternativ DOM-Prüfung via Playwright für:
  - Debug-Layout vorhanden
  - Sub-Navigationseinträge vorhanden
  - keine Syntaxfehler beim Boot in der Browser-Konsole

### Manual Verification
1. App öffnen und mit `Alt` das Programmmenü einblenden.
2. `Diagnostics` bzw. `Debug & DB` öffnen.
3. Layout prüfen:
   - links: DB-Übersicht und JSON-Dict
   - rechts: grüne bzw. kontrastreiche Live-Konsole mit eingehenden Logs
4. `System Health`, `Debug DB` und `Latency` nacheinander durchschalten.
5. `Reporting`- und `Tests`-Untermenüs auf Vollständigkeit und Routing prüfen.
6. Sicherstellen, dass beim Wechsel zwischen Haupt- und Sub-Views kein White-Out mehr auftritt.

## Recommended Defaults
- `Media` vorerst nicht destruktiv umstellen: `Video Cinema` bevorzugt einführen, `Playlists` nur entfernen, wenn die User-Flows abgesichert sind.
- Die Debug-Konsole mit Level-Filter starten und initial `INFO` oder `UI-Trace`-nahe Events priorisieren.
- Neue Sub-Navigationseinträge fehlertolerant anbinden: Wenn ein Fragment fehlt, soll ein kontrollierter Placeholder statt eines leeren Bildschirms erscheinen.
