# Implementation Plan – v1.41.124 Forensic Header Hierarchy (3-Tier)

## Ziel
Reorganisation der Top-Level-Navigationsleisten in eine klare 3-Tier-Hierarchie mit vollständiger Konfigurationsparität und konsistenter Benennung.

---

## Phase 1: Configuration Layer
- **[MODIFY] config_master.py**
  - Restructure `ui_settings`: Gruppiere Flags in drei Ebenen:
    - **LEVEL 1 (MASTER MENU):**
      - `master_header_visible`, `header_height`, `header_left_width`, `header_right_width`, `header_right_visible`
    - **LEVEL 2 (SUB-MENU):**
      - `sub_menu_visible` (vormals module_tabs), `sub_menu_height`, `sub_menu_width`, `sub_menu_offset_left`
    - **LEVEL 3 (TERTIARY SUB-NAV):**
      - `sub_nav_visible`, `sub_nav_height`, `sub_nav_width`, `sub_nav_offset_left`

## Phase 2: UI Orchestration
- **[MODIFY] ui_core.js**
  - Harmonize Constants: Passe `CONSTANTS` und `updateGeometry` an die neue "v1.41.124"-Hierarchie an.
  - Toggle Updates: Stelle sicher, dass `toggleSubMenu()` (vormals module tabs) und `toggleSubNav()` korrekt mit den tiered Flags synchronisiert sind.

## Phase 3: Interaction Layer
- **[MODIFY] mwv_hotkeys.js**
  - Labeling: Aktualisiere Kommentare, sodass sie die Level 1/2/3-Hierarchie widerspiegeln.

## Phase 4: Styling
- **[MODIFY] shell_master.css**
  - Class Parity: Sorge dafür, dass `.module-tab-nav` dieselben forensischen Variablen (width, offset) wie Level 1 und 3 unterstützt.

---

## Open Questions
- Sollen "Sub-Menu" (Level 2) und "Sub-Nav" (Level 3) standardmäßig denselben horizontalen Offset nutzen? **Annahme:** Jede Ebene erhält einen eigenen Offset für maximale Flexibilität.

---

## Verification Plan
- **Hierarchy Test:** Konfiguriere Level 1=48px, Level 2=30px, Level 3=35px → Gesamt-Offset ist exakt 113px.
- **Toggle Sweep:** Schalte Level 1, 2 und 3 einzeln um → Layout reflow ist korrekt.
- **Config Parity:** Alle neuen Flags (z.B. sub_menu_offset_left) werden korrekt im Backend gespeichert.

---

**Review erforderlich nach Umsetzung!**
