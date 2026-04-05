# Logbuch – Layout-Standardisierung: Player & Playlist

## Datum
30. März 2026

## Ziel
Harmonisierung des Layouts zwischen dem "Player" (Audio) und dem "Playlist"-Modul. Beide Ansichten sollen eine linke Sidebar und einen dedizierten Content-Bereich rechts aufweisen.

---

## Geplante/Umgesetzte Änderungen

### 1. UI-Navigation & Orchestrierung
- **ui_nav_helpers.js**:
  - `sidebarVisibleTabs` wurde um den Playlist-Tab ergänzt.
  - Die globale Sidebar wird für beide Fragmente konsistent verwaltet.

### 2. Fragment-Refactoring
- **player_queue.html**:
  - Inhalte der linken und rechten Pane wurden getauscht.
  - Linke Pane: Enthält jetzt das `active-queue-list-render-target` (aktuelle Warteschlange).
  - Rechte Pane: Neue "Now Playing"-Area mit Artwork, Metadaten und Wiedergabestatistiken.
- **playlist_manager.html**:
  - Styling der Sidebar (Breite, Border) an die des Player-Tabs angepasst.
  - Header und Aktionsbuttons konsistent positioniert.

### 3. Logik & Rendering
- **audioplayer.js**:
  - `renderPlaylist` ggf. angepasst, um neue IDs und die "Now Playing"-Sektion korrekt zu bedienen.
  - Sicherstellung, dass "Now Playing"-Inhalte rechts synchron zur Sidebar und zum Footer aktualisiert werden.

---

## Offene Frage
- **Metadaten-Spiegelung:**
  - Sollen die Metadaten (Artwork, Titel etc.) im Player-Tab nur rechts angezeigt werden oder zusätzlich weiterhin in der globalen Sidebar?
  - **Empfehlung:** Spiegelung im rechten Bereich für ein "Big Player"-Erlebnis, Sidebar bleibt für cross-tab Status erhalten.

---

## Verifikation
- Layout bleibt beim Wechsel zwischen Player- und Playlist-Tab konsistent (Links: Sidebar, Rechts: Content).
- Klick auf ein Element in der Sidebar (Playlist- oder Queue-Auswahl) aktualisiert den rechten Content-Bereich korrekt.
- "Now Playing"-Details werden im Player-Tab rechts korrekt angezeigt.

---

**Siehe PR:** https://github.com/Kazaa3/media-web-viewer/pull/4
