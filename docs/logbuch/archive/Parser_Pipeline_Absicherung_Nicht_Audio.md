# Logbuch: Parser-Pipeline Absicherung für Nicht-Audio

**Datum:** 11. März 2026

---

## Ziel
Die Parser-Pipeline soll für alle Medien außer Audio temporär deaktiviert bzw. abgesichert werden. Nur Audio-Medien werden weiterhin verarbeitet. Alle anderen Medientypen (Video, Bild, Hörbuch, etc.) werden vorübergehend "totgestellt" (keine Verarbeitung, keine Einträge in der Datenbank).

## Copilot-Anweisung
- Entwicklung immer mit der Dokumentation beginnen.
- Die Absicherung soll als temporäre Maßnahme erfolgen, bis die Filter/Bereinigung für andere Medientypen implementiert ist.
- Die Pipeline für Nicht-Audio-Medien muss robust blockiert werden (keine Verarbeitung, keine Datenbankeinträge).
- Logging für alle blockierten Medientypen aktivieren.
- Die Maßnahme soll klar im Code und in der Doku markiert werden (TODO/FIXME).

## Umsetzung
- In der Parser-Pipeline (parsers/media_parser.py) eine Prüfung einbauen:
  - Wenn Medientyp != Audio: Verarbeitung überspringen, Logging ausgeben.
  - Nur Audio-Medien werden weiter analysiert und gespeichert.
- Alle anderen Medientypen werden ignoriert und ggf. im Log protokolliert.
- Die temporäre Blockade wird in der Doku und im Code als TODO/FIXME markiert.

## Doku-Start
Siehe [DOCUMENTATION.md](DOCUMENTATION.md) für Architektur und Workflow.
Siehe [parsers/media_parser.py](../parsers/media_parser.py) für die Parser-Logik.

---

**Nächste Schritte:**
- Doku-Analyse
- Code-Absicherung in media_parser.py
- Logging für blockierte Medientypen ergänzen
- TODO/FIXME im Code und in der Doku markieren
