# Logbuch Meilenstein: Duale Datenbank-Falle & Pfad-Audit (v1.35.68)

## Diagnose & Fix

### 1. Fehlerursache
- Es existierten zwei Datenbank-Dateien:
  - ./database.db (im Hauptverzeichnis, 0 Byte, leer)
  - ./data/database.db (im Datenordner, 600 KB, 541 Titel)
- Die Applikation griff teilweise auf die leere Datei zu, was zu [DB: 0] im Sync-Anker und leeren Bibliotheken führte.

### 2. Fix & Härtung
- Die leere 0-Byte-Datenbank wurde gelöscht.
- Das Backend wurde so gehärtet, dass es explizit und ausschließlich ./data/database.db verwendet.
- In main.py wurde ein Pfad-Audit eingebaut: Bei jedem Laden wird der absolute Pfad der verwendeten DB-Datei geloggt.
- Der Server-Prozess wurde neu gestartet, damit die neuen Regeln greifen.

### 3. Verifikation
- RAW im Footer aktivieren und ↻ Ansicht laden klicken.
- Der Sync-Anker springt von [DB: 0] auf [DB: 541 | GUI: 541].
- Der PROBE-Button zeigt im Status-Popup den aktuell verwendeten Datenbankpfad an.

## Ergebnis
- Die „Schwarzes Loch“-Ursache im Dateisystem ist beseitigt.
- Maximale Transparenz durch Pfad-Audit und Logging.
- Die Mediathek ist wieder vollständig sichtbar und synchron.

---

**Meilenstein abgeschlossen: Duale Datenbank-Falle & Pfad-Audit.**
