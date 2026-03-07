<!-- Category: Release -->

# Release v1.1.12 – Datenmanagement & Klassik-Support

Dieser Release konzentriert sich auf eine bessere Kontrolle über die Anwendungsdaten und eine verfeinerte automatische Erkennung von Musikgenres, insbesondere im Bereich der klassischen Musik.

## Highlights

### 1. App-Daten Reset (Factory Reset)
- Neue Funktion in den Optionen ermöglicht es, nicht nur die Datenbank zu leeren, sondern die gesamte Anwendung auf den Werkszustand zurückzusetzen.
- Löscht restlos alle privaten Konfigurationen (`~/.config/gui_media_web_viewer`) und die Datenbank (`~/.media-web-viewer`).
- Ideal für Troubleshooting oder zum sauberen Neu-Indexieren der Bibliothek.

### 2. Intelligente Klassik-Erkennung
- Einführung der neuen Kategorie **"Klassik"**.
- Automatische Erkennung basierend auf:
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
