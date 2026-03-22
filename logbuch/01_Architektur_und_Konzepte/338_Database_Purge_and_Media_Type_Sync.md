# Logbuch-Eintrag: Database Purge & Clean Release Policy

## Ziel
Sicherstellen, dass Release-Builds immer mit einem sauberen Zustand starten (frischer Scan), während Entwicklungs-Builds persistente Daten für effizientes Testen behalten.

## Konzept
- Release-Builds: Keine vorgefüllte Datenbank im Paket, vollständige Entfernung bei Purge.
- Dev-Builds: Datenbank bleibt erhalten, um Entwicklungszyklen zu beschleunigen.
- Branch-spezifische Steuerung über Build-Metadaten und Skripte.

## Umsetzung
- [MODIFY] `build_system.py`: Übergibt BRANCH als Umgebungsvariable an `build_deb.sh`.
- [MODIFY] `build_deb.sh`: Fügt `--exclude 'data/'` zu rsync hinzu, damit das Paket nie eine vorgefüllte Datenbank enthält.
- [MODIFY] `postrm`: Robusteres grep-Muster, vollständiges Wipen für alle Branches außer dev/milestone.

## Verification Plan
- **Build Metadata:** Paket bauen und prüfen, dass `.build_metadata` den korrekten Branch enthält.
- **Package Hygiene:** Mit `dpkg -c` prüfen, dass `opt/media-web-viewer/data/` im .deb fehlt.
- **Purge Test:** Release-Build installieren, Daten anlegen, dann `apt purge` und prüfen, dass `/opt/media-web-viewer` komplett entfernt wird.

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
Abgeschlossen – Release-Policy und Medientyp-Konfiguration sind branch-spezifisch, versioniert und getestet.

## Stand
13. März 2026
