# Implementation Plan – v1.41.119 UI Geometry & Toggle Hardening

## Ziel
Globale Konfiguration der Höhen von Haupt-Header und Sub-Navigation sowie Einführung von Hotkeys zum individuellen Umschalten der Sichtbarkeit.

---

## Phase 1: Configuration Layer
- **[MODIFY] config_master.py**
  - Geometry Injection: Ergänze `ui_settings` um `"header_height": 48` und `"sub_nav_height": 35`.
  - Visibility Defaults: Füge `"master_header_visible"` und `"sub_nav_visible"` zum globalen State hinzu.

## Phase 2: UI Orchestration
- **[MODIFY] ui_core.js**
  - Dynamic Constants: Passe `init()` an, sodass die Konstanten aus dem geladenen Config übernommen werden.
  - Toggle Methods:
    - `toggleHeader(forceVisible?)`: Schaltet den Header und aktualisiert die `ui_visibility_matrix` für die aktuelle Kategorie.
    - `toggleSubNav(forceVisible?)`: Schaltet die Sub-Navigation.
  - Persistence: Toggle-States werden via `set_ui_config_value` zurück an das Python-Backend synchronisiert.

## Phase 3: User Interaction
- **[MODIFY] ui_nav_helpers.js**
  - Hotkey Listeners: Füge Listener für Alt+H (Header) und Alt+N (Sub-Nav) hinzu, die die neuen MWV_UI-Toggle-Methoden auslösen.

---

## Open Questions
- Soll die Sichtbarkeitsumschaltung global (für alle Kategorien) oder nur für die aktuelle Kategorie gelten? **Aktuelle Annahme:** Global für die Session, kann aber pro Kategorie erweitert werden.

---

## Verification Plan
- **Config Test:** `header_height` in `config_master.py` auf 60 ändern → UI-Header wächst nach Reload.
- **Toggle Test:** Alt+H → Header verschwindet, Layout verschiebt sich korrekt.
- **Toggle Test:** Alt+N → Sub-Nav verschwindet, Layout verschiebt sich korrekt.
- **Persistence Test:** Nach Umschalten und Reload bleibt der Zustand erhalten (falls Persistence aktiviert).

---

**Review erforderlich nach Umsetzung!**
