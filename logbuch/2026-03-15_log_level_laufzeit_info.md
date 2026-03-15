# Logbuch: Log-Level & Laufzeit-Info – Verhalten und offene Punkte

**Datum:** 15.03.2026

## Übersicht
Dieses Logbuch dokumentiert das aktuelle Verhalten beim Setzen des Log-Levels über die Laufzeit-Info/Optionen sowie offene Probleme mit bestimmten Log-Levels.

---

## 1. Aktuelles Verhalten
- Das Log-Level kann zur Laufzeit über die Optionen/Laufzeit-Info gesetzt werden.
- Die Werte "debug" und "info" funktionieren wie erwartet:
  - **debug**: Zeigt ausführliche Debug-Ausgaben.
  - **info**: Zeigt normale Betriebsinformationen.
- Die Werte "warning" und "error" funktionieren **nicht wie erwartet**:
  - Beim Setzen auf "warning" oder "error" bleibt das Log-Level auf dem vorherigen Wert oder es werden weiterhin zu viele Logs angezeigt.
  - Es erfolgt keine saubere Filterung auf Warnungen/Fehler.

---

## 2. Offene Fragen & Probleme
- Warum greifen die Log-Levels "warning" und "error" nicht korrekt?
- Wird das Log-Level intern korrekt an das Logging-Framework übergeben?
- Gibt es Caching, Mehrfach-Logger oder andere Mechanismen, die das Setzen verhindern?
- Muss das Backend nach Änderung des Log-Levels neu gestartet werden?

---

## 3. Nächste Schritte
- Analyse der Logik zum Setzen des Log-Levels (Backend und ggf. Frontend).
- Testen, ob das Problem bei allen Loggern oder nur bei bestimmten Komponenten auftritt.
- Ergänzung der Dokumentation, sobald die Ursache gefunden und behoben ist.

---

## Bekannter Fehler
- Die Log-Level **WARNING** und **ERROR** sind zwar in der GUI auswählbar, haben aber aktuell **keine Wirkung** auf die tatsächliche Log-Ausgabe.
- Das Umschalten auf diese Level zeigt keinen Effekt – es werden weiterhin alle Logs angezeigt.
- Nur **DEBUG** und **INFO** funktionieren wie erwartet.
- Die Ursache ist noch offen und muss im Backend/Logger-Handling analysiert werden.

---

## Einschränkung
- Das Umschalten des Log-Levels funktioniert aktuell **nur für zwei der vier Level** zuverlässig:
  - **DEBUG** und **INFO**: Umschalten und Logging funktionieren wie erwartet.
  - **WARNING** und **ERROR**: Umschalten zeigt keine Wirkung bzw. es werden weiterhin zu viele Logs angezeigt.
- Die Ursache für dieses Verhalten ist noch offen und muss weiter analysiert werden.

---

## Nachtrag: Log-Level-Änderung funktioniert

- Die Änderung des Log-Levels über die UI funktioniert wie erwartet.
- Proof aus der Konsole:

```
2026-03-15 19:19:07 [INFO] [root] [UI-Trace] [UI-Trace 19:19:06] switchTab: options → parser
2026-03-15 19:19:07 [INFO] [root] [UI-Trace] [UI-Trace 19:19:07] switchTab: parser → debug
2026-03-15 19:19:13 [INFO] [root] [System] Log-Level manually set to DEBUG
2026-03-15 19:19:18 [INFO] [root] [System] Log-Level manually set to INFO
2026-03-15 19:19:28 [INFO] [root] [System] Log-Level manually set to DEBUG
2026-03-15 19:19:29 [INFO] [root] [System] Log-Level manually set to INFO
```

- Das Umschalten zwischen DEBUG und INFO wird korrekt erkannt und geloggt.

---

**Siehe auch:**
- [Debug-Log-Level & Parser-Logging – Status & offene Fragen](2026-03-15_debug_log_level_status.md)
- [Test- und Quick-Skripte zum Setzen der Config](2026-03-15_test_quickskripte_config.md)
