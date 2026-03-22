# Logbuch-Eintrag: Media Type Synchronization (Central Config)

## Ziel
Zentrale, versionierte Konfiguration für angezeigte Medientypen, um Konsistenz über alle Umgebungen sicherzustellen.

## Konzept
- Einheitliche Steuerung der Medientypen über zentrale JSON-Templates.
- Branch-spezifische Konfiguration: Production (main) vs. Entwicklung (develop).
- Erweiterung der Backend-Logik für neue Kategorien und Mapping.

## Umsetzung
- [MODIFY] `config.main.json`: Nur `displayed_categories: ["audio"]` (minimal für Produktion).
- [MODIFY] `config.develop.json`: Alle Kategorien (`audio`, `video`, `images`, `documents`, `ebooks`, `abbild`, `spiel`, `beigabe`).
- [MODIFY] `format_utils.py`: PARSER_CONFIG-Defaults um neue Kategorien ergänzt.
- [MODIFY] `main.py`: `get_library`-Logik erweitert, damit "spiel" und "beigabe" in den Defaults sind, falls keine Config geladen wird. `cat_map` um technische Strings wie "PC Spiel", "Supplement" ergänzt.

## Verification Plan
- **Config Deployment:** `python3 infra/build_system.py --deploy-config` erzeugt `web/config.json` mit den richtigen Kategorien.
- **Library Filtering:** `get_library` liefert Medien mit "PC Spiel"-Label, wenn "spiel" im Filter ist.

## Status
Abgeschlossen – Medientyp-Konfiguration ist zentral, versioniert und branch-spezifisch ausgerollt.

## Stand
13. März 2026
