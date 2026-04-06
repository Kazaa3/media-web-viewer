# Implementation Plan – v1.34 Final UI Refinement & Playback Restoration

## Ziel
Letztes Feintuning für v1.34: Menü-Ästhetik, klare Navigation, und vollständige Wiederherstellung der Medienwiedergabe. Die Top-Navigation ist standardmäßig ausgeblendet und kann per Alt-Taste oder Menü-Button ein-/ausgeblendet werden.

---

## Proposed Changes

### [HTML] Shell & Navigation Consolidation

**[MODIFY] app.html**
- **Top Nav:**
  - `#program-menu-bar` auf 40px Höhe, glassmorphes Design, per Button/Alt-Taste ein-/ausblendbar.
- **Footer:**
  - Zwei untere Bars zu einem Unified Footer zusammenführen.
  - Status-Infos (Version, Sync) in den Hauptplayer-Footer integrieren.
  - Redundante 24px-Bar entfernen.
- **Sub-Nav:**
  - Immer nur eine Sub-Navigationszeile sichtbar (kein "Doppelmenü").

---

### [JS] Navigation & Playback Restoration

**[MODIFY] ui_nav_helpers.js**
- **Menu Toggle:**
  - `toggleMenuBar()` mit persistentem localStorage-State implementieren.
- **Keyboard Listener:**
  - Globaler Listener für Alt (und optional F10) zum Menü-Toggle.
- **Sidebar Integration:**
  - Toggle-Button-State fixen, "Classic" Wide-Deck-View als Standard.

**[MODIFY] audioplayer.js**
- **Library Sync:**
  - `syncQueueWithLibrary` wird automatisch beim App-Start oder Library-Update getriggert.
- **Item Rendering:**
  - `renderPlaylist` findet zuverlässig das `active-queue-list-render-target-legacy`-Element.
- **Playback Fix:**
  - HTML5 Audio Pipeline wird korrekt mit dem Source-File-Path initialisiert.

---

## Verification Plan

### Automated Tests
- **Auditing:** `app_audit_playwright.py` prüft Tab-Switches und Menü-Toggle.
- **Integrity Probe:** `runIntegrityCheck()` prüft, ob Library-Items in der Player-Queue erscheinen.

### Manual Verification
- **Menu Check:** Alt-Taste drücken, Menü muss weich ein-/ausblenden.
- **Playback Check:** Track-Card anklicken, Audio muss starten.
- **UI Consistency:** Alle Buttons im Top-Nav sind einheitlich und modern.

---

**User Review Required:**
- Menü ist standardmäßig ausgeblendet, Fokus auf klare Oberfläche.
- Navigation und Wiedergabe sind vollständig wiederhergestellt.
- Bitte Review und Freigabe vor Umsetzung!
