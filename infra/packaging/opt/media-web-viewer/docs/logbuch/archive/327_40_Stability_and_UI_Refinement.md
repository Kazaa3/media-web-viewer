<!-- Category: Planning -->
<!-- Title_DE: Stabilität & UI Refinement -->
<!-- Title_EN: Stability & UI Refinement -->
<!-- Summary_DE: Verbesserungen am Parser und allgemeine Fehlerbehebungen für v1.1.15. -->
<!-- Summary_EN: Parser improvements and general bug fixes for v1.1.15. -->
<!-- Status: COMPLETED -->

# Stability and UI Refinement

## Fokus
Nach den großen Feature-Releases liegt der Fokus nun auf der Stabilität des Systems und der Behebung von kleineren UI-Ecken.

## Verbesserungen
- **Parser Robustheit**: Bessere Fehlerbehandlung bei beschädigten MP3/M4B Dateien.
- **i18n System**: Umstellung auf ein deklaratives System via JSON, das nun auch das Logbuch und die Features unterstützt.
- **Performance**: Optimierung der SQLite-Abfragen für große Bibliotheken.

<!-- lang-split -->

# Stability and UI Refinement

## Focus
After the major feature releases, the focus is now on system stability and fixing minor UI glitches.

## Improvements
- **Parser Robustness**: Better error handling for corrupted MP3/M4B files.
- **i18n System**: Switch to a declarative system via JSON, which now also supports the logbook and features.
- **Performance**: Optimization of SQLite queries for large libraries.
n ermöglicht es, nicht nur die Datenbank zu leeren, sondern die gesamte Anwendung auf den Werkszustand zurückzusetzen.
- Löscht restlos alle privaten Konfigurationen (`~/.config/gui_media_web_viewer`) und die Datenbank (`~/.media-web-viewer`).
- Ideal für Troubleshooting oder zum sauberen Neu-Indexieren der Bibliothek.

### 2. Intelligente Klassik-Erkennung
    - **Komponisten**: Beethoven, Mozart, Bach, Chopin werden direkt erkannt.
    - **Keywords**: "Klassik" oder "Classical" in Genre, Interpret oder Verzeichnispfad führen zur korrekten Einstufung.
- Verbessert die Strukturierung großer Sammlungen erheblich.

### 3. Debugging & Transparenz
- Neues Debug-Flag **"TESTS"**: Erlaubt das Ein- und Ausschalten von Test-Logs in der Konsole.
- Verfeinerte Blacklist: Weitere systemfremde Dateien werden nun zuverlässig beim Scan ignoriert.

### 4. UI-Polishing
- Überarbeitete Gefahrenzone in den Optionen mit klareren Warnhinweisen und separaten Buttons für DB-Leeren vs. Full-Reset.

## Nächste Schritte
- Erweiterung der Komponisten-Liste für die Klassik-Automatik.
- Performance-Optimierung des Resets bei sehr großen Konfigurationsordnern.
