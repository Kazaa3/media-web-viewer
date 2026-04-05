# Logbuch: Task-Checkliste – Video Player & Media Handling Overhaul (März 2026)

## 1. Planung & Research
- Analyse von task.md und Überführung in den Overhaul-Plan
- Pipeline für mkvmerge → Chrome Native Streaming skizziert
- "Advanced Tools"-Panel in app.html auf Leerstellen geprüft
- "Special Object"-Struktur für DVD-Ordner (Name (Jahr) + Cover + ISO) definiert
- Kategorie-Erkennung in models.py auf fehlende Typen geprüft

## 2. Infrastruktur & Logging
- Verbesserte VLC-Fehlerprotokollierung in main.py implementiert
- "Advanced Tools"-Inhalte (HandBrake, WebM, etc.) vollständig integriert
- DVD/ISO-Special-Object-Zuordnung im Scanner/Modell verfeinert
- dvd://-URL-Generierung für DVD-Bundle-Ordner korrigiert (innerer Pfad)

## 3. Video Player Overhaul
- mkvmerge → Chrome Native (Matroska/WebM) Streaming-Route implementiert
- Logging/Output für alle Tools im Advanced Tools Tab umgesetzt
- Playback der "Vortrag"-Datei über Direct, FragMP4 und Remux getestet
- Multi-Player-Varianten (FFplay, VLC, CVLC, PyVLC) in main.py integriert
- Format-Support für DVD-ISOs, Ordner und Audio (M4B/Opus) verfeinert
- Port/Venv-Isolation für Selenium E2E-Tests umgesetzt
- Final-Check: Alle 24 Playback-Varianten erfolgreich getestet

## 4. Verifikation & Dokumentation
- Selenium-Tests für Chrome Native Streaming erstellt
- "Special Object"-DVD-Erkennung und Metadaten-Zuordnung verifiziert
- Test-Mockups in test_file_formats_suite.py mit Labels versehen
- generate_test_media.py erstellt (echte .mkv, .mp4, etc. für E2E)
- Walkthrough mit neuer Architektur aktualisiert
- Advanced Tools (HandBrake, WebM, etc.) vollständig backend-integriert
- Final-Check: Alle 24 Playback-Varianten (Tiered Selection) bestanden

---

**Datum:** 18. März 2026  
**Autor:** GitHub Copilot
