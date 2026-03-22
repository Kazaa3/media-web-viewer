# Logbuch: Logger-Konvention – log.error vs logging.error

**Datum:** 17. März 2026

## Logger-Konvention im Projekt

### Unterschied
- **log.error:** Wird verwendet, wenn ein Logger-Objekt (z.B. log = logging.getLogger("component") oder log = logger.get_logger("core")) instanziiert wurde. Log-Ausgaben erfolgen dann über log.error(...), log.info(...), etc.
- **logging.error:** Direkter Aufruf der globalen Logging-Funktion, ohne spezifisches Logger-Objekt.

### Projektstandard
- Im Projekt werden für jede Komponente eigene Logger verwendet (z.B. log = logger.get_logger("core")).
- Vorteil: Log-Ausgaben sind gezielt filterbar und können einzelnen Komponenten zugeordnet werden.
- log.error ist daher die empfohlene und korrekte Methode für Fehlerausgaben.

### Fazit
- log.error: Korrekt bei Nutzung eines Logger-Objekts (empfohlen im Projekt).
- logging.error: Nur für globales Logging ohne spezifischen Logger.

---

Weitere Details siehe logger.py und die Projektkonventionen.
