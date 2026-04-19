# Implementation Plan – v1.41.115 Ultimate DOM Consolidation

## Ziel
Behebung des "Black Screen"- und "Lade Player..."-Problems durch Eliminierung kritischer Architektur-Duplikate in app.html. Konsolidierung des Audio Players in ein einziges, hochstabiles Forensic Deck und Sicherstellung, dass der WindowManager das korrekte, sichtbare Panel adressiert.

---

## Phase 1: Shell Architecture Consolidation
- **[MODIFY] app.html**
  - Delete Duplicates: Entferne den redundanten Player-Container am Ende der Datei (Zeilen 804–808).
  - Hard-Link Registry: Stelle sicher, dass der primäre Player-Container (um Zeile 530) die ID `player-panel-container` trägt.
  - Transparency Pass-Through: Setze `background: transparent !important` auf das Player-Deck, um schwarze Overlays zu verhindern.

## Phase 2: Navigation Logic Sync
- **[MODIFY] web/js/ui_nav_helpers.js**
  - Target Calibration: Sorge dafür, dass `switchMainCategory` und `switchTab` explizit auf den konsolidierten `player-panel-container` zielen.

---

## Verification Plan
- **Fragment Load Check:** "Lade Player..." verschwindet und wird durch die Metadaten-Sidebar und Queue-Liste ersetzt.
- **Visual Continuity:** Der Player-UI-Bereich ist sichtbar und nicht durch schwarze Overlays blockiert.
- **Tab Persistence:** Tab-Wechsel führen nicht mehr zu Blackouts.

---

**Review erforderlich nach Umsetzung!**
