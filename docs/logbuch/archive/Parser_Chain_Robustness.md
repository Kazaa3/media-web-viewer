# Enhancing Parser Chain Robustness

**Datum:** 12. März 2026

---

## Ziel
Die Resilienz der Metadaten-Extraktionspipeline wird verbessert, um Parser-Abstürze, Prozessabbrüche und State-Korruption robust abzufangen.

---

### Änderungen im Orchestrations-Layer (media_parser.py)
- **State Isolation:**
  - `current_tags` wird als Kopie an Parser übergeben oder bei Fehlern aus Backup wiederhergestellt.
- **Exception Handling:**
  - Spezifische Behandlung von `TimeoutExpired` bei Subprozess-Parsers.
  - Graceful Handling von `ImportError` für optionale Dependencies.
  - Vermeidung von "partial tag leak": Nach Absturz werden halbfertige Keys entfernt.
- **Logging:**
  - Fehlerlogs enthalten Kontext (Datei, Parser, Versuch).
- **Timeout Decorator:**
  - Per-Call Timeout-Wrapper für Parsing-Loop, um Hänger zu verhindern.

---

### Änderungen in den Parser-Modulen
- **Input Read-Only:**
  - Alle Parser behandeln Input als read-only.
- **Timeouts:**
  - `subprocess.run` immer mit Timeout.

---

### Verifikationsplan
- **Automatisierte Tests:**
  - Corruption Test: Parser crasht, nachfolgende Parser erhalten sauberen State.
  - Timeout Test: Hängender Parser, Chain läuft nach Timeout weiter.
  - Process Death Test: Prozessabbruch, Exception wird abgefangen.
- **Manuelle Verifikation:**
  - App starten, Logs beim Parsen "schwieriger" Dateien beobachten.

---

*Entry created: 12. März 2026*
