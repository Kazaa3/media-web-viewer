# Logbuch: Automatisierte Datenbankbereinigung & Steuerung

**Datum:** 11. März 2026

---

## Ziel
Automatisierte Bereinigung der Datenbank beim Start, um Altlasten und fehlerhafte Einträge (z.B. durch mehrfach genutzte venvs) zu entfernen. Steuerung per CLI-Parameter und GUI-Button in den Optionen.

## Copilot-Anweisung
- Entwicklung immer mit der Dokumentation beginnen (siehe DOCUMENTATION.md).
- Die Bereinigungslogik soll als Startup-Option implementiert werden (CLI-Parameter).
- Zusätzlich einen GUI-Button in den Optionen für manuelle Bereinigung.
- Die Funktion muss robust und sicher sein, um Abstürze zu vermeiden.
- Logging und Fehlerbehandlung gemäß logger.py-Konvention.
- Die Bereinigung soll alle typischen Fragmente/Altlasten entfernen, die beim Scan immer wieder auftauchen (siehe unten).

## Typische Fragmente/Altlasten (optimiertes Wording)
- Unbekannter Künstler / Unbekannte Datei
- Hörbuch / Compilation / Film / Bilder / Spur X/Y
- Testdaten: test1, test2, test_graphic, test_photo, track, clip, disks, movie, song
- Dateinamen mit generischen Mustern: "1411_c_von_a_bis", "OLE_DB_ODBC", "S3gold1_g", "JUDITA_169_OPTION"
- Medien mit fehlenden oder generischen Metadaten (z.B. "Spur 01", "Spur 02", "Spur 2/18", "Spur 5/23")
- Wiederkehrende Künstlernamen: "Various Artists", "Unbekannter Künstler", "Verschiedene Interpreten"
- Medien mit typischen Album-/Mixtape-/Compilation-Titeln
- Dateien mit ".opus", ".mp4" und generischen Titeln

## Doku-Start
Siehe [DOCUMENTATION.md](DOCUMENTATION.md) für Architektur, API und Workflow.
Siehe [db.py](db.py) für Datenbanklogik und [env_handler.py](env_handler.py) für Umgebungsverifizierung.


## Bugfix-Strategie: Filterregeln für generische Audio-Einträge
Diese Regeln sorgen dafür, dass generische oder fehlerhafte Audio-Einträge nicht in der Datenbank verbleiben:

- **Generische Namen:** Einträge mit Namen wie "audiobook", "song", "track" und "Unbekannter Künstler" werden ausgeschlossen.
- **Dateiendungen:** Dateien mit Endung ".opus" und generischem Künstler werden gefiltert.
- **Metadaten-Prüfung:** Medien ohne spezifische Metadaten (z.B. nur "Spur X/Y", keine Album-/Künstler-Info) werden entfernt.
- **Kombinierte Filter:** Nur Einträge mit vollständigen und spezifischen Metadaten (Künstler, Album, Titel) bleiben erhalten.
- **Logging:** Alle gefilterten oder entfernten Einträge werden im Log protokolliert (siehe logger.py).

**Beispielhafte Bugs, die entfernt werden:**
- Kid Cudi vs. Crookers - Day 'n' Night.opus / Unbekannter Künstler
- Limp Bizkit - My Generation.opus / Unbekannter Künstler
- Youth Of The Nation - P.O.D.opus / Unbekannter Künstler
- audiobook / Unbekannter Künstler (Hörbuch)
- song / Unbekannter Künstler
- track / Unbekannter Künstler

**Nächste Schritte:**
- Filterregeln im Code umsetzen (db.py, main.py)
- Tests für die Filterlogik ergänzen
- Logging für entfernte Einträge implementieren
**Nächste Schritte:**
- Doku-Analyse
- Bereinigungsfunktion im Code vorbereiten
- CLI-Parameter und GUI-Button implementieren
- Logging und Fehlerbehandlung ergänzen
