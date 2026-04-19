# Implementation Plan – Multi-Level UI Restoration & Level 2 Hardening (v1.41.135)

## Ziel
Synchronisierung der Navigation und Behebung des "Black Screen"-Problems durch gezielte Anpassungen an WindowManager, Sub-Nav-Logik und Pill-Design.

---

## Phase 1: UI Orchestration
- **[MODIFY] window_manager.js**
  - Aktualisiere `_hideAllShells()`, sodass alle Elemente mit `.tab-content` ODER `.deck-view` ausgeblendet werden.
  - Dadurch wird beim Tab-Wechsel immer nur ein Viewport angezeigt.

- **[MODIFY] ui_nav_helpers.js**
  - Stärkung der `updateGlobalSubNav`-Logik: Jeder Kategorie-Wechsel triggert ein vollständiges Level-2-Menü-Refresh.
  - Nutze das hardcodierte `SUB_NAV_REGISTRY` für sofortige Reaktionsfähigkeit.

## Phase 2: Level 2 Redesign
- **[MODIFY] shell_master.css**
  - Premium "Pill"-Ästhetik:
    - 6px Radius, fette Typografie, leuchtende aktive Glows.
    - Kategorie-spezifische Farben: Blau (Media), Türkis (Status), Orange (Library).

---

## Verification Plan
- **Automated Tests:**
  - Navigation Probe: `WM.activate('debug')` blendet Player aus und zeigt Status-Panel an.
  - Registry Audit: `updateGlobalSubNav` liefert für alle 4 Kernkategorien die korrekten Pills.
- **Manual Verification:**
  - STATUS klicken: Pills wechseln zu Logs/Health, Viewport zeigt Diagnostik.
  - PLAYER klicken: Pills wechseln zu Queue/Playlist, Viewport zeigt Player.

---

**Review erforderlich nach Umsetzung!**
