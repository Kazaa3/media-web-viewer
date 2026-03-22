# Teststrategie: Webplayer-Debugging & Feature-Tests

## Testfall-Checkliste (Tab- und Feature-Abdeckung)

### 0. Startup Checks and Startup confirmed

### 1. Player-Tab
- [ ] Medienliste wird geladen (API: get_library)
- [ ] Audio- und Video-Playback (verschiedene Formate)
- [ ] Steuerung: Play, Pause, Stop, Seek, Lautstärke, Repeat, Shuffle
- [ ] Medien-Metadaten und Coveranzeige
- [ ] Fehlerfall: Nicht unterstütztes Format

### 2. Bibliothek-Tab
- [ ] Anzeige aller Medien (API: get_library)
- [ ] Filter/Suche funktioniert
- [ ] Auswahl und Anzeige von Details

### 3. Browser-Tab
- [ ] Verzeichnisnavigation (API: update_browse_dir)
- [ ] Hinzufügen neuer Medienpfade
- [ ] Anzeige von Dateitypen und Icons

### 4. Edit-Tab
- [ ] Laden und Bearbeiten von Metadaten (API: save_tags_to_file)
- [ ] Umbenennen und Löschen von Medien
- [ ] Fehlerfall: Schreibschutz/Fehlende Datei

### 5. Optionen-Tab
- [ ] Ändern von Scan- und Library-Ordnern
- [ ] Umschalten von App-/Parser-Modus
- [ ] Debug-Flags setzen und prüfen
- [ ] Anzeige der Python-/Venv-/Requirements-Infos

### 6. Parser-Tab
- [ ] Anzeigen und Ändern der Parser-Kette
- [ ] Speichern und Laden der Parser-Konfiguration
- [ ] Parser-spezifische Optionen testen

### 7. Debug-Tab
- [ ] Anzeigen von Logs und Systemstatus (API: get_konsole, get_debug_logs)
- [ ] Wechsel der Log-Level
- [ ] Anzeigen von Python- und DB-Infos

### 8. Tests-Tab
- [ ] Laden und Ausführen von Test-Suites (API: run_debug_test, Test-API)
- [ ] Anzeige von Testergebnissen und Logs

### 9. Logbuch-Tab
- [ ] Laden, Erstellen, Bearbeiten und Löschen von Logbuch-Einträgen
- [ ] Filterung nach Kategorie/Status

### 10. Playlist-Tab
- [ ] Hinzufügen/Entfernen von Medien zur Playlist
- [ ] Reihenfolge ändern, Shuffle, Speichern/Laden

### 11. VLC/Video-Tab
- [ ] Wechsel der Videomodi (Browser, VLC, FFmpeg, DnD)
- [ ] Playback in allen Modi (inkl. Fehlerfälle)
- [ ] Import/Export von VLC-Playlists

## 12. Modale: 12a) Feature Modal 12b) Debug Modal 12c) Impressum Modal

## 13. Naming, Versioning / Wording

## 14. Später Diagnostics Tab

---
**Hinweis:**
Jeder Testfall sollte als Backend-Test (API) und als Frontend-UI-Test (z. B. Selenium, Playwright, pytest + browser) abgedeckt werden. Playback-Tests müssen verschiedene Formate und Fehlerfälle abdecken.
**Datum:** 15.03.2026

## Ziel
- Der Webplayer (Frontend) soll umfassend debuggt und getestet werden.
- Es gibt 6 Haupt-Reiter (Tabs) im Webplayer – alle Features in jedem Tab müssen abgedeckt werden.

## Vorgehen
1. **Backend-Tests:**
   - Zuerst werden alle relevanten Backend-APIs und -Funktionen getestet (z. B. Metadaten-Extraktion, Medienlisten, Status-APIs, Log-Ausgaben).
   - Sicherstellen, dass alle Backend-Endpunkte für die Tabs korrekt und stabil funktionieren.
2. **Frontend-Integration:**
   - Für jeden der 6 Tabs werden automatisierte UI-Tests erstellt:
     - Tab-Wechsel und Sichtbarkeit
     - Feature-Buttons und Interaktionen
     - Anzeige und Playback von Medien
     - Fehler- und Edge-Case-Handling
   - Besonderes Augenmerk auf vollständiges Playback (Audio/Video) im Player-Tab.
3. **Playback-Tests:**
   - Automatisierte Tests für das vollständige Abspielen von Medien (verschiedene Formate, Codecs, Container).
   - Überprüfung von Start, Pause, Seek, Stop, Lautstärke, Vollbild etc.
   - Fehlerfälle (nicht unterstützte Formate, fehlende Codecs) werden abgefangen und geloggt.

## Test-Suite-Aufbau
- Tests werden in `tests/integration/ui/` und `tests/integration/backend/` organisiert.
- Mock- und Realdateien werden für Playback- und UI-Tests verwendet.
- Ziel: Jede Funktion und jeder Tab ist durch mindestens einen Testfall abgedeckt.

## Ergebnis
- Der Webplayer ist robust, alle Features und Tabs sind automatisiert getestet.
- Fehler werden früh erkannt und können gezielt behoben werden.
