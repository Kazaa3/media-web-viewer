# Debug-Log-Level & Parser-Logging – Status & offene Fragen

**Datum:** 15.03.2026

## Übersicht
Dieses Logbuch dokumentiert den aktuellen Stand der Debug- und Logging-Einstellungen (insbesondere Parser-Logging) sowie offene Fragen zur optimalen Konfiguration.

---

## 1. Aktuelle Einstellungen (Stand 15.03.2026)
- In den Konfigurationsdateien (`web/config.json`, `web/config.develop.json`):
  - `debug`: false
  - `log_level`: "INFO"
  - `feature_flags.verbose_parsing`: false
- Damit ist das Parser-Logging standardmäßig deaktiviert und das allgemeine Log-Level auf "INFO" gesetzt (keine Debug-Flut in der Konsole).

---

## 2. Offene Fragen & Diskussionspunkte
- **Was sind sinnvolle Debug-/Log-Einstellungen für Entwicklung, Test und Produktion?**
  - Welche Flags/Level sind für Entwickler:innen hilfreich, ohne die Konsole zu überfluten?
  - Wann ist `verbose_parsing` sinnvoll, wann sollte es aus sein?
  - Sollten bestimmte Komponenten (z.B. nur Parser, nur DB) gezielt auf Debug schaltbar sein?
- **Wie werden Debug-Flags und Log-Level im laufenden Betrieb am besten gesteuert?**
  - Per Config, per Kommandozeile, per UI?
- **Wie sieht ein "Best Practice"-Profil für verschiedene Umgebungen aus?**
  - Entwicklung: Mehr Debug, gezielt aktivierbar?
  - Produktion: Minimal, nur Fehler/Warnungen?

---

## 3. Nächste Schritte
- Klärung und Dokumentation von Best-Practice-Empfehlungen für Debug-/Log-Einstellungen.
- Evtl. Implementierung feingranularer Debug-Flags pro Komponente.
- Ergänzung der Dokumentation, sobald ein Konsens gefunden ist.

---

**Siehe auch:**
- [Shutdown/KeyboardInterrupt – Logbuch](2026-03-15_shutdown_keyboardinterrupt.md)
- [Browser PID und Auswahl – Logbuch](2026-03-15_browser_pid_und_auswahl.md)
