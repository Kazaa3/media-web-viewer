# Überblick: Tab- und Feature-Struktur der App

**Datum:** 15.03.2026

## Media Web Viewer – Funktionsübersicht

Der Media Web Viewer ist eine moderne Desktop- und Webanwendung zur Verwaltung und Wiedergabe von Mediendateien. Die App bietet eine übersichtliche, tab-basierte Benutzeroberfläche (GUI) mit folgenden Hauptbereichen:

- **Player:** Wiedergabe von Audio- und Videodateien, Steuerung (Play, Pause, Seek, Lautstärke, Shuffle, Repeat), Anzeige von Metadaten und Cover. Unterstützt verschiedene Playback-Engines (Browser, VLC, FFmpeg).
- **Bibliothek:** Übersicht und Verwaltung aller Medien, Filter- und Suchfunktionen, Anzeige von Details und Metadaten.
- **Browser:** Durchsuchen des Dateisystems, Hinzufügen neuer Medienverzeichnisse, Anzeige von Dateitypen und Icons.
- **Edit:** Bearbeiten von Metadaten, Umbenennen und Löschen von Medien, direkte Interaktion mit der Datenbank und den Dateien.
- **Optionen:** Konfiguration von Scan- und Library-Ordnern, App- und Parser-Modus, Debug-Flags, Anzeige von System- und Umgebungsinformationen.
- **Parser:** Verwaltung und Konfiguration der Metadaten-Parser-Kette, Anpassung parser-spezifischer Optionen.
- **Debug:** Anzeige von Logs, Systemstatus, Python- und DB-Informationen, Wechsel des Log-Levels.
- **Tests:** Ausführen und Anzeigen von Test-Suites, Testergebnissen und Logs.
- **Logbuch:** Dokumentation aller Änderungen, Features, Bugs und Testfälle, Filterung nach Kategorie und Status.
- **Playlist:** Erstellen, Bearbeiten und Abspielen von Playlists, Reihenfolge ändern, Shuffle, Speichern/Laden.
- **VLC/Video:** Erweiterte Videowiedergabe mit verschiedenen Engines (Browser, VLC, FFmpeg), Import/Export von VLC-Playlists, Drag & Drop.

Jeder Tab ist mit spezifischen Backend-APIs verbunden (z. B. Medienliste, Metadaten-Extraktion, Parser-Info, Debug-Logs, Test-Suites, Playback). Die Architektur ist modular, testbar und für Erweiterungen ausgelegt.

## Erweiterung: Diagnostics & Modale

### Diagnostics
- Die App bietet im Debug-Tab und im Optionen-Tab umfassende Diagnostikfunktionen:
  - Anzeige von Systemstatus, Python-/Venv-Informationen, installierten Paketen und Tool-Verfügbarkeit (ffmpeg, vlc, mediainfo etc.).
  - Health-Checks und Latenztests für Backend und UI.
  - Log-Ausgabe und Fehlerprotokollierung für schnelle Fehleranalyse.
  - Test-Suites und Gate-Tests zur Überprüfung der wichtigsten Funktionen.

### Modale Dialoge
- Die Benutzeroberfläche nutzt modale Dialoge für zentrale Interaktionen und Rückmeldungen:
  - **Logbuch-Editor:** Erstellen und Bearbeiten von Logbuch-Einträgen in einem eigenen Modal.
  - **Impressum/About:** Anzeige von Lizenz- und Entwicklerinformationen in einem Modal.
  - **Warnungen/Bestätigungen:** Modale Fenster für kritische Aktionen (z. B. Löschen, Reset, Fehler).
  - **Debug-Flags:** Modale Übersicht und Steuerung der Debug-Optionen.

Diese Mechanismen sorgen für Transparenz, Nachvollziehbarkeit und eine sichere Bedienung der App – sowohl für Endnutzer als auch für Entwickler und Tester.
