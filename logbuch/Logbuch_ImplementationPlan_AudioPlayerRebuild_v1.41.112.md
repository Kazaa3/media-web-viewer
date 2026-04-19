# Implementation Plan – v1.41.112 Audio Player Rebuild

## Ziel
Struktureller Neuaufbau des Audio Player-Bereichs in der legacy app.html, um das "Black Screen"-Problem zu beheben und die fehlenden Sub-Navigation-Pills (Queue, Playlist, Lyrics) wiederherzustellen.

---

## Phase 1: Audio Player Structural Rebuild
- **[MODIFY] app.html**
  - Sub-Nav Restoration: Füge den `#sub-nav-container` explizit innerhalb von `player-panel-container` wieder ein.
  - Atomic Bridge Mapping: Stelle sicher, dass `player-panel-container` die richtigen `active`- und `tab-content`-Klassen besitzt.
  - Viewport Hardening: Ergänze ein explizites `id="audio-player-main-viewport"` mit 100% Geometrie.

## Phase 2: Visibility Enforcement
- **[MODIFY] web/css/main.css**
  - Display Layer Sync: Füge eine forensische CSS-Regel hinzu, damit `#player-panel-container` niemals von Legacy-Overlays überdeckt wird.

## Phase 3: Navigation Handshake
- **[MODIFY] web/js/ui_nav_helpers.js**
  - Pill Refresh: Erzwinge einen Aufruf von `refreshUIVisibility('media')` während der Player-Aktivierung, damit die Sub-Menu-Pills sofort erscheinen.

---

## Verification Plan
- **Hydration Check:** "Queue", "Playlist" und "Lyrics" erscheinen wieder in der Sub-Navigation.
- **Visual Check:** Der Black Screen ist verschwunden, der Player-UI-Bereich ist sichtbar.
- **Control Handshake:** Klick auf die Pills wechselt korrekt die Sub-Views.

---

**Review erforderlich nach Umsetzung!**
