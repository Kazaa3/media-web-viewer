# Implementation Plan – v1.41.104 UI Emergency Restoration

## Ziel
Behebung des kritischen Black-Screen-Fehlers und Wiederherstellung der fehlenden Sub-Navigation-Pills (Queue, Visualizer, Lyrics).

---

## Phase 1: Logic Consolidation (JS)
- Entferne die doppelte Definition von `refreshUIVisibility` (Zeile 1353 in `web/js/ui_nav_helpers.js`).
- Aktualisiere die moderne `refreshUIVisibility` (Zeile 495), sodass sie `updateGlobalSubNav()` aufruft.
- Ergänze `SUB_NAV_REGISTRY['media']` um:
  - Queue (`warteschlange`)
  - Playlist (`playlist`)
  - Visualizer (`visualizer`)
  - Lyrics (`lyrics`)

## Phase 2: Structural Visibility Enforcement (CSS)
- Füge `display: block !important` für `#player-view.active` in `web/css/main.css` hinzu.
- Sorge dafür, dass `#sub-nav-container` einen höheren `z-index` als die Fragments hat.

## Phase 3: Version Synchronization
- Aktualisiere die `VERSION` in `src/core/config_master.py` auf `1.41.104-UI-RESTORATION`.

## Phase 4: Final Verification
- Klicke auf "Player" und prüfe, ob der Black Screen verschwunden ist.
- Überprüfe, ob alle 4 Pills in der Sub-Navigation sichtbar sind.

---

**Hinweis:**
Die Ursache war eine Funktions-Kollision (doppelte Definition von `refreshUIVisibility`). Durch die Konsolidierung und CSS-Härtung wird die UI-Stabilität wiederhergestellt.

**Review erforderlich nach Umsetzung!**
