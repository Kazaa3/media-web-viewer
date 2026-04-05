# Logbuch-Eintrag: Media Type Configuration Synchronization

## Ziel
Synchronisierung und Standardisierung der Media-Type-Konfiguration über alle Projektbereiche hinweg.

## Konzept
- Zentrale Verwaltung der angezeigten und indizierten Medientypen ("displayed_categories", "indexed_categories") in den Haupt-Konfigurationsdateien.
- Erweiterung der Backend-Logik zur konsistenten Kategorisierung und Filterung.
- Automatisierte, branch-spezifische Bereitstellung der Konfiguration über das Build-System.

## Umsetzung
1. **config.main.json & config.develop.json**: Hinzufügen und Vereinheitlichen von `displayed_categories` und `indexed_categories` inkl. "spiel" (PC Games) und "beigabe" (Supplements).
2. **src/core/main.py**: Erweiterung von `cat_map` und der Filterlogik, sodass "PC Spiel" und "Supplement" korrekt zugeordnet und angezeigt werden.
3. **BuildSystem CLI**: Hinzufügen des Flags `--deploy-config` zu `infra/build_system.py` für branch-spezifische Bereitstellung.
4. **Verifikation**: Lokale Prüfung, dass `web/config.json` nach Deployment alle Kategorien korrekt enthält und die Filterung in der Bibliothek funktioniert.

## Status
Abgeschlossen – Die Medientyp-Konfiguration ist jetzt zentral, versioniert und konsistent in allen Umgebungen verfügbar.

## Stand
13. März 2026

---

**Summary of changes:**
- Central Configuration: Added `displayed_categories` and `indexed_categories` to the central templates (`config.main.json` and `config.develop.json`).
- Backend Extension: Updated `src/core/main.py` to include "PC Games" (spiel) and "Supplements" (beigabe) in the mapping logic, ensuring they appear correctly in the library.
- Build System Enhancement: Added a new `--deploy-config` flag to `infra/build_system.py`, providing a clean CLI path for branch-aware configuration deployment.
- Verified deployment: `web/config.json` now correctly reflects the synchronized state.

Das Projekt ist konsistent und bereit für die nächsten Schritte.