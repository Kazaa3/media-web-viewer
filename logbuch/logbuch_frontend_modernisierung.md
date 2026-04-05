# Logbuch – Frontend Optimization & Modernization (Meilenstein 1)

## Datum
30. März 2026

## Ziel
Optimierung und Modernisierung der Frontend-Struktur der App (app.html), um die Ladezeiten zu verbessern, die Wartbarkeit zu erhöhen und ein modernes, hochwertiges UI-Design (Glassmorphism) einzuführen.

## Geplante Änderungen
- **app.html**: Reduktion auf ein Skeleton mit globalen Komponenten (Header, Main, Footer, Sidebar). Statische Tab-Inhalte werden durch Platzhalter-Divs ersetzt. Inline-SVGs werden entfernt und durch eine externe SVG-Sprite (icons.svg) ersetzt.
- **icons.svg**: Auslagerung aller SVG-<symbol>-Definitionen aus app.html.
- **fragments/**: Auslagerung der Tab-Inhalte in einzelne HTML-Fragmente:
  - player_queue.html (Audio Player / Queue)
  - filesystem_browser.html (Dateibrowser)
  - library_explorer.html (Bibliothek/Coverflow)
  - item_inventory.html (SQLite-Repository)
  - playlist_manager.html (Playlist-Editor)
  - metadata_editor.html (Metadaten-Editor)
  - system_governance.html (Systemeinstellungen)
  - diagnostics_suite.html (Logs/Tests)
- **FragmentLoader**: Registrierung und dynamisches Nachladen aller Fragmente.
- **ui_nav_helpers.js**: Anpassung von switchTab für fragmentiertes Laden und Initialisierungshooks pro Fragment.
- **Design**: Umstellung auf Glassmorphic-Design mit modernen Farben und Animationen.

## Offene Fragen
- Schriftart: Google Fonts (z.B. Inter, Outfit) oder System-Default für Offline-Kompatibilität?
- Primäres Theme: Dunkles oder helles Glassmorphic-Design?

## Verifizierungsplan
- Automatisierte UI-Tests (js/ui_test_suite.js) für Tab-Switching und Interaktionen.
- Prüfung auf Konsolenfehler (Fragment-Loading, SVGs).
- Manuelle Überprüfung der Tabs, UI-Konsistenz und SVG-Icons.

## Status
Warten auf User-Feedback zu Schriftart und Theme. Umsetzung nach Freigabe.

---

**Siehe PR:** https://github.com/Kazaa3/media-web-viewer/pull/4

## Project Execution: Audio Analyzer and iPad OS Overhaul

### Date
1 April 2026

### Execution Status
- [x] Phase 1: Core Design System
  - [x] Update web/css/main.css with iPad OS variables and glassmorphism.
  - [x] Audit existing styles for consistency.
- [x] Phase 2: Global Shell Refactor
  - [x] Redesign web/app.html to a sidebar-based layout.
  - [x] Modernize the floating footer and media controller.
  - [x] Update web/js/ui_nav_helpers.js for the new navigation flow.
- [ ] Phase 3: Audio Player and Minimalist Analyzer
  - [x] Update web/fragments/player_queue.html with visualizer canvas.
  - [x] Implement AudioContext and AnalyserNode in web/js/audioplayer.js.
  - [/] Refactor renderPlaylist for modern, rounded list items (in progress).
  - [ ] Implement multiple visualizer styles (Bars, Circles, Wave).
- [ ] Phase 4: Video Player and Orchestrator Integration
  - [ ] Move Orchestrator controls from app.html/tools_panel.html to web/fragments/video_player.html.
  - [ ] Update web/js/video.js to refresh orchestrator state in the new UI.
- [ ] Phase 5: Options and Sidebar Persistence
  - [ ] Add Default Sidebar State setting in Options panel.
  - [ ] Add Visualizer Style setting in Options/Player.
  - [ ] Implement local storage persistence for these settings.
- [ ] Phase 6: Verification and Polish

### Next Steps
1. Complete renderPlaylist refactor in web/js/audioplayer.js.
2. Implement visualizer styles with setting-based switching.
3. Integrate orchestrator UI in web/fragments/video_player.html and wire web/js/video.js.
4. Add options and local storage persistence.
5. Run final verification and polish pass.

## Implementation Plan: Logbook Restoration and v1.34 Standardization

### Date
1 April 2026

### User Review Required
IMPORTANT

- Sidebar Integration: The Logbook is accessible via the Management section of the new iPad OS sidebar.
- Design Language: The Logbook interface is converted to a deep-dark, glassmorphic style aligned with the v1.34 overhaul.
- Version Rollback: System version labels are standardized to v1.34.

### Proposed Changes

#### Core Shell and Branding
- [MODIFY] app.html
  - Standardize version strings from v1.35 to v1.34.
  - Update main titles:
    - Short: Media Viewer
    - Long: Desktop Media Player and Library Manager
  - Ensure the Logbook sidebar entry is correctly linked.
- [MODIFY] options_panel.html
  - Update version badge to v1.34 Core.

#### Logbook (Journal) Module
- [MODIFY] logbook_panel.html
  - Refactor styles to CSS variables (--bg-primary, --border-color) instead of hardcoded hex colors.
  - Apply .glass-card and .glass-blur to sidebar and viewer panes.
  - Standardize typography: Inter for UI and JetBrains Mono for metadata/code blocks.
  - Modernize Sync and New Entry buttons with premium silhouettes and hover states.
- [MODIFY] logbook_helpers.js
  - Update renderLogbuchList() to generate modernized list items with glassy backgrounds and hover animations.
  - Standardize status icons using the v1.34 SVG icon library.

#### Navigation Logic
- [MODIFY] ui_nav_helpers.js
  - Ensure switchMainCategory(logbuch) triggers fragment loading and displays logbook-tab-container.

### Open Question
- Should the Logbook sidebar item move to the top Media section instead of Management? (Current plan keeps it in Management/Governance.)

### Verification Plan (Manual)
- Header/Footer Audit: Confirm version displays as v1.34 in all visible locations.
- Sidebar Navigation: Click Logbuch and verify fragment loading is smooth.
- Rendering Check: Select a log entry and verify markdown renders correctly in dark theme.
- Editor Check: Click Neuer Eintrag and verify editor modal opens and functions.
