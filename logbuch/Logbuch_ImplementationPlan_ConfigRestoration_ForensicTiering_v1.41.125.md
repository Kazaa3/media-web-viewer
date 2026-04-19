# Implementation Plan – v1.41.125 Configuration Restoration & Forensic Tiering

## Ziel
Wiederherstellung aller globalen UI-Settings nach versehentlichem Verlust und Etablierung der gewünschten 3-Tier-Hierarchie (Level 1, 2, 3) in einer sauberen, vollständigen Struktur.

---

## Phase 1: Configuration Layer
- **[MODIFY] config_master.py**
  - Authoritative Restoration: Baue den Block `ui_settings` von Grund auf neu auf und stelle sicher, dass keine Flags (Sidebar, Footer, HUD, Fragments etc.) fehlen.
  - Tiered Grouping:
    - **LEVEL 1 (MASTER MENU):** Alle Header-/Top-Menu-Flags (z.B. master_header_visible, header_height, header_left_width, header_right_width, header_right_visible)
    - **LEVEL 2 (SUB-MENU):** Alle Module-Tab/Mid-Bar-Flags (z.B. sub_menu_visible, sub_menu_height, sub_menu_width, sub_menu_offset_left)
    - **LEVEL 3 (TERTIARY SUB-NAV):** Alle Contextual-Pill/Bottom-Header-Flags (z.B. sub_nav_visible, sub_nav_height, sub_nav_width, sub_nav_offset_left)
    - **GLOBAL ENGINE FLAGS:** Sidebar, Footer, HUD, Fragments etc.

---

## Open Questions
- Gibt es spezielle Custom-Höhen oder -Breiten, die als neue Defaults gesetzt werden sollen? **Annahme:** Es werden die Standardwerte aus v1.41.124 verwendet (48px, 32px, 35px).

---

## Verification Plan
- **Config Audit:** Zeilenweiser Abgleich des neuen ui_settings-Blocks mit dem Zustand vor der Löschung plus neuer Hierarchie.
- **Persistence Test:** Flag über die UI ändern → Sicherstellen, dass es korrekt in der neuen Struktur persistiert.

---

**Review erforderlich nach Umsetzung!**
