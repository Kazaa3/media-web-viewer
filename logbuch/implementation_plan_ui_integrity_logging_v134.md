# Implementation Plan – UI Integrity & Robust Logging (v1.34)

## Problem Statement
Zwei kritische visuelle Bugs im neuen Player-Layout wurden identifiziert:
- Inhalt ist nach rechts verschoben.
- Playlist-Items erscheinen nicht.

Zusätzlich wurde ein robustes Logging aller GUI-Interaktionen gefordert.

---

## Proposed Changes

### [Frontend] Robust Interaction Logging

**[MODIFY] trace_helpers.js**
- **Global Click Listener:**
  - Erfasse alle Klick-Events im DOM.
  - Logge Ziel-id, className und (ggf. gekürzten) innerText via `mwv_trace` an das Backend.
- **Tab Switch Logging:**
  - Jeder Aufruf von `switchTab` und `switchMediaSubView` erzeugt ein Trace-Event.

**[MODIFY] ui_nav_helpers.js**
- Integriere `traceUiNav` in die Kernlogik des Tab-/Subnav-Switchings, um jeden Wechsel zu erfassen.

---

### [Frontend] Player UI Fixing & Polish

**[MODIFY] player_queue.html**
- **Layout-Fix:**
  - Setze `#player-deck-column`-Breite auf 420px.
  - Entferne zentrierende Paddings, die Content nach rechts verschieben.
- **Metadaten-Erweiterung:**
  - Füge Platzhalter für `#spec-path` und eine dedizierte Zeile für die graue Tech-Info-Box hinzu.

**[MODIFY] main.css**
- **Card-Styling:**
  - Gestalte `.legacy-track-item` als große weiße Karten (runde Ecken, dezente Ränder statt Glassmorphism).
- **Tech-Box:**
  - Definiere `.legacy-tech-box` (hellgrauer Hintergrund, Mono-Font für Specs).

**[MODIFY] audioplayer.js**
- **Playlist-Rendering:**
  - `renderPlaylist` zielt korrekt auf DOM-Elemente, ohne den Container mit "Empty State" zu überschreiben, wenn andere Views aktiv sind.
  - `#active-queue-list-render-target-legacy` wird beim Hinzufügen korrekt geleert und neu gerendert.
- **Metadaten-Update:**
  - Dateipfad und detaillierte Bitrateninfos werden im Legacy-Deck angezeigt.

---

## Verification Plan

### Automated Tests
- Führe `tests/ui/navigation_verify.py` aus, um Tab-Erreichbarkeit zu prüfen.

### Manual Verification
- Öffne den Audio Player Tab.
- Füge Tracks aus der Bibliothek zur Queue hinzu und prüfe, ob sie als große weiße Karten rechts erscheinen.
- Klicke beliebige Buttons/Pills und prüfe, ob ein Trace im Backend erscheint.
- Kontrolliere, dass Artwork/Meta korrekt ausgerichtet und nicht nach rechts verschoben ist.

---

**User Review Required:**
- Diese Änderung führt einen globalen Click-Listener ein. Jede Interaktion wird für Debugging-Zwecke an das Backend getraced.
- Bitte Review und Freigabe vor Umsetzung!
