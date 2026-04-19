# Implementation Plan – v1.41.126 Authoritative Config Restoration

## Ziel
Wiederherstellung aller versehentlich gelöschten Konfigurations-Flags und Etablierung der 3-Tier-Header-Hierarchie (Level 1, 2, 3) anhand der Einstellungen und Kommentare aus Commit 7906aa0.

---

## Phase 1: Configuration Layer
- **[MODIFY] config_master.py**
  - Restoration & Tiering: Baue das Registry `ui_settings` mit folgender Struktur wieder auf:
    - **LEVEL 1: MASTER MENU (Top Header)**
    - **LEVEL 2: SUB-MENU (Module Tabs)**
    - **LEVEL 3: TERTIARY HEADER (Sub-Nav)**
    - **GLOBAL UI ELEMENTS & GEOMETRY:** Sidebar, Footer, HUD
    - **GRANULAR UI FRAGMENT FLAGS**
    - **FUNKTIONALE MODULE:** Engine Toggles (Audio, Video, Queue, etc.)
  - Inklusive aller forensischen Kommentare und vollständiger Liste an Engine-Toggles aus dem Repository-Verlauf.

---

## Verification Plan
- **Geometric Match:** Prüfen, dass die Top-Level-Offsets der 3-Tier-Hierarchie im UI entsprechen.
- **Flag Persistence:** Sicherstellen, dass alle funktionalen Toggles (z.B. footer_visible, audio_engine_enabled) vorhanden und funktionsfähig sind.

---

**Review erforderlich nach Umsetzung!**
