# Implementation Plan – Legacy UI Restoration (v1.3.4)

## Ziel
Rückkehr zum klassischen Desktop-Design mit High-Density-Horizontallayout, Zwei-Spalten-Player und festem Footer. Fokus auf vollständige Wiederherstellung der "Click-to-Play"-Funktionalität und Desktop-Usability.

---

## Proposed Changes

### [CSS] Layout Foundations

**[MODIFY] main.css**
- **Header:**
  - `#program-menu-bar` immer sichtbar, hoher Kontrast (weißer Hintergrund, dunkle Umrandung).
- **Footer:**
  - `.layout-footer-wrapper` und `.footer-pill` als festen Bottom-Bar (width: 100%; left: 0; bottom: 0; transform: none;).
- **Cards:**
  - `.legacy-track-item` als weiße Karten mit Schatten und Hover-State.
- **Scroll:**
  - Rechte Playlist-Spalte erhält eine persistente Scrollbar.

---

### [HTML] Shell & Navigation

**[MODIFY] app.html**
- **Top Nav:**
  - Komplette Navigationsleiste wiederherstellen:
    - Player, Library, Browser, Edit, Options, Parser, Debug & DB, Tests, Logbook, Video Player, Flags, Features, Scan Media.
- **Structure:**
  - `main-content-area` dehnt sich zwischen festem Header und Footer aus.

---

### [JS] Playback & Logic Restoration

**[MODIFY] audioplayer.js**
- **Item Rendering:**
  - `renderPlaylist` zielt auf `player-view-legacy` und injiziert die High-Fidelity-Track-Cards.
- **Click-to-Play:**
  - Jeder Card-OnClick-Handler triggert zuverlässig die `play()`-Pipeline.

**[MODIFY] ui_nav_helpers.js**
- **Navigation:**
  - Alle Navigationsfunktionen auf die erweiterte Top-Header-Leiste mappen.
  - Sidebar wird nur auf expliziten Wunsch angezeigt, Standard ist "versteckt" (breites Deck).

---

## Verification Plan

### Automated Tests
- **Playwright Audit:** `app_audit_playwright.py` prüft Tab-Switches und Sichtbarkeit der Panels.
- **Integrity Probe:** `runIntegrityCheck()` bestätigt Rendering und Klickbarkeit der Track-Items.

### Manual Verification
- **Visual Match:** App mit Screenshot vergleichen.
- **Interaction:** Track in rechter Spalte anklicken, sofortige Wiedergabe prüfen.
- **Responsive Check:** Zwei-Spalten-Layout bleibt auf 1080p stabil.

---

**User Review Required:**
- Die UI wird auf das klassische Desktop-Layout zurückgestellt.
- Fokus auf Bedienbarkeit, Übersicht und sofortige Interaktion.
- Bitte Review und Freigabe vor Umsetzung!
