# Implementation Plan: Navigation Orchestrator Synchronization (v1.46.029)

## Ziel
Synchronisierung von Backend und Frontend durch Umbenennung der Navigations-Registry-Keys in config_master.py. Dadurch werden die Level 2 Sub-Navigation-Pills wieder sichtbar und die Navigation bleibt zukunftssicher.

## Schritte

### 1. Configuration Alignment (config_master.py)
- **legacy_navigation → navigation_orchestrator**
  - Die gesamte Navigationsstruktur wird unter dem neuen Key `navigation_orchestrator` bereitgestellt.
- **sub_nav_registry → level_2**
  - Die Sub-Navigation-Registry wird in `level_2` umbenannt.
- **sub_nav_aliases → aliases**
  - Die Alias-Registry wird in `aliases` umbenannt.
- **window.CONFIG.navigation_orchestrator.level_2** ist damit für das UI verfügbar und entspricht dem aktuellen Frontend-Standard.

## Verifikationsplan
- **Automatisiert:**
  - `python3 src/core/main.py --probe` ausführen und prüfen, dass die Konfiguration das interne Schema validiert.
- **Manuell:**
  - Nach Auswahl einer Level 1 Kategorie erscheinen die zugehörigen Sub-Navigation-Pills (z.B. 'Queue', 'Playlist', 'Alben-Galerie') wieder korrekt in der horizontalen Leiste.

## Status
- Keine Kategorien oder Sub-Tabs werden gelöscht.
- Backend und Frontend sind wieder synchronisiert.
- Die Navigation ist robust und zukunftssicher.

---

**Freigabe erforderlich:**
Bitte bestätigen Sie, ob diese Registry-Umbenennung wie beschrieben umgesetzt werden soll.