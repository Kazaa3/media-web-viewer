# Implementation Plan: Fragment Integration & Level 2 Expansion (v1.46.028)

## Ziel
Integration von 10 bisher "verwaisten" HTML-Fragmente als dedizierte Level-2-Sub-Tabs (Pills) in die bestehende Navigation. Jede Funktion erhält einen klaren, benannten Zugangspunkt.

## Schritte

### 1. Navigation SSOT Expansion (config_master.py)
- **media:**
  - Alben-Ansicht (album_view.html)
  - Hörbuch-Sektor (audiobook_view.html)
  - Playlist-Profi (playlist_manager.html)
- **library:**
  - Film-Sektion (film_section.html)
  - Serien-Katalog (series_catalog.html)
- **video:**
  - Forensic-Player (video_player.html)
  - Video-Engine (video_view.html)
- **debug:**
  - Rescue-System (diagnostic_rescue.html)
  - DOM-Auditor (dom_audit.html)
- **reporting:**
  - System-Monitor (status_panel.html)

### 2. Frontend Logic Alignment (ui_nav_helpers.js)
- **switchMediaSubView:**
  - Routing für album_view.html, audiobook_view.html, playlist_manager.html im Media-Tab.
  - Routing für video_player.html, video_view.html im Video-Tab.
- **switchLibrarySubView:**
  - Routing für film_section.html, series_catalog.html im Bibliothek-Tab.
- **switchDiagnosticsSubView:**
  - Routing für diagnostic_rescue.html, dom_audit.html im Debug-Tab.
- **switchReportingView:**
  - Routing für status_panel.html im Report-Tab.

## Verifikationsplan
- Neue Pills erscheinen in der Sub-Navigation nach Klick auf die jeweilige Hauptkategorie.
- Klick auf Alben-Ansicht (Player) lädt album_view.html.
- Klick auf Rescue System (Debug) lädt diagnostic_rescue.html.
- Klick auf Forensic Player (Video) lädt video_player.html.
- Klick auf System Monitor (Report) lädt status_panel.html.

## Status
- Alle 10 Fragmente sind logisch und benutzerfreundlich in die Navigation integriert.
- Frontend-Routing ist für alle neuen Sub-Tabs implementiert.

---

**Freigabe erforderlich:**
Bitte bestätigen Sie, ob diese Integration wie beschrieben umgesetzt werden soll.