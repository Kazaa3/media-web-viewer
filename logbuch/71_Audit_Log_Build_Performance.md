# Logbuch-Update: Audit-Log – Build-Time Performance & Parser Monitoring

## Ziel
Lückenlose Nachvollziehbarkeit aller Audit- und Performance-Messungen während des Build-Prozesses, insbesondere bei der parallelen und ressourcenschonenden Ausführung der Parser.

## Audit-Log Konzept
- **Zentrale Audit-Logs:**
  - Alle relevanten Audit- und Performance-Daten werden in `build/management_reports/` als JSON und/oder Markdown abgelegt.
  - Logs enthalten: Dateiname, Dateigröße, verwendete Parser, Skip-Entscheidungen, Laufzeit, Erfolg/Fehler, Speicherverbrauch (wo möglich).
- **Performance-Daten:**
  - Für jede Datei und jeden Parser werden folgende Werte geloggt:
    - Verarbeitungsdauer (ms)
    - Erfolg/Misserfolg (Status)
    - Speicherverbrauch (sofern messbar)
    - Parser-spezifische Besonderheiten (z.B. Fallback, Skip-Grund)
  - Aggregierte Statistiken (Durchschnitt, Median, Min/Max) werden für alle Formate und Parser im Report bereitgestellt.
  - Performance-Daten dienen als Grundlage für gezielte Optimierung und Vergleich von Parser-Strategien.
- **Parser-Monitoring:**
  - Für jeden Parser wird dokumentiert, ob er ausgeführt oder übersprungen wurde (inkl. Grund, z.B. Dateigröße >500MB).
  - Fehler, Timeouts und Ausnahmen werden mit Stacktrace und Timestamp geloggt.
- **Parallelitäts- und Ressourcen-Tracking:**
  - Bei paralleler Ausführung werden Thread/Task-IDs, Start-/Endzeit und ggf. Subprozess-IDs mitprotokolliert.
  - Audit-Log dokumentiert, wie viele Dateien/Parser parallel verarbeitet wurden.
- **Nutzung:**
  - Logs dienen als Grundlage für Performance-Analysen, Bottleneck-Erkennung und Regressionstests.
  - Sie ermöglichen gezielte Optimierung und Fehleranalyse im Build- und Testprozess.

## Status
Audit-Log-Konzept und Monitoring sind etabliert und werden kontinuierlich für Build- und Parser-Optimierung genutzt.

## Stand
13. März 2026
