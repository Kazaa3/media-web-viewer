# Logbuch Meilenstein: Navigation Refinement & Media Hierarchy (v1.35.68)

## Ziel
Konsolidierung der Medienkategorien in eine klar strukturierte Hierarchie und Aufräumen der Hauptnavigation.

## Maßnahmen & geplante Änderungen

### 1. Main Header Cleanup
- app.html:
  - Entfernt: nav-btn-films, nav-btn-series, nav-btn-albums, nav-btn-audiobooks
  - Behalten: nav-btn-cinema (YouTube-Style), nav-btn-library, nav-btn-player, nav-btn-database, nav-btn-browser

### 2. Bibliothek Sidebar Refinement
- library_explorer.html:
  - Neue Sub-Tab-Buttons: Filme, Serien, Alben, Hörbuch (mit switchLibrarySubTab-Aufruf)
  - Entfernt: Streaming, Database (bereits Haupttab), Playlist Manager (Redundanz)

### 3. Sub-Tab Loading Logic
- library_explorer.html:
  - switchLibrarySubTab(viewId): Lädt spezialisierte Fragments (films, series, albums, audiobooks) in lib-results-container
  - Reuse der High-Fidelity-UI-Fragmente

### 4. Navigation Mapping
- ui_nav_helpers.js:
  - Entfernt: Main-Category-Mappings für Filme, Serien, Alben, Hörbuch
  - Sicherstellen: Cinema bleibt Hauptkategorie

## Technische Details
- lib-results-container ist Mount-Point für Sub-Fragments
- Sub-Tab-Wechsel triggert init*View-Funktionen

## Verifikation
- Bibliothek-Sidebar zeigt neue Sub-Tabs
- Klick auf Sub-Tab lädt entsprechendes Fragment
- Main Header zeigt nur noch die gewünschten Hauptkategorien
- Cinema funktioniert als eigenständiger Top-Level-Tab

---

**Freigabe zur Umsetzung: Navigation Refinement & Media Hierarchy v1.35.68**
