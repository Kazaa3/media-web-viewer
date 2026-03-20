# UI-Tab-Audit – März 2026

## Task
Systematische Überprüfung aller Applikations-Tabs auf Layout- und Darstellungsfehler.

- Ziel: Jede Haupt- und Sub-Ansicht aufrufen, Screenshots anfertigen, Auffälligkeiten dokumentieren.
- Vorgehen: http://localhost:8345/app.html geöffnet (bei Verbindungsfehler Fallback auf file://-Pfad).

## Getestete Tabs
- Player
- Bibliothek (Cover Flow, Grid, Details)
- Item
- Datei
- Edit
- Optionen (Allgemein, Tools, Infrastruktur)
- Parser
- Debug DB
- Tests
- Reporting
- Logbuch
- Playlist
- Video
- Flags
- Features

## Ergebnisse
### Allgemein
- Navigationsleiste funktioniert, die meisten Tabs laden ihre Panels korrekt.
- Verbindung zu localhost:8345 nicht möglich; stattdessen file:///home/xc/#Coding/gui_media_web_viewer/web/app.html genutzt.

### Layout-Bugs
- [object Object] erscheint am Anfang der Top-Navigation.
- [object Object] erscheint im Footer (unten rechts).
- Player-Steuerung bleibt in der mittleren Spalte auf allen Tabs sichtbar.
- Status-Labels wie voffline und sync_offline_no_backend erscheinen (erwartet, da Backend nicht läuft).
- Einige Tabs (z.B. Bibliothek, Item) zeigen große leere Bereiche.

### Spezifische Screens
- Optionen: Alle Sub-Tabs vorhanden und konsistent.
- Parser: Regex-Orchestrator-Panel korrekt dargestellt.
- Debug DB: Cache- und Systeminfo erreichbar.
- Logbuch: Dokumentationsjournal funktionsfähig.

## Screenshots
- Für jede Ansicht wurden Screenshots angefertigt (siehe Testarchiv).

## Lessons Learned
- UI-Tab-Audit deckt systematisch Layout- und Renderfehler auf, die im laufenden Betrieb übersehen werden könnten.
- Fallback auf file://-Pfad ist für reine Layout-Tests ausreichend, Backend-Status muss aber beachtet werden.
- Persistente UI-Elemente (z.B. Player-Steuerung) sollten für Nicht-Player-Tabs ausgeblendet werden.
- [object Object]-Fehler deuten auf fehlerhafte Template- oder JS-Ausgabe hin und müssen gezielt gesucht werden.
