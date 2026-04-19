# Implementation Plan – v1.41.120 UI Forensic Expansion

## Ziel
Erweiterung der Umschalt- und Geometrie-Konfiguration auf alle 5 Haupt-UI-Komponenten: Header, Sub-Navigation, Module Tabs, Footer und Sidebar.

---

## Phase 1: Configuration Layer
- **[MODIFY] config_master.py**
  - Geometry Sync: Ergänze und bestätige folgende Werte in `ui_settings`:
    - `"header_height": 48`
    - `"sub_nav_height": 35`
    - `"module_tab_height": 32`
    - `"footer_height": 48`
    - `"sidebar_width": 250`

## Phase 2: UI Orchestration
- **[MODIFY] ui_core.js**
  - Config Sync: Passe `init()` an, sodass alle 5 Konstanten aus dem Backend geladen werden.
  - Dynamic Calculation: Aktualisiere `updateGeometry()`, sodass `total-top-offset` dynamisch aus Header-, Sub-Nav- und Module-Tab-Sichtbarkeit berechnet wird.
  - Unified Toggling: Implementiere `toggleModuleTabs()`, `toggleFooter()` und synchronisiere `toggleSidebar()` mit der neuen Geometrie-Engine.

## Phase 3: User Interaction
- **[MODIFY] ui_nav_helpers.js**
  - Full Hotkey Registry: Füge Hotkeys hinzu:
    - Alt+H (Header)
    - Alt+N (Sub-Nav)
    - Alt+M (Module Tabs)
    - Alt+F (Footer)
    - Alt+S (Sidebar)

## Phase 4: Styling & Layout
- **[MODIFY] shell_master.css**
  - Visibility Infrastructure: Ergänze `.mwv-hide-module-tabs`, `.mwv-hide-footer` und unterstütze dynamische `.sidebar`-Breite über Variablen.

---

## Open Questions
- **"Third Menu" ID:** Die dritte horizontale Leiste wird als `.module-tab-nav` identifiziert. Falls sie nicht in allen Kategorien vorhanden ist, behandelt der Toggle dies automatisch.

---

## Verification Plan
- **Geometry Check:** `total-top-offset` summiert nur sichtbare Top-Bars korrekt.
- **Toggle Marathon:** Schnelles Umschalten aller 5 Komponenten (Alt+H/N/M/F/S) hält das Layout stabil.
- **Config Check:** Änderung von `footer_height` auf 100 in Python → UI-Footer wächst nach Reload.

---

**Review erforderlich nach Umsetzung!**
