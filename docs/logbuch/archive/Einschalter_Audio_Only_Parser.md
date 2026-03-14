# Logbuch: Einschalter für Audio-Only-Parser-Pipeline

**Datum:** 11. März 2026

---

## Ziel
Ein flexibler Einschalter für die Audio-Only-Parser-Pipeline, um die Verarbeitung auf Audio-Medien zu begrenzen und andere Medientypen temporär zu blockieren.

## Optionen für den Einschalter
- **CLI-Parameter:** z.B. `--audio-only` (main.py)
- **Konfigurationsflag:** z.B. `PARSER_CONFIG["audio_only"]`
- **GUI-Option:** Checkbox im Optionen-Menü (web/app.html)

## Stand im Code
- Mechanismen für CLI-Flags sind vorhanden (siehe main.py: initialize_debug_flags, is_no_gui_mode).
- Im Web-Frontend existiert bereits ein Toggle für den Parser-Modus.

## Empfehlung
- CLI-Flag `--audio-only` einführen (main.py)
- Konfigurationsoption in `PARSER_CONFIG` ergänzen
- GUI-Checkbox für Audio-Only-Modus (web/app.html)
- Prüfung in media_parser.py: Wenn Audio-Only aktiv, nur Audio verarbeiten, sonst alles blockieren und loggen

## Nächste Schritte
- Code-Implementierung für den Einschalter (CLI, Config, GUI, Parser-Logik)
- Logging und Doku ergänzen

---

**Frage:**
Soll ich mit der Code-Implementierung für den Einschalter beginnen (CLI, Config, GUI, Parser-Logik)?


Umsetzung: Audio-Only-Parser mit Einschalter und Datenbankbereinigung
1. CLI-Flag und Konfigurationsoption
In main.py wird ein neues CLI-Flag --audio-only eingeführt.
Beim Start wird geprüft, ob das Flag gesetzt ist. Dann wird PARSER_CONFIG["audio_only"] = True aktiviert.
2. GUI-Checkbox
Im Optionen-Menü (web/app.html) wird eine Checkbox „Nur Audio verarbeiten“ ergänzt.
Der Status wird an das Backend übergeben und synchronisiert mit PARSER_CONFIG["audio_only"].
3. Parser-Pipeline-Absicherung
In media_parser.py wird vor der Verarbeitung geprüft:
Ist audio_only aktiv und der Medientyp kein Audio, wird die Verarbeitung übersprungen und ein Log-Eintrag erzeugt.
TODO/FIXME-Kommentar im Code für spätere Erweiterung.
4. Automatisierte Datenbankbereinigung
Beim Start (oder per GUI-Button) wird eine Bereinigungsfunktion aufgerufen, die alle typischen Altlasten und generischen Einträge entfernt:
Filterregeln: generische Namen, fehlende Metadaten, bestimmte Dateiendungen.
Logging für alle entfernten Einträge.
5. Dokumentation
Alle Änderungen und Filterregeln werden in der Doku (DOCUMENTATION.md) und im Logbuch dokumentiert.
Die temporäre Blockade für Nicht-Audio ist als TODO/FIXME markiert.
Nächste Schritte:

Code-Implementierung für CLI-Flag, Config, GUI-Checkbox und Parser-Logik.
Bereinigungsfunktion in db.py/main.py ergänzen.
Logging und Doku aktualisieren.
Melde dich, wenn ich mit der konkreten Code-Implementierung starten soll.
