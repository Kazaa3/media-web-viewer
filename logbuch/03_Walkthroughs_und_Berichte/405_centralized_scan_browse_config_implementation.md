# Centralized Scan & Browse Path Configuration – Implementation Report

**Datum:** 14.03.2026
**Autor:** Copilot

---

## Zusammenfassung

Die Konfiguration der Scan- und Browse-Pfade ist jetzt vollständig zentralisiert und dynamisch mit der UI synchronisiert. Alle Pfadangaben sind konsistent zwischen Backend, zentraler Config und Frontend.

---

## Maßnahmen

- **Zentrale Config:**
  - SCAN_MEDIA_DIR und BROWSER_DEFAULT_DIR werden direkt aus `PARSER_CONFIG` (in `format_utils.py`) geladen und synchronisiert.
  - Defaultwerte werden korrekt aufgelöst und in der zentralen Config gespeichert.

- **Dynamische UI:**
  - Die Beschreibungstexte in den Einstellungen zeigen nun den tatsächlich verwendeten Medienpfad an (kein harter Text mehr).
  - Die UI erhält die Pfade direkt vom Backend und ersetzt Platzhalter dynamisch.

- **Persistenz:**
  - Über die neue API `update_browse_default_dir` kann der Standard-Browse-Pfad dauerhaft in der parser_config.json gespeichert werden.

- **Backend-Sync:**
  - `get_environment_info` liefert die aktuellen Pfade an das Frontend, sodass diese für Beschreibungen und Vorbelegungen genutzt werden können.

---

## Ergebnis

- Pfadangaben sind konsistent und zentral verwaltet.
- Die UI ist dynamisch und zeigt immer den korrekten Pfad an.
- Änderungen an den Pfaden werden sofort und dauerhaft übernommen.

---

**Details siehe:**
- [main.py](/src/core/main.py)
- [parsers/format_utils.py](/src/parsers/format_utils.py)
- [web/app.html](/web/app.html)
- [walkthrough.md](walkthrough.md)
