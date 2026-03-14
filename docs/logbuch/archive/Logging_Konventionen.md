# Logbuch: Logging-Konventionen (log.debug & logging.info)

**Datum:** 11. März 2026

---

## Zweck
Klar definierte Logging-Konventionen sorgen für bessere Nachvollziehbarkeit, Debugging und Monitoring im Media Web Viewer.

---

## log.debug
- Für detaillierte technische Informationen, Fehleranalyse und Entwickler-Logs.
- Beispiel: log.debug("Starte Parsing für '%s'", filename)
- Einsatz: Parser-Pipeline, Datenbankoperationen, interne Abläufe.

## logging.info
- Für allgemeine Status- und Ablaufmeldungen, die auch für Nutzer/System relevant sind.
- Beispiel: logging.info("Datenbank erfolgreich aktualisiert.")
- Einsatz: Systemstart, wichtige Ereignisse, Statusmeldungen.

---

## Best Practices
- log.debug für technische Details, die nur im Debug-Modus sichtbar sein sollen.
- logging.info für wichtige Ereignisse, die im normalen Betrieb protokolliert werden.
- Beide Methoden mit klaren, aussagekräftigen Nachrichten verwenden.
- Logging immer mit logger.get_logger("component") initialisieren.

---

**TODO:**
- Logging-Konventionen im Code und in der Doku konsistent anwenden.
- Logbuch-Eintrag nach Erweiterung/Änderung aktualisieren.
