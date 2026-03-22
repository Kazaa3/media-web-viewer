# Logbuch-Eintrag: Build-Time Performance Audit & Parser Statistics

## Ziel
Management-taugliche Transparenz über Parser-Performance, Formatabdeckung und aktuelle Einstellungen direkt im Build-Prozess.

## Konzept & Umsetzung
- [MODIFY] `benchmark_all_parsers.py`:
  - Unterstützung für `PERF_REPORT_DIR` zur zentralen Ablage.
  - Aggregation von Statistiken pro Dateiformat:
    - Erfolgsrate pro Format
    - Durchschnittliche Verarbeitungszeit pro Format
    - Dominanter Parser pro Format (welcher Parser liefert die Tags)
  - Inklusion des aktuellen `PARSER_CONFIG`-Snapshots im Report.
- [MODIFY] `build_system.py`:
  - Neues CLI-Flag: `--audit-performance` (oder Integration in `--build-all`).
  - Automatische Umgebungsvariable `PERF_REPORT_DIR` für Benchmarks.
  - Sicherstellen, dass alle Reports in `build/management_reports/` landen.

## Verification Plan
- **Report Content:** `--audit-performance` ausführen und prüfen, dass der JSON-Report `format_stats`, `parser_config` und `detailed_results` enthält.
- **CI Integration:** Sicherstellen, dass der Audit-Report als Artifact in GitHub Actions erscheint.

---

# Logbuch-Eintrag: Media Type Synchronization (Update)

## Ziel
Zentrale, versionierte Konfiguration für angezeigte Medientypen, um Konsistenz über alle Umgebungen sicherzustellen.

## Konzept & Umsetzung
- [MODIFY] `config.main.json`: Nur `displayed_categories: ["audio"]` (minimal für Produktion).
- [MODIFY] `config.develop.json`: Alle Kategorien (`audio`, `video`, `images`, `documents`, `ebooks`, `abbild`, `spiel`, `beigabe`).
- [MODIFY] `format_utils.py`: PARSER_CONFIG-Defaults um neue Kategorien ergänzt.
- [MODIFY] `main.py`: `get_library`-Logik erweitert, damit "spiel" und "beigabe" in den Defaults sind, falls keine Config geladen wird. `cat_map` um technische Strings wie "PC Spiel", "Supplement" ergänzt.

## Verification Plan
- **Config Deployment:** `python3 infra/build_system.py --deploy-config` erzeugt `web/config.json` mit den richtigen Kategorien.
- **Library Filtering:** `get_library` liefert Medien mit "PC Spiel"-Label, wenn "spiel" im Filter ist.

## Status
Abgeschlossen – Performance-Audit, Parser-Statistiken und Medientyp-Konfiguration sind umgesetzt und getestet.

## Stand
13. März 2026
